"""Contrato imutável de anexo, independente da origem do conteúdo."""
from __future__ import annotations

import mimetypes
import re
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import BinaryIO
from urllib.parse import unquote, urlsplit

from ..enums import MimeType

_MIME = re.compile(r"^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+$")


@dataclass(frozen=True, slots=True)
class Attachment:
    """Origem local, URL HTTPS, bytes ou arquivo binário aberto.

    Arquivos locais e URLs são resolvidos somente durante o envio.
    Para bytes e streams sem nome, informe `filename`.
    """
    source: str | Path | bytes | BinaryIO
    mime_type: MimeType | str | None = None
    filename: str | None = None

    def __post_init__(self) -> None:
        source = self.source
        if isinstance(source, str):
            if not source.strip():
                raise ValueError("source não pode ser vazio.")
            if "://" in source:
                url = urlsplit(source)
                if url.scheme != "https" or not url.hostname or url.username or url.password or url.fragment:
                    raise ValueError("URLs de anexos devem ser HTTPS, sem credenciais ou fragmento.")
                nome = Path(unquote(url.path)).name
            else:
                nome = PureWindowsPath(source).name if "\\" in source else Path(source).name
        elif isinstance(source, Path):
            nome = source.name
        elif isinstance(source, bytes):
            if not source:
                raise ValueError("bytes do anexo não podem ser vazios.")
            nome = None
        elif callable(getattr(source, "read", None)):
            nome = None
        else:
            raise TypeError("source deve ser caminho, URL HTTPS, bytes ou fluxo binário.")

        filename = self.filename if self.filename is not None else nome
        if not isinstance(filename, str) or not filename or len(filename) > 255:
            raise ValueError("filename é obrigatório e deve ter até 255 caracteres.")
        if (
            filename != Path(filename).name
            or filename != PureWindowsPath(filename).name
            or any(ch in filename for ch in ("\x00", "\r", "\n"))
            or filename in {".", ".."}
        ):
            raise ValueError("filename deve ser um nome simples, sem diretórios.")

        mime = self.mime_type
        if mime is None:
            mime = mimetypes.guess_type(filename)[0]
        if not isinstance(mime, str) or not _MIME.fullmatch(mime):
            raise ValueError("mime_type deve ser um MIME válido, como MimeType.PDF.")
        object.__setattr__(self, "filename", filename)
        object.__setattr__(self, "mime_type", str(mime))

    @classmethod
    def from_path(
        cls, path: str | Path, *, mime_type: MimeType | str | None = None,
        filename: str | None = None,
    ) -> Attachment:
        return cls(source=path, mime_type=mime_type, filename=filename)

    @classmethod
    def from_url(
        cls, url: str, *, mime_type: MimeType | str | None = None,
        filename: str | None = None,
    ) -> Attachment:
        if not isinstance(url, str) or not url.startswith("https://"):
            raise ValueError("from_url requer uma URL HTTPS.")
        return cls(source=url, mime_type=mime_type, filename=filename)
