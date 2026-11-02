"""Operações tipadas de entrada e respostas JSON nativas para Canned Responses."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .models import CannedResponse

if TYPE_CHECKING:
    from .client import CWClient


class CannedResponsesResource:
    """CRUD de respostas rápidas da conta, sem modelos de saída."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    @staticmethod
    def _validar_search(search: str | None) -> dict[str, str] | None:
        if search is None:
            return None
        if not isinstance(search, str) or not search.strip() or "\x00" in search:
            raise ValueError("search deve ser texto não vazio e sem NUL.")
        return {"search": search.strip()}

    def list(self, account_id: int, *, search: str | None = None) -> list[dict[str, Any]]:
        """GET: sem search retorna tudo, com search filtra no Chatwoot."""
        self._client._validar_id(account_id, "account_id")
        consulta = self._validar_search(search)
        caminho = f"api/v1/accounts/{account_id}/canned_responses"
        resposta = self._client._get(caminho, parametros=consulta)
        lista = self._client._exigir_lista(
            resposta, operacao="listar respostas rápidas", caminho=caminho
        )
        if any(not isinstance(item, dict) for item in lista):
            from .client import ErroAPIChatwoot
            raise ErroAPIChatwoot(
                "Chatwoot retornou itens inválidos na lista de respostas rápidas.",
                caminho=caminho,
            )
        return lista

    def create(self, account_id: int, response: CannedResponse) -> dict[str, Any]:
        """POST: os dois campos são obrigatórios."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(response, CannedResponse):
            raise TypeError("response deve ser CannedResponse.")
        if response.short_code is None or response.content is None:
            raise ValueError("Criação requer short_code e content.")
        caminho = f"api/v1/accounts/{account_id}/canned_responses"
        resultado = self._client._post(caminho, dados=response.to_payload())
        return self._client._exigir_objeto(
            resultado, operacao="criar resposta rápida", caminho=caminho
        )

    def update(
        self, account_id: int, canned_response_id: int, response: CannedResponse,
    ) -> dict[str, Any]:
        """PATCH: apenas os campos informados, sem sobrescrever os demais."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(canned_response_id, "canned_response_id")
        if not isinstance(response, CannedResponse):
            raise TypeError("response deve ser CannedResponse.")
        dados = response.to_payload()
        if not dados:
            raise ValueError("Atualização requer short_code e/ou content.")
        caminho = f"api/v1/accounts/{account_id}/canned_responses/{canned_response_id}"
        resultado = self._client._patch(caminho, dados=dados)
        return self._client._exigir_objeto(
            resultado, operacao="atualizar resposta rápida", caminho=caminho
        )

    def delete(self, account_id: int, canned_response_id: int) -> Any:
        """DELETE: devolve corpo JSON nativo ou None caso vazio."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(canned_response_id, "canned_response_id")
        caminho = f"api/v1/accounts/{account_id}/canned_responses/{canned_response_id}"
        return self._client._delete(caminho)
