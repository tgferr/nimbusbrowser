.PHONY: run test lint clean build-deb

SHELL := /bin/bash
VENV_BIN := .venv/bin
PYTHON := $(VENV_BIN)/python
PYTEST := $(VENV_BIN)/pytest
PYINSTALLER := $(VENV_BIN)/pyinstaller
VERSION := 1.0.0

# Executa o navegador Nimbus localmente
run:
	@export PYTHONPATH=src && $(PYTHON) -m nimbus.main

# Executa a suíte de testes unitários e de integração
test:
	@export PYTHONPATH=src && $(PYTEST) tests/ -v

# Compila o binário e empacota .deb localmente (apenas Linux)
build-deb:
	@echo "Compilando com PyInstaller..."
	@$(PYINSTALLER) --noconfirm nimbus.spec
	@echo "Montando estrutura do pacote Debian..."
	@mkdir -p DebDir/usr/lib/nimbus-browser
	@mkdir -p DebDir/usr/bin
	@mkdir -p DebDir/usr/share/applications
	@mkdir -p DebDir/usr/share/icons/hicolor/256x256/apps
	@mkdir -p DebDir/DEBIAN
	@cp -r dist/Nimbus/* DebDir/usr/lib/nimbus-browser/
	@ln -sf /usr/lib/nimbus-browser/Nimbus DebDir/usr/bin/nimbus-browser
	@echo "[Desktop Entry]" > DebDir/usr/share/applications/nimbus-browser.desktop
	@echo "Name=Nimbus Browser" >> DebDir/usr/share/applications/nimbus-browser.desktop
	@echo "Exec=nimbus-browser" >> DebDir/usr/share/applications/nimbus-browser.desktop
	@echo "Icon=nimbus-browser" >> DebDir/usr/share/applications/nimbus-browser.desktop
	@echo "Type=Application" >> DebDir/usr/share/applications/nimbus-browser.desktop
	@echo "Categories=Network;WebBrowser;" >> DebDir/usr/share/applications/nimbus-browser.desktop
	@convert assets/nimbus_icon.ico[0] DebDir/usr/share/icons/hicolor/256x256/apps/nimbus-browser.png || cp assets/nimbus_icon.ico DebDir/usr/share/icons/hicolor/256x256/apps/nimbus-browser.png
	@echo "Package: nimbus-browser" > DebDir/DEBIAN/control
	@echo "Version: $(VERSION)" >> DebDir/DEBIAN/control
	@echo "Section: web" >> DebDir/DEBIAN/control
	@echo "Priority: optional" >> DebDir/DEBIAN/control
	@echo "Architecture: amd64" >> DebDir/DEBIAN/control
	@echo "Maintainer: Nimbus Developer <dev@nimbus.local>" >> DebDir/DEBIAN/control
	@echo "Description: Nimbus Browser" >> DebDir/DEBIAN/control
	@echo " Navegador web moderno, focado em privacidade, feito em Python e QtWebEngine." >> DebDir/DEBIAN/control
	@mkdir -p dist-installer
	@echo "Gerando nimbus-browser-v$(VERSION)-amd64.deb..."
	@fakeroot dpkg-deb -Znone --build DebDir dist-installer/nimbus-browser-v$(VERSION)-amd64.deb
	@echo "Pacote gerado em: dist-installer/nimbus-browser-v$(VERSION)-amd64.deb"

# Limpeza de caches e arquivos transitórios
clean:
	@rm -rf .pytest_cache __pycache__ src/**/__pycache__ tests/__pycache__ build/ dist/ DebDir/ dist-installer/
