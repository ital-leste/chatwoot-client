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


def _validar_url_publica(url: str, allowed_hosts: frozenset[str] | None) -> None:
    parsed = urlsplit(url)
    host = parsed.hostname
    if parsed.scheme != "https" or not host or parsed.username or parsed.password or parsed.fragment:
        raise ErroAnexoChatwoot("URL de anexo inválida: exige HTTPS.")
    if parsed.port not in (None, 443):
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
    while chunk := source.read(64 * 1024):
        if not isinstance(chunk, bytes):
            raise ErroAnexoChatwoot("O fluxo do anexo deve fornecer bytes.")
        total += len(chunk)
        if total > limit:
            raise ErroAnexoChatwoot("Anexo excede o limite de tamanho configurado.")
        dest.write(chunk)
    if not total:
        raise ErroAnexoChatwoot("Anexo vazio.")


def _resolver_url(url: str, dest: BinaryIO, limit: int, timeout: float) -> None:
    try:
        # Cliente separado: token do Chatwoot nunca é enviado ao host da mídia.
        with httpx.Client(timeout=timeout, follow_redirects=False, trust_env=False) as web:
            with web.stream("GET", url) as response:
                if response.status_code != 200:
                    raise ErroAnexoChatwoot("Servidor de mídia não retornou HTTP 200.")
                size = response.headers.get("content-length")
                if size and size.isdecimal() and int(size) > limit:
                    raise ErroAnexoChatwoot("Anexo excede o limite de tamanho configurado.")
                count = 0
                for chunk in response.iter_bytes(64 * 1024):
                    count += len(chunk)
                    if count > limit:
                        raise ErroAnexoChatwoot("Anexo excede o limite de tamanho configurado.")
                    dest.write(chunk)
                if count == 0:
                    raise ErroAnexoChatwoot("Anexo remoto vazio.")
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
                _resolver_url(src, temp, max_bytes, timeout)
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
