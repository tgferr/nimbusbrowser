"""Gerenciamento de abas e ciclo de vida."""

from typing import Dict, List, Optional
from nimbus.core.models import TabModel


class TabManager:
    """Controla a lista e o estado lógico das abas ativas."""

    def __init__(self) -> None:
        self._tabs: Dict[str, TabModel] = {}
        self._order: List[str] = []
        self._active_tab_id: Optional[str] = None

    def add_tab(self, url: str = "", title: str = "Nova Aba") -> TabModel:
        """Cria e registra uma nova aba lógica."""
        tab = TabModel(url=url, title=title)
        self._tabs[tab.id] = tab
        self._order.append(tab.id)
        self._active_tab_id = tab.id
        return tab

    def remove_tab(self, tab_id: str) -> Optional[str]:
        """
        Remove a aba especificada.
        Retorna o id da próxima aba recomendada para ativação ou None se vazia.
        """
        if tab_id not in self._tabs:
            return self._active_tab_id

        idx = self._order.index(tab_id)
        self._order.remove(tab_id)
        del self._tabs[tab_id]

        if not self._order:
            self._active_tab_id = None
            return None

        # Se removeu a ativa, ajusta para a vizinha mais próxima
        if self._active_tab_id == tab_id:
            next_idx = min(idx, len(self._order) - 1)
            self._active_tab_id = self._order[next_idx]

        return self._active_tab_id

    def set_active(self, tab_id: str) -> bool:
        """Define a aba ativa."""
        if tab_id in self._tabs:
            self._active_tab_id = tab_id
            return True
        return False

    def get_tab(self, tab_id: str) -> Optional[TabModel]:
        """Obtém uma aba por ID."""
        return self._tabs.get(tab_id)

    def get_active_tab(self) -> Optional[TabModel]:
        """Retorna a aba atualmente ativa."""
        if self._active_tab_id:
            return self._tabs.get(self._active_tab_id)
        return None

    def count(self) -> int:
        """Quantidade de abas abertas."""
        return len(self._order)

    @property
    def tab_ids(self) -> List[str]:
        """Lista ordenada de IDs das abas."""
        return list(self._order)
