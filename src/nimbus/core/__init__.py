"""Exports do módulo core."""

from nimbus.core.constants import (
    ASSETS_DIR,
    BrowserConfig,
    DEFAULT_HOME_URL,
    ICON_PATH,
    NEW_TAB_URL,
    OFFLINE_HOME_PATH,
    normalize_input_url,
)
from nimbus.core.models import HistoryEntry, TabModel
from nimbus.core.tab_manager import TabManager

__all__ = [
    "BrowserConfig",
    "DEFAULT_HOME_URL",
    "NEW_TAB_URL",
    "ASSETS_DIR",
    "ICON_PATH",
    "OFFLINE_HOME_PATH",
    "normalize_input_url",
    "TabModel",
    "HistoryEntry",
    "TabManager",
]
