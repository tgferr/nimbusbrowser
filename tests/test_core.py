"""Testes unitários para o módulo core do Nimbus."""

import pytest
from nimbus.core.constants import DEFAULT_HOME_URL, normalize_input_url
from nimbus.core.tab_manager import TabManager


def test_normalize_input_url_empty():
    assert normalize_input_url("") == DEFAULT_HOME_URL
    assert normalize_input_url("   ") == DEFAULT_HOME_URL


def test_normalize_input_url_with_scheme():
    assert normalize_input_url("https://google.com") == "https://google.com"
    assert normalize_input_url("http://example.com") == "http://example.com"
    assert normalize_input_url("file:///tmp/test.html") == "file:///tmp/test.html"


def test_normalize_input_url_domain_without_scheme():
    assert normalize_input_url("github.com") == "https://github.com"
    assert normalize_input_url("sub.domain.org/path") == "https://sub.domain.org/path"


def test_normalize_input_url_search_query():
    assert normalize_input_url("python programming") == "https://duckduckgo.com/?q=python programming"
    assert normalize_input_url("o que e nimbus") == "https://duckduckgo.com/?q=o que e nimbus"


def test_tab_manager_lifecycle():
    manager = TabManager()
    assert manager.count() == 0
    assert manager.get_active_tab() is None

    # Adicionar 2 abas
    tab1 = manager.add_tab("https://tab1.com", "Tab 1")
    assert manager.count() == 1
    assert manager.get_active_tab().id == tab1.id

    tab2 = manager.add_tab("https://tab2.com", "Tab 2")
    assert manager.count() == 2
    assert manager.get_active_tab().id == tab2.id

    # Trocar ativa
    assert manager.set_active(tab1.id) is True
    assert manager.get_active_tab().id == tab1.id

    # Remover ativa
    next_active_id = manager.remove_tab(tab1.id)
    assert manager.count() == 1
    assert next_active_id == tab2.id
    assert manager.get_active_tab().id == tab2.id

    # Remover última
    last_id = manager.remove_tab(tab2.id)
    assert manager.count() == 0
    assert last_id is None
    assert manager.get_active_tab() is None
