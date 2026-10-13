<div align="center">
  <h1>⚡ Nimbus Browser</h1>
  
  <h2>📥 DOWNLOAD LATEST VERSION</h2>
  <a href="https://github.com/tgferr/nimbusbrowser/releases/latest">
    <img src="https://img.shields.io/badge/Windows_10%2B-Download_.exe-0078D6?style=for-the-badge&logo=windows" alt="Download Windows" />
  </a>
  <a href="https://github.com/tgferr/nimbusbrowser/releases/latest">
    <img src="https://img.shields.io/badge/Linux_Debian-Download_.deb-A81D33?style=for-the-badge&logo=debian" alt="Download Debian" />
  </a>
  <a href="https://github.com/tgferr/nimbusbrowser/releases/latest">
    <img src="https://img.shields.io/badge/Linux_Ubuntu-Download_.AppImage-E95420?style=for-the-badge&logo=ubuntu" alt="Download Linux AppImage" />
  </a>
  <a href="https://github.com/tgferr/nimbusbrowser/releases/latest">
    <img src="https://img.shields.io/badge/Linux_Portable-Download_.tar.gz-6C757D?style=for-the-badge&logo=linux" alt="Download Tarball" />
  </a>
  <br>
  <i>Click the badges above and download the <b>.exe</b>, <b>.deb</b>, <b>.AppImage</b> or <b>.tar.gz</b> file under the <b>Assets</b> section.</i>
</div>

<br>

<p align="center">
  <img src="assets/nimbus_icon.ico" width="80" height="80" alt="Nimbus Browser Logo" />
</p>

<p align="center">
  <strong>A modern, privacy-focused, lightweight desktop web browser powered by Python and QtWebEngine (Chromium).</strong>
</p>

<p align="center">
  <a href="https://github.com/tgferr/nimbusbrowser/releases/latest">
    <img src="https://img.shields.io/github/v/release/tgferr/nimbusbrowser?color=0A84FF&label=Latest%20Release" alt="Latest Release" />
  </a>
  <a href="https://github.com/tgferr/nimbusbrowser/actions/workflows/release.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/tgferr/nimbusbrowser/release.yml?label=Build%20Status" alt="Build Status" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB.svg?logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/Qt-PySide6%206.12-41CD52.svg?logo=qt&logoColor=white" alt="PySide6" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg" alt="Platforms" />
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License" />
</p>

---

## ✨ Highlights & Features

- **Chromium-Powered Engine**: Built on top of PySide6 `QtWebEngineWidgets` for modern web standards, CSS3, WebGL, and high-performance JavaScript execution.
- **Glassmorphic Dark UI**: Custom-tailored dark theme inspired by macOS and Windows 11 aesthetics with subtle glow effects and rounded pill controls.
- **Chrome-Compliant Keyboard Shortcuts**: Seamless muscle memory support for `Ctrl+T`, `Ctrl+W`, `Ctrl+Shift+T`, `Ctrl+L`, `Ctrl+Tab`, and more.
- **Offline-First Dynamic Home Page**: Zero external dependencies to start. Features configurable Speed Dials with local persistence (`localStorage`), multiple search engines (Google, DuckDuckGo, Bing), and quick modal addition/removal.
- **Robust Tab Isolation & Lifecycle**: Clean architecture separating application shell, navigation controller, and individual tab views with leak-free disposal.
- **Continuous Integration & Auto-Packaging**: Automated GitHub Actions matrix generating certified Inno Setup Windows installers on every release tag.

---

## ⌨️ Keyboard Shortcuts

| Shortcut                             | Description                      |
| :----------------------------------- | :------------------------------- |
| `Ctrl + T`                           | Open new tab                     |
| `Ctrl + W` / `Ctrl + F4`             | Close active tab                 |
| `Ctrl + Shift + T`                   | Reopen last closed tab           |
| `Ctrl + L` / `Alt + D` / `F6`        | Focus and select URL address bar |
| `Ctrl + R` / `F5`                    | Reload page                      |
| `Ctrl + Shift + R` / `Ctrl + F5`     | Hard reload (bypass cache)       |
| `Ctrl + Tab` / `Ctrl + PgDown`       | Next tab                         |
| `Ctrl + Shift + Tab` / `Ctrl + PgUp` | Previous tab                     |
| `Ctrl + 1` to `Ctrl + 8`             | Jump to tab 1 through 8          |
| `Ctrl + 9`                           | Jump to last tab                 |
| `Alt + Left` / `Alt + Right`         | Navigate Back / Forward          |

---

## 🛠️ Developer Setup & Local Execution

### Prerequisites

- **Python 3.12+**
- `make` (optional, for automation tasks)
- Linux / Windows / macOS with graphics display

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/tgferr/nimbusbrowser.git
cd nimbusbrowser

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Browser

```bash
make run
# or directly via python:
PYTHONPATH=src python -m nimbus.main
```

### 3. Run Test Suite

```bash
make test
# or via pytest:
PYTHONPATH=src pytest tests/ -v
```

---

## 🏗️ Architecture & Project Structure

```text
nimbusbrowser/
├── .github/workflows/       # GitHub Actions CI/CD (release.yml)
├── .openspec/               # Specification-Driven Development (SDD) & Knowledge Base
│   ├── brain.md             # Nimbus Brain orchestrator and memory
│   ├── agents/              # Specialized Autonomous Subagents (Architect, QA, Security...)
│   └── templates/           # Delivery and MR templates
├── assets/                  # Icons, offline pages, and bundled home UI
│   ├── home.html            # Native offline-first glassmorphic home page
│   └── nimbus_icon.ico      # Application icon
├── installer/               # Inno Setup compilation script (nimbus.iss)
├── src/nimbus/
│   ├── core/                # Models, tab manager, domain rules & constants
│   ├── engine/              # QWebEngineView abstraction & async favicon client
│   ├── ui/                  # Main window, navigation bar & QSS dark theme
│   └── main.py              # Application entry point
├── tests/                   # Pytest & pytest-qt test suites
├── Makefile                 # Development task automation
└── nimbus.spec              # PyInstaller bundle specification
```

---

## 📦 Building the Windows Installer Locally

1. Install PyInstaller and Inno Setup 6.
2. Build the binary distribution:
   ```bash
   pyinstaller --noconfirm nimbus.spec
   ```
3. Compile the setup wizard:
   ```bash
   iscc installer/nimbus.iss
   ```
   The generated installer will be located in `dist-installer/`.

---

## 📄 License

This project is open-source and released under the [MIT License](LICENSE).
