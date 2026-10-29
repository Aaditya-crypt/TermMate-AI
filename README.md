# ⚡ TermMate AI

> **A lightweight, offline, rule-based terminal assistant built with pure Python.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#requirements)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20External-orange.svg)](#requirements)

TermMate AI simplifies day-to-day terminal navigation, file inspection, and Python project scaffolding through intuitive, natural-language prompts. It operates **100% locally and offline** without requiring expensive LLM APIs, cloud connections, or third-party dependencies.

---

## 📌 Key Features

* 📂 **File & Directory Management**: List files, inspect file/folder sizes, and display the current working directory.
* 🔍 **Smart File Search**: Search files by name, extension, or pattern (e.g., locate all `.py` files).
* 🖥️ **System Health Monitor**: View OS platform info, active Python version, and real-time disk storage metrics (Used/Free/Total).
* ⚙️ **Code & Project Scaffolding**:
  * Generate a fully working Python terminal calculator (`calculator.py`).
  * Create starter Python files with standard `main()` boilerplate.
  * Scaffold structured Python projects (`main.py`, `README.md`, `requirements.txt`).
* 📖 **Command Dictionary**: Explain common terminal commands (`mkdir`, `cd`, `pip`, `git`, etc.) in simple terms.
* 🛡️ **Safe Command Execution**: Safely execute whitelisted system commands (`git version`, `python version`, `ipconfig/ifconfig`, etc.) with user confirmation.
* 📜 **Persistent Session History**: Automatically maintains a rolling history of your last 100 requests in `termmate_history.json`.

---

## 🔒 Security & Safety Architecture

TermMate AI is built with safety as a priority to prevent accidental data loss:

* **Isolated Workspace**: All generated files and scaffolded projects are confined to the `TermMate_Workspace/` directory.
* **Explicit User Confirmation**: Actions that create files, modify workspace structure, or invoke shell commands require explicit approval (`Y/N`).
* **Overwrite Protection**: TermMate uses exclusive file creation modes (`'x'`) and never silently overwrites existing files.
* **Strict Command Whitelisting**: Arbitrary shell execution is blocked; only pre-approved, non-destructive diagnostic commands can be run.

---

## 📋 Requirements

* **Operating System**: macOS, Linux, or Windows
* **Python**: Python 3.11 or newer recommended
* **Dependencies**: **None** (Built strictly using Python's standard library: `pathlib`, `shutil`, `subprocess`, `platform`, `json`, etc.)

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Aaditya-crypt/TermMate-AI.git
cd TermMate-AI
```

### 2. Launch TermMate AI
* **macOS / Linux**:
  ```bash
  python3 termmate.py
  ```
* **Windows**:
  ```cmd
  py termmate.py
  # or
  python termmate.py
  ```

---

## 💻 Commands, Live Outputs & Internal Explanations

Here is the complete reference of supported natural-language commands along with real execution outputs and how each feature works internally under the hood.

### 1. Current Working Directory
* **Prompt**: `Where am I?` / `where ami?` / `pwd`
* **Output**:
  ```text
  Current directory: /Users/shivam/Desktop/ITM /Linux git/1/TermMate-AI
  ```
* **Internal Explanation**:
  * Uses Python's standard `pathlib.Path.cwd()` method to fetch the absolute path of the current working directory.
  * Replaces the need to remember OS-specific commands (`pwd` on Linux/macOS or `cd` on Windows).

---

### 2. File & Directory Inspection
* **Prompt**: `Show me all files in this folder`
* **Output**:
  ```text
  Contents of: /Users/shivam/Desktop/ITM /Linux git/1/TermMate-AI
  [DIR]  .git
  [DIR]  TermMate_Workspace
  [FILE] .gitignore
  [FILE] README.md
  [FILE] termmate.py
  [FILE] termmate_history.json
  ```
* **Internal Explanation**:
  * Scans current directory using `Path.cwd().iterdir()`.
  * Sorts items alphabetically while placing directories (`[DIR]`) first, followed by files (`[FILE]`).

---

### 3. File Sizes in Human-Readable Units
* **Prompt**: `Show folder sizes`
* **Output**:
  ```text
  Contents of: /Users/shivam/Desktop/ITM /Linux git/1/TermMate-AI
  [DIR]  .git
  [DIR]  TermMate_Workspace
  [FILE] .gitignore - 259 bytes
  [FILE] README.md - 5.3 KB
  [FILE] termmate.py - 16.1 KB
  [FILE] termmate_history.json - 1.1 KB
  ```
* **Internal Explanation**:
  * Extracts raw file sizes using `item.stat().st_size`.
  * Automatically converts raw byte counts into human-readable units (`bytes`, `KB`, `MB`, `GB`) for quick inspection.

---

### 4. Recursive File Search
* **Prompt**: `Find Python files` or `Find file named hello.py`
* **Output**:
  ```text
  Searching for: *.py
  /Users/shivam/Desktop/ITM /Linux git/1/TermMate-AI/termmate.py
  /Users/shivam/Desktop/ITM /Linux git/1/TermMate-AI/TermMate_Workspace/hello.py
  ```
* **Internal Explanation**:
  * Recursively traverses subdirectories using `Path.rglob()`.
  * Skips internal/dependency directories like `.git`, `node_modules`, `venv`, and `__pycache__` to keep results clean and fast.

---

### 5. System Health & Storage Metrics
* **Prompt**: `Check system health`
* **Output**:
  ```text
  --- System Information ---
  Operating system: macOS-26.5.1-arm64-arm-64bit-Mach-O
  Python version: 3.15.0rc2
  Current directory: /Users/shivam/Desktop/ITM /Linux git/1/TermMate-AI
  Disk total: 460 GB
  Disk used:  141 GB
  Disk free:  319 GB
  --------------------------
  ```
* **Internal Explanation**:
  * **OS & Hardware**: Detected via `platform.platform()`.
  * **Python Environment**: Retrieved using `platform.python_version()`.
  * **Storage Health**: Evaluated via `shutil.disk_usage()`, converted from bytes to gigabytes ($GB = \text{bytes} / 1024^3$).

---

### 6. Automated Code Generation & Scaffolding
* **Prompt**: `Create a Python calculator`
* **Output**:
  ```text
  =======================================================
  PREVIEW: Create new file
  -------------------------------------------------------
  Destination: .../TermMate_Workspace/calculator.py
  Description: Create a Python calculator
  ...
  Proceed? Type Y to approve: y
  Created successfully: .../TermMate_Workspace/calculator.py
  ```
* **Internal Explanation**:
  * Generates a fully working CLI calculator script with basic arithmetic and zero-division handling.
  * **Safe Isolation**: Saves strictly to `TermMate_Workspace/`.
  * **Overwrite Protection**: Uses Python's exclusive file mode (`'x'`). If a file with the same name already exists, creation is safely cancelled.

---

### 7. Project Structure Scaffolding
* **Prompt**: `Create a Python project named StudentManager`
* **Output**:
  ```text
  =======================================================
  PREVIEW: Create Python project
  -------------------------------------------------------
  Project: .../TermMate_Workspace/StudentManager
  Files to create:
    - main.py
    - README.md
    - requirements.txt
  -------------------------------------------------------
  Proceed? Type Y to approve: y
  Project created: .../TermMate_Workspace/StudentManager
  ```
* **Internal Explanation**:
  * Scaffolds a complete starter repository directory containing standard entry-point (`main.py`), project documentation (`README.md`), and dependency manifest (`requirements.txt`).

---

### 8. Terminal Command Dictionary
* **Prompt**: `Explain mkdir`
* **Output**:
  ```text
  Creates a new directory.
  ```
* **Internal Explanation**:
  * Built-in dictionary mapping standard shell commands (`mkdir`, `cd`, `ls`, `git`, `pip`, `pwd`, etc.) to concise, beginner-friendly explanations.

---

### 9. Cross-Platform Whitelisted Diagnostics
* **Prompt**: `Run git version` / `Run ipconfig`
* **Output** (macOS example):
  ```text
  =======================================================
  PREVIEW: Run supported command
  -------------------------------------------------------
  Command: ipconfig (ifconfig)
  -------------------------------------------------------
  Proceed? Type Y to approve: y
  en0: flags=8863<UP,BROADCAST,SMART,RUNNING> mtu 1500
          inet 10.154.32.63 netmask 0xffffff00 broadcast 10.154.32.255
          ...
  Exit code: 0
  ```
* **Internal Explanation**:
  * Runs pre-approved diagnostic commands safely using `subprocess.run()`.
  * **Cross-Platform Compatibility**: Automatically adapts commands between Windows (`ipconfig`, `cmd dir`) and macOS/Linux (`ifconfig`, `ls -la`).

---

## 📂 Project Structure

```text
TermMate-AI/
├── termmate.py               # Core application logic and command handlers
├── README.md                 # Project documentation & reference
├── termmate_history.json     # Rolling log of user requests (last 100 entries)
└── TermMate_Workspace/       # Safe output directory for generated files & projects
```

---

## 🗺️ Roadmap

- [ ] Fuzzy matching and regex-based NLP for broader query tolerance.
- [ ] Optional local LLM integration (e.g., via Ollama) for advanced queries.
- [ ] Cross-platform safe file deletion/trash-bin integration.
- [ ] Comprehensive unit and integration test suite (`pytest`).

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
