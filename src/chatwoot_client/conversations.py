"""Recurso Conversations — entradas tipadas e retornos JSON nativos."""
from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal

from .enums import ConversationPriority, ConversationStatus
from .models import ConversationCreate, FilterCondition
from .models.filters import _serializar_filtros

if TYPE_CHECKING:
    from .client import CWClient

_FILTROS_STATUS = {"all", "open", "resolved", "pending", "snoozed"}
_FILTROS_ATENDENTE = {"me", "unassigned", "all", "assigned"}
_ORDENACAO_FILTROS = {
    "last_activity_at_asc", "last_activity_at_desc",
    "created_at_asc", "created_at_desc",
    "priority_asc", "priority_desc",
    "waiting_since_asc", "waiting_since_desc",
    "priority_desc_created_at_asc", "unread",
}


class ConversationsResource:
    """Interface Python para os endpoints oficiais de conversas."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    @staticmethod
    def _validar_lista_labels(labels: list[str] | None) -> list[str] | None:
        if labels is None:
            return None
        if not isinstance(labels, list) or any(
            not isinstance(label, str) or not label.strip() for label in labels
        ):
            raise ValueError("labels deve ser lista de textos não vazios.")
        return labels

    def _consulta_conversas(
        self,
        *,
        status: str | None,
        q: str | None,
        inbox_id: int | None,
        team_id: int | None,
        labels: list[str] | None,
    ) -> dict[str, Any]:
        if status is not None and (
            not isinstance(status, str) or status not in _FILTROS_STATUS
        ):
            raise ValueError("status de consulta deve ser all, open, resolved, pending ou snoozed.")
        if q is not None and (not isinstance(q, str) or not q.strip()):
            raise ValueError("q deve ser texto não vazio.")
        for valor, nome in ((inbox_id, "inbox_id"), (team_id, "team_id")):
            if valor is not None:
                self._client._validar_id(valor, nome)
        consulta: dict[str, Any] = {}
        for nome, valor in (
            ("status", status), ("q", q), ("inbox_id", inbox_id), ("team_id", team_id)
        ):
            if valor is not None:
                consulta[nome] = valor
        lista = self._validar_lista_labels(labels)
        if lista is not None:
            consulta["labels[]"] = lista
        return consulta

    @staticmethod
    def _validar_atributos(atributos: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(atributos, Mapping) or any(
            not isinstance(chave, str) for chave in atributos
        ):
            raise ValueError("custom_attributes deve ser objeto JSON com chaves string.")
        resultado = dict(atributos)
        try:
            json.dumps(resultado, allow_nan=False)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("custom_attributes deve conter JSON válido.") from exc
        return resultado

    @staticmethod
    def _validar_prioridade(prioridade: ConversationPriority | None) -> str | None:
        if prioridade is None:
            return None
        if not isinstance(prioridade, ConversationPriority):
            raise TypeError("priority deve ser ConversationPriority ou None.")
        return prioridade.value

    def list(
        self,
        account_id: int,
        *,
        assignee_type: str | None = None,
        status: str | None = None,
        q: str | None = None,
        inbox_id: int | None = None,
        team_id: int | None = None,
        labels: list[str] | None = None,
        page: int | None = None,
    ) -> dict[str, Any]:
        """GET lista, preservando o envelope {"data": {"meta":..., "payload":...}}."""
        self._client._validar_id(account_id, "account_id")
        consulta = self._consulta_conversas(
            status=status, q=q, inbox_id=inbox_id, team_id=team_id, labels=labels
        )
        if assignee_type is not None:
            if not isinstance(assignee_type, str) or assignee_type not in _FILTROS_ATENDENTE:
                raise ValueError("assignee_type deve ser me, unassigned, all ou assigned.")
            consulta["assignee_type"] = assignee_type
        if page is not None:
            self._client._validar_id(page, "page")
            consulta["page"] = page
        caminho = f"api/v1/accounts/{account_id}/conversations"
        resposta = self._client._get(caminho, parametros=consulta)
        return self._client._exigir_objeto(
            resposta, operacao="listar conversas", caminho=caminho
        )

    def get(self, account_id: int, conversation_id: int) -> dict[str, Any]:
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}"
        resposta = self._client._get(caminho)
        return self._client._exigir_objeto(
            resposta, operacao="consultar conversa", caminho=caminho
        )

    def meta(
        self,
        account_id: int,
        *,
        status: str | None = None,
        q: str | None = None,
        inbox_id: int | None = None,
        team_id: int | None = None,
        labels: list[str] | None = None,
    ) -> dict[str, Any]:
        self._client._validar_id(account_id, "account_id")
        consulta = self._consulta_conversas(
            status=status, q=q, inbox_id=inbox_id, team_id=team_id, labels=labels
        )
        caminho = f"api/v1/accounts/{account_id}/conversations/meta"
        resposta = self._client._get(caminho, parametros=consulta)
        return self._client._exigir_objeto(
            resposta, operacao="consultar totais de conversas", caminho=caminho
        )

    def filter(
        self,
        account_id: int,
        filters: Sequence[FilterCondition],
        *,
        page: int | None = None,
        sort_by: str | None = None,
    ) -> dict[str, Any]:
        self._client._validar_id(account_id, "account_id")
        dados = {"payload": _serializar_filtros(filters)}
        parametros: dict[str, Any] = {}
        if page is not None:
            self._client._validar_id(page, "page")
            parametros["page"] = page
        if sort_by is not None:
            if not isinstance(sort_by, str) or sort_by not in _ORDENACAO_FILTROS:
                raise ValueError("sort_by não é uma ordenação oficial de conversas.")
            parametros["sort_by"] = sort_by
        caminho = f"api/v1/accounts/{account_id}/conversations/filter"
        resposta = self._client._post(caminho, dados=dados, parametros=parametros)
        return self._client._exigir_objeto(
            resposta, operacao="filtrar conversas", caminho=caminho
        )

    def create(self, account_id: int, conversation: ConversationCreate) -> dict[str, Any]:
        """POST com contrato de entrada; retorna objeto JSON original."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(conversation, ConversationCreate):
            raise TypeError("conversation deve ser ConversationCreate.")
        caminho = f"api/v1/accounts/{account_id}/conversations"
        resposta = self._client._post(caminho, dados=conversation.to_payload())
        return self._client._exigir_objeto(
            resposta, operacao="criar conversa", caminho=caminho
        )

    def update(
        self,
        account_id: int,
        conversation_id: int,
        *,
        priority: ConversationPriority | None,
    ) -> dict[str, Any]:
        """PATCH: prioridade fornecida; None explícito remove prioridade."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        dados = {"priority": self._validar_prioridade(priority)}
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}"
        resposta = self._client._patch(caminho, dados=dados)
        return self._client._exigir_objeto(
            resposta, operacao="atualizar conversa", caminho=caminho
        )

    def set_status(
        self,
        account_id: int,
        conversation_id: int,
        status: ConversationStatus,
        *,
        snoozed_until: int | None = None,
    ) -> dict[str, Any]:
        """POST de estado explícito; preserva regra de handoff do AgentBot."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(status, ConversationStatus):
            raise TypeError("status deve ser ConversationStatus.")
        if snoozed_until is not None:
            if status is not ConversationStatus.SNOOZED:
                raise ValueError("snoozed_until só é válido quando status='snoozed'.")
            self._client._validar_id(snoozed_until, "snoozed_until")
        dados: dict[str, Any] = {"status": status.value}
        if snoozed_until is not None:
            dados["snoozed_until"] = snoozed_until
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status"
        resposta = self._client._post(caminho, dados=dados)
        return self._client._exigir_objeto(
            resposta, operacao="alterar status da conversa", caminho=caminho
        )

    def toggle_priority(
        self,
        account_id: int,
        conversation_id: int,
        *,
        priority: ConversationPriority | None = None,
    ) -> None:
        """POST: prioridade explícita ou None para limpar (API sem corpo)."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        dados = {"priority": self._validar_prioridade(priority)}
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_priority"
        return self._client._post(caminho, dados=dados)

    def set_typing_status(
        self,
        account_id: int,
        conversation_id: int,
        *,
        typing_status: Literal["on", "off"],
        is_private: bool = False,
    ) -> None:
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if typing_status not in ("on", "off") or not isinstance(typing_status, str):
            raise ValueError("typing_status deve ser 'on' ou 'off'.")
        if not isinstance(is_private, bool):
            raise ValueError("is_private deve ser bool.")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_typing_status"
        return self._client._post(
            caminho, dados={"typing_status": typing_status, "is_private": is_private}
        )

    def update_last_seen(self, account_id: int, conversation_id: int) -> dict[str, Any] | None:
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/update_last_seen"
        return self._client._post(caminho)

    def update_custom_attributes(
        self,
        account_id: int,
        conversation_id: int,
        *,
        custom_attributes: Mapping[str, Any],
        merge: bool = True,
    ) -> dict[str, Any]:
        """Por padrão mescla as chaves; merge=False substitui o hash inteiro."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(merge, bool):
            raise ValueError("merge deve ser bool.")
        dados = {"custom_attributes": self._validar_atributos(custom_attributes), "merge": merge}
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/custom_attributes"
        resposta = self._client._post(caminho, dados=dados)
        return self._client._exigir_objeto(
            resposta, operacao="atualizar atributos da conversa", caminho=caminho
        )

    def delete_custom_attributes(
        self, account_id: int, conversation_id: int, *, keys: Sequence[str],
    ) -> dict[str, Any]:
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if isinstance(keys, (str, bytes)) or not isinstance(keys, (list, tuple)) or not keys:
            raise ValueError("keys deve ser lista não vazia de nomes de atributos.")
        if any(not isinstance(k, str) or not k.strip() for k in keys):
            raise ValueError("keys deve conter somente textos não vazios.")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/destroy_custom_attributes"
        resposta = self._client._post(caminho, dados={"custom_attributes": list(keys)})
        return self._client._exigir_objeto(
            resposta, operacao="remover atributos da conversa", caminho=caminho
        )

    def reporting_events(self, account_id: int, conversation_id: int) -> Any:
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/reporting_events"
        return self._client._get(caminho)
