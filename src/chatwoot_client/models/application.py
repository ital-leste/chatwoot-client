"""Contratos tipados de entrada da Application API Chatwoot 4.19.0.

Mantêm o JSON de saída inalterado. Campos ausentes não entram em PATCH;
None explícito só é aceito quando o esquema permite None.
"""
from __future__ import annotations
import json
from copy import deepcopy
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, fields
from typing import Any, ClassVar


class _Ausente:
    __slots__ = ()


AUSENTE = _Ausente()


def _validar_json(valor: Any, nome: str) -> Any:
    try:
        copia = deepcopy(valor)
        json.dumps(copia, allow_nan=False)
    except (TypeError, ValueError, OverflowError, RecursionError) as exc:
        raise ValueError(f"{nome} requer JSON válido.") from exc
    return copia


class _ContratoEntrada:
    """Serialização comum para dataclasses com campos declarados no Swagger."""
    def __post_init__(self) -> None:
        for campo in fields(self):
            valor = getattr(self, campo.name)
            if valor is AUSENTE:
                continue
            # Cópia defensiva já na construção para não reter entrada mutável.
            validado = self._validar_campo(campo, valor)
            if isinstance(validado, (dict, list)):
                object.__setattr__(self, campo.name, validado)

    @staticmethod
    def _validar_campo(campo: Any, valor: Any) -> Any:
        nome = campo.name
        meta = campo.metadata
        if valor is None:
            if meta.get("nullable"):
                return None
            raise ValueError(f"{nome} não admite None.")
        tipo = meta["tipo"]
        if tipo == "str":
            if not isinstance(valor, str):
                raise ValueError(f"{nome} deve ser string.")
            if meta.get("nao_vazio") and not valor.strip():
                raise ValueError(f"{nome} deve ser texto não vazio.")
        elif tipo == "int":
            if type(valor) is not int:
                raise ValueError(f"{nome} deve ser int.")
        elif tipo == "number":
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                raise ValueError(f"{nome} deve ser número.")
        elif tipo == "bool":
            if type(valor) is not bool:
                raise ValueError(f"{nome} deve ser bool.")
        elif tipo == "object":
            if not isinstance(valor, Mapping) or any(type(k) is not str for k in valor):
                raise ValueError(f"{nome} requer objeto com chaves string.")
            valor = dict(valor)
        elif tipo in ("array_str", "array_int", "array_obj"):
            if not isinstance(valor, (list, tuple)):
                raise ValueError(f"{nome} requer lista ou tupla.")
            if tipo == "array_str" and any(not isinstance(v, str) for v in valor):
                raise ValueError(f"{nome} requer textos.")
            if tipo == "array_int" and any(type(v) is not int for v in valor):
                raise ValueError(f"{nome} requer inteiros.")
            if tipo == "array_obj" and any(
                not isinstance(v, Mapping) or any(type(k) is not str for k in v)
                for v in valor
            ):
                raise ValueError(f"{nome} requer objetos JSON.")
            valor = list(valor)
        else:
            raise ValueError(f"Tipo não reconhecido no contrato: {tipo}.")
        opcoes = meta.get("enum")
        if opcoes is not None and valor not in opcoes:
            raise ValueError(f"{nome} não é uma opção documentada.")
        return _validar_json(valor, nome)

    def to_payload(self, *, required: Sequence[str] = ()) -> dict[str, Any]:
        dados = {}
        for campo in fields(self):
            valor = getattr(self, campo.name)
            if valor is not AUSENTE:
                dados[campo.name] = self._validar_campo(campo, valor)
        if not dados:
            raise ValueError("Contrato requer ao menos um campo informado.")
        faltantes = [nome for nome in required if nome not in dados]
        if faltantes:
            raise ValueError(f"Campos obrigatórios ausentes: {', '.join(faltantes)}.")
        return dados

@dataclass(frozen=True, slots=True, kw_only=True)
class AccountSettingsInput(_ContratoEntrada):
    """Entrada tipada para PATCH /api/v1/accounts/{account_id}."""
    name: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    locale: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    domain: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    support_email: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    auto_resolve_after: int | None | _Ausente = field(default=AUSENTE, metadata={"tipo": "int","nullable": True})
    auto_resolve_message: str | None | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nullable": True})
    auto_resolve_ignore_waiting: bool | None | _Ausente = field(default=AUSENTE, metadata={"tipo": "bool","nullable": True})
    industry: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    company_size: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    timezone: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})


@dataclass(frozen=True, slots=True, kw_only=True)
class AgentBotInput(_ContratoEntrada):
    """Entrada tipada para POST /api/v1/accounts/{account_id}/agent_bots."""
    name: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    description: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    outgoing_url: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    avatar: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    avatar_url: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    bot_type: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    bot_config: Mapping[str, Any] | _Ausente = field(default=AUSENTE, metadata={"tipo": "object"})


@dataclass(frozen=True, slots=True, kw_only=True)
class AutomationRuleInput(_ContratoEntrada):
    """Entrada tipada para POST /api/v1/accounts/{account_id}/automation_rules."""
    name: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    description: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    event_name: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True,"enum": ["conversation_created","conversation_updated","conversation_resolved","message_created"]})
    active: bool | _Ausente = field(default=AUSENTE, metadata={"tipo": "bool"})
    actions: Sequence[Mapping[str, Any]] | _Ausente = field(default=AUSENTE, metadata={"tipo": "array_obj"})
    conditions: Sequence[Mapping[str, Any]] | _Ausente = field(default=AUSENTE, metadata={"tipo": "array_obj"})


@dataclass(frozen=True, slots=True, kw_only=True)
class InboxSettingsInput(_ContratoEntrada):
    """Entrada tipada para POST /api/v1/accounts/{account_id}/inboxes."""
    name: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    avatar: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    greeting_enabled: bool | _Ausente = field(default=AUSENTE, metadata={"tipo": "bool"})
    greeting_message: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    enable_email_collect: bool | _Ausente = field(default=AUSENTE, metadata={"tipo": "bool"})
    csat_survey_enabled: bool | _Ausente = field(default=AUSENTE, metadata={"tipo": "bool"})
    csat_config: Mapping[str, Any] | _Ausente = field(default=AUSENTE, metadata={"tipo": "object"})
    enable_auto_assignment: bool | _Ausente = field(default=AUSENTE, metadata={"tipo": "bool"})
    working_hours_enabled: bool | _Ausente = field(default=AUSENTE, metadata={"tipo": "bool"})
    out_of_office_message: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    timezone: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    allow_messages_after_resolved: bool | _Ausente = field(default=AUSENTE, metadata={"tipo": "bool"})
    lock_to_single_conversation: bool | _Ausente = field(default=AUSENTE, metadata={"tipo": "bool"})
    portal_id: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    sender_name_type: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","enum": ["friendly","professional"]})
    business_name: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    channel: Mapping[str, Any] | _Ausente = field(default=AUSENTE, metadata={"tipo": "object"})


@dataclass(frozen=True, slots=True, kw_only=True)
class CustomAttributeInput(_ContratoEntrada):
    """Entrada tipada para POST /api/v1/accounts/{account_id}/custom_attribute_definitions."""
    attribute_display_name: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    attribute_display_type: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    attribute_description: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    attribute_key: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    attribute_values: Sequence[str] | _Ausente = field(default=AUSENTE, metadata={"tipo": "array_str"})
    attribute_model: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    regex_pattern: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    regex_cue: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})


@dataclass(frozen=True, slots=True, kw_only=True)
class CustomFilterInput(_ContratoEntrada):
    """Entrada tipada para POST /api/v1/accounts/{account_id}/custom_filters."""
    name: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    type: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","enum": ["conversation","contact","report"]})
    query: Mapping[str, Any] | _Ausente = field(default=AUSENTE, metadata={"tipo": "object"})


@dataclass(frozen=True, slots=True, kw_only=True)
class HelpCenterPortalInput(_ContratoEntrada):
    """Entrada tipada para POST /api/v1/accounts/{account_id}/portals."""
    color: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    custom_domain: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    header_text: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    homepage_link: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    name: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    page_title: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    slug: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    archived: bool | _Ausente = field(default=AUSENTE, metadata={"tipo": "bool"})
    config: Mapping[str, Any] | _Ausente = field(default=AUSENTE, metadata={"tipo": "object"})


@dataclass(frozen=True, slots=True, kw_only=True)
class HelpCenterCategoryInput(_ContratoEntrada):
    """Entrada tipada para POST /api/v1/accounts/{account_id}/portals/{id}/categories."""
    name: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    description: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    position: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    slug: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    locale: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    icon: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    parent_category_id: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    associated_category_id: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})


@dataclass(frozen=True, slots=True, kw_only=True)
class HelpCenterArticleInput(_ContratoEntrada):
    """Entrada tipada para POST /api/v1/accounts/{account_id}/portals/{id}/articles."""
    title: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    slug: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str","nao_vazio": True})
    position: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    content: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    description: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    category_id: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    author_id: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    associated_article_id: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    status: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    locale: str | _Ausente = field(default=AUSENTE, metadata={"tipo": "str"})
    meta: Mapping[str, Any] | _Ausente = field(default=AUSENTE, metadata={"tipo": "object"})


@dataclass(frozen=True, slots=True, kw_only=True)
class IntegrationHookInput(_ContratoEntrada):
    """Entrada tipada para POST /api/v1/accounts/{account_id}/integrations/hooks."""
    app_id: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    inbox_id: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    status: int | _Ausente = field(default=AUSENTE, metadata={"tipo": "int"})
    settings: Mapping[str, Any] | _Ausente = field(default=AUSENTE, metadata={"tipo": "object"})


