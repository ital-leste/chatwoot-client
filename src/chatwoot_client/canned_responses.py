"""Operações de Canned Responses com parâmetros tipados e JSON nativo."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class CannedResponsesResource:
    """CRUD de respostas rápidas da conta, sem contratos de domínio extras."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    @staticmethod
    def _validar_texto(valor: str, nome: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{nome} deve ser texto não vazio.")
        return valor

    @staticmethod
    def _validar_search(search: str | None) -> dict[str, str] | None:
        if search is None:
            return None
        if not isinstance(search, str) or not search.strip() or "\x00" in search:
            raise ValueError("search deve ser texto não vazio e sem NUL.")
        return {"search": search.strip()}

    def list(self, account_id: int, *, search: str | None = None) -> list[dict[str, Any]]:
        """GET: sem search retorna tudo; com search filtra no servidor."""
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

    def create(
        self, account_id: int, *, short_code: str, content: str,
    ) -> dict[str, Any]:
        """POST: atalho e conteúdo obrigatórios, com retorno JSON original."""
        self._client._validar_id(account_id, "account_id")
        dados = {
            "short_code": self._validar_texto(short_code, "short_code"),
            "content": self._validar_texto(content, "content"),
        }
        caminho = f"api/v1/accounts/{account_id}/canned_responses"
        resultado = self._client._post(caminho, dados=dados)
        return self._client._exigir_objeto(
            resultado, operacao="criar resposta rápida", caminho=caminho
        )

    def update(
        self,
        account_id: int,
        canned_response_id: int,
        *,
        short_code: str | None = None,
        content: str | None = None,
    ) -> dict[str, Any]:
        """PATCH parcial: envia exclusivamente os campos informados."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(canned_response_id, "canned_response_id")
        dados: dict[str, str] = {}
        if short_code is not None:
            dados["short_code"] = self._validar_texto(short_code, "short_code")
        if content is not None:
            dados["content"] = self._validar_texto(content, "content")
        if not dados:
            raise ValueError("Atualização requer short_code e/ou content.")
        caminho = f"api/v1/accounts/{account_id}/canned_responses/{canned_response_id}"
        resultado = self._client._patch(caminho, dados=dados)
        return self._client._exigir_objeto(
            resultado, operacao="atualizar resposta rápida", caminho=caminho
        )

    def delete(self, account_id: int, canned_response_id: int) -> Any:
        """DELETE: JSON nativo ou None quando o sucesso não possui corpo."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(canned_response_id, "canned_response_id")
        caminho = f"api/v1/accounts/{account_id}/canned_responses/{canned_response_id}"
        return self._client._delete(caminho)
