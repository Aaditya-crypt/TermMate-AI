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
* 🛡️ **Safe Command Execution**: Safely execute whitelisted system commands (`git version`, `python version`, `ipconfig`, etc.) with user confirmation.
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

## 💬 Usage & Command Reference

Once launched, interact with TermMate using natural requests:

### 📁 Navigation & Inspection
| Request Prompt | Description |
| :--- | :--- |
| `Show me all files in this folder` | Lists all files and subdirectories |
| `Show folder sizes` | Shows file and folder sizes in readable units |
| `Where am I?` | Prints the absolute working directory path |
| `Find Python files` | Searches and lists all `.py` files |
| `Find file named <filename>` | Locates a specific file by name |

### 🛠️ Scaffolding & Code Generation
| Request Prompt | Description |
| :--- | :--- |
| `Create a Python calculator` | Creates a full terminal calculator in `TermMate_Workspace/` |
| `Make a Python file named <name>` | Creates a boilerplate `<name>.py` with a `main()` function |
| `Create a Python project named <name>` | Scaffolds a full starter project directory with standard files |
| `Create file named <name>` | Creates an empty text file |

### 🔍 System Diagnostics & Helpers
| Request Prompt | Description |
| :--- | :--- |
| `Check system health` | Displays OS, Python version, and disk capacity breakdown |
| `Explain <command>` | Explains commands like `mkdir`, `cd`, `git`, `pip`, etc. |
| `Run git version` | Checks the installed Git version with confirmation |
| `Show history` | Lists recent queries from `termmate_history.json` |
| `Clear screen` | Clears the terminal screen |
| `help` | Prints the interactive help menu |
| `exit` / `quit` | Exits the TermMate session |

---

## 📂 Project Structure

```text
TermMate-AI/
├── termmate.py               # Core application logic and command handlers
├── README.md                 # Project documentation
├── termmate_history.json     # Rolling log of user requests
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
