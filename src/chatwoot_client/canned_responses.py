"""Canned Responses da Application API Chatwoot 4.19."""
from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from .models import CannedResponse, CannedResponseCreate, CannedResponseUpdate

if TYPE_CHECKING:
    from .client import CWClient


class CannedResponsesResource:
    """Consultas com filtro opcional, criação, atualização e exclusão."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    @staticmethod
    def _parametros_consulta(
        *, search: str | None, parametros: Mapping[str, Any] | None,
    ) -> dict[str, Any] | None:
        if parametros is not None and not isinstance(parametros, Mapping):
            raise ValueError("parametros deve ser um mapeamento de consulta.")
        consulta = dict(parametros or {})
        if search is not None:
            if not isinstance(search, str) or not search.strip() or "\x00" in search:
                raise ValueError("search deve ser texto não vazio e sem NUL.")
            if "search" in consulta:
                raise ValueError("Use search ou parametros['search'], não ambos.")
            consulta["search"] = search.strip()
        return consulta or None

    def list(
        self,
        account_id: int,
        *,
        search: str | None = None,
        parametros: Mapping[str, Any] | None = None,
    ) -> Any:
        """GET sem search lista tudo; GET com search filtra no Chatwoot.

        O retorno permanece o array JSON original, por retrocompatibilidade.
        `parametros={"search": ...}` continua aceito.
        """
        self._client._validar_id(account_id, "account_id")
        consulta = self._parametros_consulta(search=search, parametros=parametros)
        caminho = f"api/v1/accounts/{account_id}/canned_responses"
        return self._client._get(caminho, parametros=consulta)

    def list_typed(
        self, account_id: int, *, search: str | None = None,
    ) -> list[CannedResponse]:
        """Mesma consulta de list, com desserialização validada de cada item."""
        caminho = f"api/v1/accounts/{account_id}/canned_responses"
        resultado = self.list(account_id, search=search)
        lista = self._client._exigir_lista(
            resultado, operacao="consultar respostas rápidas", caminho=caminho
        )
        try:
            return [CannedResponse.from_api(item) for item in lista]
        except ValueError:
            from .client import ErroAPIChatwoot
            raise ErroAPIChatwoot(
                "Chatwoot retornou uma resposta rápida com estrutura inválida.",
                caminho=caminho,
            ) from None

    def create(
        self,
        account_id: int,
        data: Mapping[str, Any] | CannedResponseCreate,
        *,
        parametros: Mapping[str, Any] | None = None,
    ) -> Any:
        """POST: contrato tipado ou payload histórico (mapping)."""
        self._client._validar_id(account_id, "account_id")
        if isinstance(data, CannedResponseCreate):
            dados: Mapping[str, Any] = data.to_payload()
        elif isinstance(data, Mapping):
            dados = data
        else:
            raise ValueError("data deve ser CannedResponseCreate ou objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/canned_responses"
        return self._client._post(caminho, dados=dados, parametros=parametros)

    def update(
        self,
        account_id: int,
        canned_response_id: int,
        data: Mapping[str, Any] | CannedResponseUpdate,
        *,
        parametros: Mapping[str, Any] | None = None,
    ) -> Any:
        """PATCH: atualização parcial tipada ou payload histórico."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(canned_response_id, "canned_response_id")
        if isinstance(data, CannedResponseUpdate):
            dados: Mapping[str, Any] = data.to_payload()
        elif isinstance(data, Mapping):
            dados = data
        else:
            raise ValueError("data deve ser CannedResponseUpdate ou objeto JSON.")
        caminho = (
            f"api/v1/accounts/{account_id}/canned_responses/{canned_response_id}"
        )
        return self._client._patch(caminho, dados=dados, parametros=parametros)

    def delete(
        self,
        account_id: int,
        canned_response_id: int,
        *,
        parametros: Mapping[str, Any] | None = None,
    ) -> Any:
        """DELETE por ID; endpoint não possui operação de restauração."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(canned_response_id, "canned_response_id")
        caminho = (
            f"api/v1/accounts/{account_id}/canned_responses/{canned_response_id}"
        )
        return self._client._delete(caminho, parametros=parametros)
