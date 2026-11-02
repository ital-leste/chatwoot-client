"""Client HTTP próprio para as operações necessárias da API Chatwoot."""

from .client import CWClient, ErroAPIChatwoot, ErroConfiguracaoChatwoot

__all__ = [
    "CWClient",
    "ErroAPIChatwoot",
    "ErroConfiguracaoChatwoot",
]
