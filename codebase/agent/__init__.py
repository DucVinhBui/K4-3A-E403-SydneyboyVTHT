"""Agent học trò — điểm gọi quyết định AI thay heuristic trong prototype.

Exposed API:
    - StateCheckAgent: lõi agent, gọi `.decide(text) -> Decision`
    - TeachingSession: state machine M1→M4, bao agent + log phiên
    - Decision, ProbeQuestion: output schema
    - Settings, load_settings: config runtime
"""

from .config import Settings, load_settings
from .core import StateCheckAgent
from .schema import Decision, ProbeQuestion
from .session import TeachingSession

__all__ = [
    "StateCheckAgent",
    "TeachingSession",
    "Decision",
    "ProbeQuestion",
    "Settings",
    "load_settings",
]
