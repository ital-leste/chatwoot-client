"""Contratos de entrada para recursos selecionados."""
from .attachments import Attachment
from .messages import TextMessage, MediaMessage
from .labels import LabelDefinition
from .contacts import Contact
from .conversations import ConversationCreate
from .filters import FilterCondition

__all__ = ["Attachment", "TextMessage", "MediaMessage", "LabelDefinition", "Contact", "ConversationCreate", "FilterCondition",
    "ProfileInput", "AccountSettingsInput", "AgentBotInput", "AutomationRuleInput", "InboxSettingsInput", "CustomAttributeInput", "CustomFilterInput", "HelpCenterPortalInput", "HelpCenterCategoryInput", "HelpCenterArticleInput", "IntegrationHookInput",
]
from .application import AccountSettingsInput, AgentBotInput, AutomationRuleInput, InboxSettingsInput, CustomAttributeInput, CustomFilterInput, HelpCenterPortalInput, HelpCenterCategoryInput, HelpCenterArticleInput, IntegrationHookInput

from .application import ProfileInput
