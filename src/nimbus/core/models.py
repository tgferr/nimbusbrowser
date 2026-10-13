"""Modelos de dados e entidades do navegador."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class TabModel:
    """Representa o estado de uma aba aberta."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    url: str = ""
    title: str = "Nova Aba"
    favicon_bytes: Optional[bytes] = None
    is_loading: bool = False
    can_go_back: bool = False
    can_go_forward: bool = False
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class HistoryEntry:
    """Entrada de histórico de navegação."""
    url: str
    title: str
    visited_at: datetime = field(default_factory=datetime.now)
