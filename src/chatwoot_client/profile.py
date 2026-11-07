"""Consultas do perfil autenticado na API Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping

from typing import TYPE_CHECKING, Any

from .models.application import ProfileInput

if TYPE_CHECKING:
    from .client import CWClient


class ProfileResource:
    """Operações de consulta do perfil associado ao token de API."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def get(self) -> dict[str, Any]:
        """Retorna o JSON do perfil associado ao token, sem alterar dados."""
        path = "api/v1/profile"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_objeto(
            response,
            operacao="consultar o perfil",
            caminho=path,
        )

    def update(self, profile: ProfileInput) -> Any:
        """PUT com envelope profile; não imprime nem registra credenciais."""
        if not isinstance(profile, ProfileInput):
            raise TypeError("profile deve ser ProfileInput.")
        return self._client._put("api/v1/profile", dados={"profile": profile.to_payload()})

    def update_multipart(
        self,
        *,
        avatar: tuple[str, bytes, str],
        fields: Mapping[str, str] | None = None,
    ) -> Any:
        """PUT /api/v1/profile via multipart, inclusive avatar do perfil."""
        if (
            not isinstance(avatar, tuple) or len(avatar) != 3
            or not isinstance(avatar[0], str) or not avatar[0]
            or not isinstance(avatar[1], bytes)
            or not isinstance(avatar[2], str) or not avatar[2]
        ):
            raise ValueError("avatar deve ser (nome, bytes, MIME).")
        if fields is not None and (
            not isinstance(fields, Mapping) or any(
                not isinstance(k, str) or not k or not isinstance(v, str)
                for k, v in fields.items()
            )
        ):
            raise ValueError("fields deve ser um mapeamento texto para texto.")
        formulario = {f"profile[{chave}]": valor for chave, valor in (fields or {}).items()}
        caminho = "api/v1/profile"
        return self._client._solicitar_json(
            "PUT", caminho, formulario=formulario,
            arquivos=[("profile[avatar]", avatar)],
        )

