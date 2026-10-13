.PHONY: run test lint clean

SHELL := /bin/bash
VENV_BIN := .venv/bin
PYTHON := $(VENV_BIN)/python
PYTEST := $(VENV_BIN)/pytest

# Executa o navegador Nimbus localmente
run:
	@export PYTHONPATH=src && $(PYTHON) -m nimbus.main

# Executa a suíte de testes unitários e de integração
test:
	@export PYTHONPATH=src && $(PYTEST) tests/ -v

# Limpeza de caches e arquivos transitórios
clean:
	@rm -rf .pytest_cache __pycache__ src/**/__pycache__ tests/__pycache__
