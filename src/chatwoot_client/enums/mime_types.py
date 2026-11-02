"""Tipos MIME comuns, sem bloquear tipos adicionais válidos."""
from enum import StrEnum


class MimeType(StrEnum):
    PDF = "application/pdf"
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    WEBP = "image/webp"
    MP4 = "video/mp4"
    WEBM = "video/webm"
    MP3 = "audio/mpeg"
    OGG = "audio/ogg"
    WAV = "audio/wav"
    TEXT = "text/plain"
    CSV = "text/csv"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    OCTET_STREAM = "application/octet-stream"
