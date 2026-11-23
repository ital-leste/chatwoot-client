"""Resolução segura de anexos para multipart, sem Base64 nem download no model."""
from __future__ import annotations

import ipaddress
import socket
import tempfile
from contextlib import ExitStack, contextmanager
from pathlib import Path
from typing import BinaryIO, Iterator
from urllib.parse import urlsplit

import httpx

from .models import Attachment

DEFAULT_MAX_BYTES = 25 * 1024 * 1024


class ErroAnexoChatwoot(ValueError):
    """Arquivo ou URL de anexo inválido/inacessível."""


class ErroRedirecionamentoAnexoChatwoot(ErroAnexoChatwoot):
    """Redirecionamento de mídia rejeitado antes de qualquer POST."""


def _validar_url_publica(url: str, allowed_hosts: frozenset[str] | None) -> None:
    try:
        parsed = urlsplit(url)
        host = parsed.hostname
        porta = parsed.port
    except ValueError:
        raise ErroAnexoChatwoot("URL de anexo contém host ou porta inválidos.") from None
    if (
        parsed.scheme != "https"
        or not host
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or parsed.netloc.endswith(":")
        or any(ch.isspace() or ch == "\\" for ch in parsed.netloc)
    ):
        raise ErroAnexoChatwoot("URL de anexo inválida: exige HTTPS.")
    if porta not in (None, 443):
        raise ErroAnexoChatwoot("URL de anexo deve usar a porta HTTPS padrão.")
    host = host.lower().rstrip(".")
    if host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
        raise ErroAnexoChatwoot("URL de anexo não pode apontar para rede local.")
    if allowed_hosts is not None and host not in allowed_hosts:
        raise ErroAnexoChatwoot("Domínio de anexo fora da lista permitida.")
    try:
        ips = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        if not ips or any(
            not ipaddress.ip_address(result[4][0]).is_global for result in ips
        ):
            raise ErroAnexoChatwoot("URL de anexo resolve para endereço não público.")
    except (OSError, ValueError) as exc:
        if isinstance(exc, ErroAnexoChatwoot):
            raise
        raise ErroAnexoChatwoot("Não foi possível validar o destino do anexo.") from None


def _copiar_limitado(source: BinaryIO, dest: BinaryIO, limit: int) -> None:
    total = 0
    while True:
        chunk = source.read(64 * 1024)
        if chunk == b"":
            break
        # read() == None não é EOF: não enviar anexo parcialmente copiado.
        if not isinstance(chunk, bytes):
            raise ErroAnexoChatwoot("O fluxo do anexo deve fornecer bytes; read() não pode retornar None.")
        total += len(chunk)
        if total > limit:
            raise ErroAnexoChatwoot("Anexo excede o limite de tamanho configurado.")
        dest.write(chunk)
    if not total:
        raise ErroAnexoChatwoot("Anexo vazio.")


def _validar_midia_remota(tipo_declarado: str, cabecalho: str, primeiros_bytes: bytes) -> None:
    """Rejeita HTML e imagens remotas incompatíveis com o MIME declarado."""
    tipo = tipo_declarado.split(";", 1)[0].strip().lower()
    recebido = cabecalho.split(";", 1)[0].strip().lower()
    if recebido in {"text/html", "application/xhtml+xml"}:
        raise ErroAnexoChatwoot("Servidor de mídia retornou HTML, não um anexo.")
    assinaturas = {
        "image/png": lambda b: b.startswith(bytes.fromhex("89504e470d0a1a0a")),
        "image/jpeg": lambda b: b.startswith(bytes.fromhex("ffd8ff")),
        "image/gif": lambda b: b.startswith((b"GIF87a", b"GIF89a")),
        "image/webp": lambda b: len(b) >= 12 and b[:4] == b"RIFF" and b[8:12] == b"WEBP",
    }
    if tipo in assinaturas and (
        recebido not in {tipo, "application/octet-stream", ""}
        or not assinaturas[tipo](primeiros_bytes)
    ):
        raise ErroAnexoChatwoot("Conteúdo remoto incompatível com o tipo de imagem declarado.")


def _resolver_url(url: str, dest: BinaryIO, limit: int, timeout: float, mime_type: str) -> None:
    try:
        # Cliente separado: token do Chatwoot nunca é enviado ao host da mídia.
        with httpx.Client(timeout=timeout, follow_redirects=False, trust_env=False) as web:
            with web.stream("GET", url) as response:
                if 300 <= response.status_code < 400:
                    # Política explícita: URLs finais são obrigatórias. Seguir
                    # Location automaticamente pode ultrapassar a allowlist.
                    raise ErroRedirecionamentoAnexoChatwoot(
                        "Redirect de anexo rejeitado; utilizar URL HTTPS final autorizada."
                    )
                if response.status_code != 200:
                    raise ErroAnexoChatwoot("Servidor de mídia não retornou HTTP 200.")
                size = response.headers.get("content-length")
                if size and size.isdecimal() and int(size) > limit:
                    raise ErroAnexoChatwoot("Anexo excede o limite de tamanho configurado.")
                count = 0
                primeiros_bytes = b""
                for chunk in response.iter_bytes(64 * 1024):
                    if len(primeiros_bytes) < 16:
                        primeiros_bytes += chunk[:16 - len(primeiros_bytes)]
                    count += len(chunk)
                    if count > limit:
                        raise ErroAnexoChatwoot("Anexo excede o limite de tamanho configurado.")
                    dest.write(chunk)
                if count == 0:
                    raise ErroAnexoChatwoot("Anexo remoto vazio.")
                _validar_midia_remota(mime_type, response.headers.get("content-type", ""), primeiros_bytes)
    except httpx.HTTPError:
        raise ErroAnexoChatwoot("Falha no download HTTPS do anexo.") from None


@contextmanager
def preparar_anexos(
    attachments: tuple[Attachment, ...],
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    timeout: float = 30.0,
    allowed_hosts: frozenset[str] | None = None,
) -> Iterator[list[tuple[str, tuple[str, bytes | BinaryIO, str]]]]:
    """Prepara streams multipart e fecha apenas arquivos abertos pela biblioteca.

    URL e fluxos externos são copiados de forma limitada para arquivo temporário.
    Caminhos locais são transmitidos por streaming; bytes não são recodificados.
    """
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes <= 0:
        raise ValueError("max_bytes deve ser inteiro positivo.")
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or not (0 < timeout < float("inf")):
        raise ValueError("timeout deve ser positivo e finito.")
    if allowed_hosts is not None:
        if not isinstance(allowed_hosts, (set, frozenset)) or any(
            not isinstance(host, str) or not host for host in allowed_hosts
        ):
            raise ValueError("allowed_hosts deve ser um conjunto de domínios.")
        allowed_hosts = frozenset(host.lower().rstrip(".") for host in allowed_hosts)
    files: list[tuple[str, tuple[str, bytes | BinaryIO, str]]] = []
    with ExitStack() as stack:
        for attachment in attachments:
            src = attachment.source
            if isinstance(src, bytes):
                if len(src) > max_bytes:
                    raise ErroAnexoChatwoot("Anexo excede o limite de tamanho configurado.")
                data: bytes | BinaryIO = src
            elif isinstance(src, str) and src.startswith("https://"):
                _validar_url_publica(src, allowed_hosts)
                temp = stack.enter_context(tempfile.SpooledTemporaryFile(max_size=1024 * 1024, mode="w+b"))
                _resolver_url(src, temp, max_bytes, timeout, attachment.mime_type)
                temp.seek(0)
                data = temp
            elif isinstance(src, (str, Path)):
                path = Path(src)
                try:
                    if not path.is_file():
                        raise ErroAnexoChatwoot("Caminho do anexo não é um arquivo.")
                    size = path.stat().st_size
                    if size <= 0 or size > max_bytes:
                        raise ErroAnexoChatwoot("Arquivo vazio ou acima do limite de tamanho.")
                    data = stack.enter_context(path.open("rb"))
                except OSError:
                    raise ErroAnexoChatwoot("Não foi possível abrir o arquivo local.") from None
            else:
                temp = stack.enter_context(tempfile.SpooledTemporaryFile(max_size=1024 * 1024, mode="w+b"))
                try:
                    _copiar_limitado(src, temp, max_bytes)
                except (OSError, TypeError):
                    raise ErroAnexoChatwoot("Não foi possível ler o fluxo do anexo.") from None
                temp.seek(0)
                data = temp
            files.append(("attachments[]", (attachment.filename, data, attachment.mime_type)))
        yield files
