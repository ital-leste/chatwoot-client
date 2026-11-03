"""Transporte HTTP comum e ponto de composição dos recursos do Chatwoot."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any, BinaryIO
from urllib.parse import urlsplit

import httpx

from .account import AccountResource
from .agents import AgentsResource
from .contacts import ContactsResource
from .conversations import ConversationsResource
from .conversation_assignments import ConversationAssignmentsResource
from .conversation_labels import ConversationLabelsResource
from .inboxes import InboxesResource
from .labels import LabelsResource
from .messages import MessagesResource
from .profile import ProfileResource
from .transport import executar
from .audit_logs import AuditLogsResource
from .account_agentbots import AccountAgentBotsResource
from .canned_responses import CannedResponsesResource
from .custom_attributes import CustomAttributesResource
from .contact_labels import ContactLabelsResource
from .automation_rules import AutomationRulesResource
from .help_center import HelpCenterResource
from .integrations import IntegrationsResource
from .teams import TeamsResource
from .custom_filters import CustomFiltersResource
from .webhooks import WebhooksResource
from .reports import ReportsResource
from .campaigns import CampaignsResource


class ErroConfiguracaoChatwoot(ValueError):
    """Configuração ausente ou inválida para a API do Chatwoot."""


class ErroAPIChatwoot(RuntimeError):
    """Falha de transporte, HTTP ou formato na API do Chatwoot."""

    def __init__(
        self,
        mensagem: str,
        *,
        caminho: str,
        status_http: int | None = None,
    ) -> None:
        super().__init__(mensagem)
        self.caminho = caminho
        self.status_http = status_http


class CWClient:
    """Client HTTP da API Chatwoot com respostas JSON sem modelos externos.

    ``api_token`` é o token de acesso pessoal do perfil de usuário.
    O endereço e o token são fornecidos pelo código que instancia o client.

    As operações por recurso ficam em módulos separados. O client expõe
    consultas e escritas explícitas, preservando integralmente o JSON da API.
    """

    def __init__(
        self, base_url: str, api_token: str, timeout: float = 30.0,
        *, auth_mode: str = "bearer",
    ) -> None:
        if not isinstance(base_url, str) or not base_url.strip():
            raise ErroConfiguracaoChatwoot("base_url deve ser URL http(s) não vazia.")
        base_url = base_url.strip().rstrip("/")
        partes_url = urlsplit(base_url)
        if (
            partes_url.scheme not in {"http", "https"}
            or not partes_url.netloc
            or partes_url.username is not None
            or partes_url.password is not None
            or partes_url.query
            or partes_url.fragment
        ):
            raise ErroConfiguracaoChatwoot(
                "base_url deve ser uma URL http(s) sem credenciais, "
                "query ou fragmento."
            )
        if not isinstance(api_token, str) or not api_token.strip():
            raise ErroConfiguracaoChatwoot("api_token é obrigatório.")
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
            raise ErroConfiguracaoChatwoot(
                "timeout deve ser um número positivo."
            )
        if auth_mode not in {"bearer", "api_access_token"}:
            raise ErroConfiguracaoChatwoot("auth_mode inválido.")
        self._base_path = partes_url.path.strip("/")
        base_url_raiz = f"{partes_url.scheme}://{partes_url.netloc}/"
        self._http = httpx.Client(
            base_url=base_url_raiz,
            headers=(
                {"Authorization": f"Bearer {api_token.strip()}"}
                if auth_mode == "bearer"
                else {"api_access_token": api_token.strip()}
            ),
            timeout=timeout,
        )

        self.account: AccountResource = AccountResource(self)
        self.agents: AgentsResource = AgentsResource(self)
        self.contacts: ContactsResource = ContactsResource(self)
        self.inboxes: InboxesResource = InboxesResource(self)
        self.profile: ProfileResource = ProfileResource(self)
        self.conversations: ConversationsResource = ConversationsResource(self)
        self.conversation_labels: ConversationLabelsResource = ConversationLabelsResource(self)
        self.conversation_assignments: ConversationAssignmentsResource = ConversationAssignmentsResource(self)
        self.labels: LabelsResource = LabelsResource(self)
        self.messages: MessagesResource = MessagesResource(self)
        self.audit_logs: AuditLogsResource = AuditLogsResource(self)
        self.account_agentbots: AccountAgentBotsResource = AccountAgentBotsResource(self)
        self.canned_responses: CannedResponsesResource = CannedResponsesResource(self)
        self.custom_attributes: CustomAttributesResource = CustomAttributesResource(self)
        self.contact_labels: ContactLabelsResource = ContactLabelsResource(self)
        self.automation_rules: AutomationRulesResource = AutomationRulesResource(self)
        self.help_center: HelpCenterResource = HelpCenterResource(self)
        self.integrations: IntegrationsResource = IntegrationsResource(self)
        self.teams: TeamsResource = TeamsResource(self)
        self.custom_filters: CustomFiltersResource = CustomFiltersResource(self)
        self.webhooks: WebhooksResource = WebhooksResource(self)
        self.reports: ReportsResource = ReportsResource(self)
        self.campaigns: CampaignsResource = CampaignsResource(self)

    @staticmethod
    def _validar_id(valor: int, nome: str) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise ValueError(f"{nome} deve ser um inteiro positivo.")

    @staticmethod
    def _segmento(valor: str | int, nome: str) -> str:
        """Protege segmentos textuais de caminhos da API."""
        from urllib.parse import quote
        if isinstance(valor, bool) or not isinstance(valor, (str, int)):
            raise ValueError(f"{nome} deve ser texto ou inteiro.")
        if not str(valor).strip():
            raise ValueError(f"{nome} não pode ser vazio.")
        return quote(str(valor), safe="")

    def _request(
        self,
        metodo: str,
        caminho: str,
        *,
        dados: Mapping[str, Any] | None = None,
        parametros: Mapping[str, Any] | None = None,
        arquivos: Sequence[tuple[str, tuple[str, bytes | BinaryIO, str]]] | None = None,
        formulario: Mapping[str, Any] | None = None,
    ) -> Any:
        """Único caminho de execução HTTP, sem retry automático.

        As operações por recurso não precisam conhecer httpx ou autenticação.
        """
        try:
            resposta = executar(
                self._http, self._base_path, metodo, caminho,
                dados=dados, parametros=parametros, arquivos=arquivos,
                formulario=formulario,
            )
        except httpx.RequestError:
            raise ErroAPIChatwoot(
                f"Falha de conexão ao chamar {metodo} {caminho}.",
                caminho=caminho,
            ) from None
        try:
            resposta.raise_for_status()
        except httpx.HTTPStatusError as erro:
            status = erro.response.status_code
            raise ErroAPIChatwoot(
                f"Chatwoot respondeu HTTP {status} para {metodo} {caminho}.",
                caminho=caminho, status_http=status,
            ) from None
        if resposta.status_code == 204 or not resposta.content:
            return None
        try:
            return resposta.json()
        except ValueError:
            raise ErroAPIChatwoot(
                f"Chatwoot retornou JSON inválido para {metodo} {caminho}.",
                caminho=caminho, status_http=resposta.status_code,
            ) from None

    def _get(self, caminho: str, **kwargs: Any) -> Any:
        return self._request("GET", caminho, **kwargs)

    def _post(self, caminho: str, **kwargs: Any) -> Any:
        return self._request("POST", caminho, **kwargs)

    def _put(self, caminho: str, **kwargs: Any) -> Any:
        return self._request("PUT", caminho, **kwargs)

    def _patch(self, caminho: str, **kwargs: Any) -> Any:
        return self._request("PATCH", caminho, **kwargs)

    def _delete(self, caminho: str, **kwargs: Any) -> Any:
        return self._request("DELETE", caminho, **kwargs)

    def _solicitar_json(
        self,
        metodo: str,
        caminho: str,
        *,
        dados: Mapping[str, Any] | None = None,
        parametros: Mapping[str, Any] | None = None,
        arquivos: Sequence[tuple[str, tuple[str, bytes | BinaryIO, str]]] | None = None,
        formulario: Mapping[str, Any] | None = None,
    ) -> Any:
        """Adaptador retrocompatível para os recursos existentes."""
        return self._request(
            metodo, caminho, dados=dados, parametros=parametros,
            arquivos=arquivos, formulario=formulario,
        )

    @staticmethod
    def _exigir_objeto(
        resposta: Any,
        *,
        operacao: str,
        caminho: str,
    ) -> dict[str, Any]:
        if not isinstance(resposta, dict):
            raise ErroAPIChatwoot(
                f"Resposta inesperada ao {operacao}: era esperado um objeto JSON.",
                caminho=caminho,
            )
        return resposta

    @staticmethod
    def _exigir_lista(
        resposta: Any,
        *,
        operacao: str,
        caminho: str,
    ) -> list[Any]:
        if not isinstance(resposta, list):
            raise ErroAPIChatwoot(
                f"Resposta inesperada ao {operacao}: era esperada uma lista JSON.",
                caminho=caminho,
            )
        return resposta

    def close(self) -> None:
        """Libera a sessão HTTP mantida pelo cliente."""
        self._http.close()

    def __enter__(self) -> "CWClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
