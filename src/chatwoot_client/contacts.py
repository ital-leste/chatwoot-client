"""Consultas de contatos da Application API do Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from .models import Contact, FilterCondition
from .models.filters import _serializar_filtros

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

    def filter(
        self, account_id: int, filters: Sequence[FilterCondition], *, page: int | None = None,
    ) -> dict[str, Any]:
        """POST de filtros estruturados compartilhados com Conversations."""
        self._client._validar_id(account_id, "account_id")
        if page is not None:
            self._client._validar_id(page, "page")
        caminho = f"api/v1/accounts/{account_id}/contacts/filter"
        resposta = self._client._post(
            caminho,
            dados={"payload": _serializar_filtros(filters)},
            parametros={"page": page} if page is not None else None,
        )
        return self._client._exigir_objeto(
            resposta, operacao="filtrar contatos", caminho=caminho
        )


    def add_inbox(
        self, account_id: int, contact_id: int, *, inbox_id: int,
        source_id: str | None = None,
    ) -> Any:
        """Associa contato à inbox com identificador explícito."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        self._client._validar_id(inbox_id, "inbox_id")
        dados: dict[str, Any] = {"inbox_id": inbox_id}
        if source_id is not None:
            if not isinstance(source_id, str) or not source_id.strip():
                raise ValueError("source_id deve ser string não vazia.")
            dados["source_id"] = source_id
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/contact_inboxes"
        return self._client._post(caminho, dados=dados)

    def list_contactable_inboxes(self, account_id: int, contact_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/contacts/{id}/contactable_inboxes; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/contactable_inboxes"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)


    def merge(
        self, account_id: int, *, base_contact_id: int, mergee_contact_id: int,
    ) -> Any:
        """Mescla contato de origem no principal: operação potencialmente destrutiva."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(base_contact_id, "base_contact_id")
        self._client._validar_id(mergee_contact_id, "mergee_contact_id")
        if base_contact_id == mergee_contact_id:
            raise ValueError("Os contatos devem ser diferentes.")
        caminho = f"api/v1/accounts/{account_id}/actions/contact_merge"
        return self._client._post(
            caminho, dados={
                "base_contact_id": base_contact_id,
                "mergee_contact_id": mergee_contact_id,
            },
        )

