"""Consultas de contatos da Application API do Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping

from .models import Contact

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class ContactsResource:
    """Operações da categoria Contacts."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def get(self, account_id: int, contact_id: int) -> dict[str, Any]:
        """GET /api/v1/accounts/{account_id}/contacts/{id}: contato por ID."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        path = f"api/v1/accounts/{account_id}/contacts/{contact_id}"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_objeto(
            response, operacao="consultar o contato", caminho=path
        )

    def list(self, account_id: int, *, sort: str | None = None, page: int | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/contacts; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/contacts"
        consulta: dict[str, Any] = {
            "sort": sort,
            "page": page,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create(
        self,
        account_id: int,
        contact: Contact,
        *,
        inbox_id: int | None = None,
        source_id: str | None = None,
    ) -> dict[str, Any]:
        """POST: dados tipados; associação à inbox é opcional no controlador."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(contact, Contact):
            raise TypeError("contact deve ser Contact.")
        dados = contact.to_payload()
        if inbox_id is not None:
            self._client._validar_id(inbox_id, "inbox_id")
            dados["inbox_id"] = inbox_id
        if source_id is not None:
            if inbox_id is None:
                raise ValueError("source_id somente pode ser informado com inbox_id.")
            if not isinstance(source_id, str) or not source_id.strip():
                raise ValueError("source_id deve ser texto não vazio.")
            dados["source_id"] = source_id
        if not dados:
            raise ValueError("Informe ao menos um campo do contato ou inbox_id.")
        caminho = f"api/v1/accounts/{account_id}/contacts"
        resposta = self._client._post(caminho, dados=dados)
        return self._client._exigir_objeto(
            resposta, operacao="criar contato", caminho=caminho
        )

    def update(
        self, account_id: int, contact_id: int, contact: Contact,
    ) -> dict[str, Any] | None:
        """PUT parcial: apenas campos presentes no contrato vão ao servidor.

        Não busca nem reenvia valores já cadastrados; ausência significa
        preservação no backend, e None explícito é enviado como JSON null.
        """
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        if not isinstance(contact, Contact):
            raise TypeError("contact deve ser Contact.")
        dados = contact.to_payload()
        if not dados:
            raise ValueError("Atualização requer pelo menos um campo informado.")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}"
        resposta = self._client._put(caminho, dados=dados)
        if resposta is None:
            return None
        return self._client._exigir_objeto(
            resposta, operacao="atualizar contato", caminho=caminho
        )

    def delete(self, account_id: int, contact_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/contacts/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)

    def list_conversations(self, account_id: int, contact_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/contacts/{id}/conversations; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/conversations"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def search(self, account_id: int, *, q: str | None = None, sort: str | None = None, page: int | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/contacts/search; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/contacts/search"
        consulta: dict[str, Any] = {
            "q": q,
            "sort": sort,
            "page": page,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def filter(self, account_id: int, data: Mapping[str, Any], *, page: int | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/contacts/filter; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/contacts/filter"
        consulta: dict[str, Any] = {
            "page": page,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def add_inbox(self, account_id: int, contact_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/contacts/{id}/contact_inboxes; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/contact_inboxes"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def list_contactable_inboxes(self, account_id: int, contact_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/contacts/{id}/contactable_inboxes; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/contactable_inboxes"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def merge(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/actions/contact_merge; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/actions/contact_merge"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)
