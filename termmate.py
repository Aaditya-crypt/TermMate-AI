
import datetime
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

APP_NAME = "TermMate AI"
VERSION = "3.0"

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE = BASE_DIR / "TermMate_Workspace"
HISTORY_FILE = BASE_DIR / "termmate_history.json"


# 1. Confirmation and safety
def confirm(title, details):
    print("\n" + "=" * 55)
    print("PREVIEW:", title)
    print("-" * 55)
    print(details)
    print("-" * 55)
    return input("Proceed? Type Y to approve: ").strip().lower() == "y"


# 2. Request history
def record(request):
    try:
        history = []
        if HISTORY_FILE.exists():
            history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        if not isinstance(history, list):
            history = []

        history.append(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}  {request}"
        )
        HISTORY_FILE.write_text(
            json.dumps(history[-100:], indent=2),
            encoding="utf-8"
        )
    except (OSError, ValueError):
        pass


def show_history():
    try:
        if not HISTORY_FILE.exists():
            print("No history available yet.")
            return

        history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        if not history:
            print("No history available yet.")
            return

        print("\n--- Recent Requests ---")
        for item in history[-20:]:
            print(item)
    except (OSError, ValueError):
        print("Could not read request history.")


def format_size(size_bytes):
    for unit in ["bytes", "KB", "MB", "GB"]:
        if size_bytes < 1024.0 or unit == "GB":
            if unit == "bytes":
                return f"{size_bytes} {unit}"
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} GB"


# 3. List files and folders
def list_files(show_sizes=False):
    folder = Path.cwd()
    print(f"\nContents of: {folder}")

    try:
        items = sorted(
            folder.iterdir(),
            key=lambda item: (not item.is_dir(), item.name.lower())
        )

        if not items:
            print("This folder is empty.")
            return

        for item in items:
            if item.is_dir():
                print(f"[DIR]  {item.name}")
            elif show_sizes:
                try:
                    size = format_size(item.stat().st_size)
                    print(f"[FILE] {item.name} - {size}")
                except OSError:
                    print(f"[FILE] {item.name} - size unavailable")
            else:
                print(f"[FILE] {item.name}")

    except OSError as error:
        print("Could not list files:", error)


# 4. Find files
def find_files(pattern):
    if not pattern or any(char in pattern for char in "/\\"):
        print("Enter a filename or a pattern such as *.py.")
        return

    roots = [Path.cwd(), WORKSPACE]
    ignored = {".git", ".venv", "venv", "node_modules", "__pycache__"}
    found = set()

    print(f"\nSearching for: {pattern}")

    for root in roots:
        if not root.is_dir():
            continue
        try:
            for path in root.rglob(pattern):
                if any(part.lower() in ignored for part in path.parts):
                    continue
                found.add(path)
                if len(found) >= 100:
                    break
        except OSError:
            continue

    if found:
        for path in sorted(found, key=lambda p: str(p).lower()):
            print(path)
    else:
        print("No matching files found.")


# 5. Create safe filenames
def safe_name(name):
    name = name.strip().strip('"').strip("'")

    if (
        not name
        or name in {".", ".."}
        or any(char in name for char in '/\\<>:"|?*')
        or name.endswith((" ", "."))
        or any(ord(char) < 32 for char in name)
    ):
        return None

    return name


def write_new_file(name, content, description):
    name = safe_name(name)

    if not name:
        print("Invalid filename. Use a simple filename without folder paths.")
        return

    WORKSPACE.mkdir(parents=True, exist_ok=True)
    destination = WORKSPACE / name

    if destination.exists():
        print("Cancelled: this file or folder already exists.")
        print("TermMate will not overwrite existing items.")
        return

    preview = (
        f"Destination: {destination}\n\n"
        f"Description: {description}\n\n"
        f"Content preview:\n{content[:1000]}"
    )

    if not confirm("Create new file", preview):
        print("Cancelled. Nothing was created.")
        return

    try:
        # Exclusive creation prevents accidentally overwriting a file.
        with destination.open("x", encoding="utf-8") as file:
            file.write(content)
        print("Created successfully:", destination)
    except OSError as error:
        print("Could not create file:", error)


# 6. Create Python starter files and calculators
def make_python_file(name, calculator=False):
    name = safe_name(name)

    if not name:
        print("Please provide a simple filename.")
        return

    if not name.lower().endswith(".py"):
        name += ".py"

    if calculator:
        code = '''def main():
    print("TermMate Python Calculator")
    print("Operations: +, -, *, /")

    try:
        first = float(input("Enter first number: "))
        operator = input("Enter operation: ").strip()
        second = float(input("Enter second number: "))

        if operator == "+":
            result = first + second
        elif operator == "-":
            result = first - second
        elif operator == "*":
            result = first * second
        elif operator == "/":
            if second == 0:
                print("Error: Cannot divide by zero.")
                return
            result = first / second
        else:
            print("Unsupported operation.")
            return

        print("Result:", result)

    except ValueError:
        print("Please enter valid numbers.")

if __name__ == "__main__":
    main()
'''
    else:
        code = '''def main():
    print("Hello from TermMate AI!")

if __name__ == "__main__":
    main()
'''

    write_new_file(
        name,
        code,
        "Create a Python calculator" if calculator
        else "Create a Python starter file"
    )


# 7. Create a starter Python project
def create_project(name):
    name = safe_name(name)

    if not name:
        print("Use a simple project name without folder paths.")
        return

    WORKSPACE.mkdir(parents=True, exist_ok=True)
    folder = WORKSPACE / name

    if folder.exists():
        print("Cancelled: this project already exists.")
        return

    files = {
        "main.py": (
            'def main():\n'
            '    print("Hello from your Python project!")\n\n'
            'if __name__ == "__main__":\n'
            '    main()\n'
        ),
        "README.md": (
            f"# {name}\n\n"
            "Python project created by TermMate AI.\n\n"
            "Run with: `py main.py`\n"
        ),
        "requirements.txt": "# Add required packages here.\n"
    }

    preview = (
        f"Project: {folder}\n"
        "Files to create:\n"
        + "\n".join(f"  - {filename}" for filename in files)
    )

    if not confirm("Create Python project", preview):
        print("Cancelled.")
        return

    try:
        folder.mkdir()
        for filename, content in files.items():
            (folder / filename).write_text(content, encoding="utf-8")
        print("Project created:", folder)
    except OSError as error:
        print("Project creation failed:", error)


# 8. Display system information
def system_health():
    print("\n--- System Information ---")
    print("Operating system:", platform.platform())
    print("Python version:", platform.python_version())
    print("Current directory:", Path.cwd())

    try:
        disk = shutil.disk_usage(Path.cwd().anchor or Path.cwd())
        print(f"Disk total: {disk.total // (1024**3)} GB")
        print(f"Disk used:  {disk.used // (1024**3)} GB")
        print(f"Disk free:  {disk.free // (1024**3)} GB")
    except OSError as error:
        print("Disk information unavailable:", error)

    print("--------------------------")


# 9. Explain common terminal commands
def explain_command(request):
    word = request.strip().lower().split()[0] if request.strip() else ""

    explanations = {
        "dir": "Lists files and folders on Windows.",
        "ls": "Lists files and folders; PowerShell also supports dir.",
        "cd": "Changes the current directory.",
        "pwd": "Displays the current working directory.",
        "mkdir": "Creates a new directory.",
        "del": "Deletes files. Check the target carefully before using it.",
        "rmdir": "Removes directories. Check the target carefully.",
        "python": "Runs Python or a Python script.",
        "py": "The Windows Python launcher.",
        "pip": "Installs or manages Python packages.",
        "git": "Tracks code changes with version control.",
        "ipconfig": "Displays Windows network configuration."
    }

    print(explanations.get(word, f"No explanation is available for {request!r}."))


# 10. Run only explicitly supported commands
def run_safe_command(request):
    key = request.strip().lower()

    # Cross-platform safe command mappings
    is_windows = os.name == "nt"
    
    if key in {"dir", "ls"}:
        command = ["cmd", "/c", "dir"] if is_windows else ["ls", "-la"]
    elif key == "pwd":
        command = ["powershell", "-NoProfile", "-Command", "Get-Location"] if is_windows else ["pwd"]
    elif key in {"python version", "check python version"}:
        command = [sys.executable, "--version"]
    elif key in {"git version", "check git version"}:
        command = ["git", "--version"]
    elif key in {"ipconfig", "ifconfig", "ip", "network info"}:
        if is_windows:
            command = ["ipconfig"]
        else:
            # On macOS and Linux, ifconfig provides interface details
            command = ["ifconfig"]
    else:
        command = None

    if command is None:
        print("Blocked: this command is not on the approved list.")
        print("Supported: dir, ls, pwd, python version, git version, ipconfig/ifconfig")
        return

    if not confirm("Run supported command", f"Command: {key} ({' '.join(command)})"):
        print("Cancelled.")
        return

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15,
            check=False
        )
        print(result.stdout or "(No output)")
        if result.stderr:
            print(result.stderr)
        print("Exit code:", result.returncode)
    except (OSError, subprocess.TimeoutExpired) as error:
        print("Command failed:", error)


def help_text():
    print("""
TermMate AI v3.0 — Available Requests

1.  Show me all files in this folder
2.  Show folder sizes
3.  Find Python files
4.  Find file named report.csv
5.  Where am I?
6.  Check system health
7.  Create a Python calculator
8.  Make a Python file named hello
9.  Create a Python project named StudentManager
10. Explain mkdir
11. Run git version
12. Run ipconfig
13. Show history
14. Clear screen
15. Help
16. Exit

Created files are stored in TermMate_Workspace.
TermMate does not overwrite existing files.
Writes and supported commands require confirmation.
Arbitrary shell commands are not executed.
""")


def handle_request(request):
    text = request.strip()
    if not text:
        return True

    record(text)

    # Normalize: lower case and strip trailing punctuation (?, !, ., etc.)
    lower = text.lower()
    cleaned = re.sub(r"[?!.,;:]+$", "", lower).strip()

    if cleaned in {"exit", "quit", "bye", "goodbye"}:
        print("TermMate: See you later, buddy!")
        return False

    elif cleaned in {"help", "commands", "features", "what can you do"}:
        help_text()

    elif (
        cleaned in {"list files", "show files", "ls", "dir",
                    "show folder contents", "show all files",
                    "list all files", "show me all files in this folder",
                    "show me all the files in this folder",
                    "show all files in this folder"}
        or ("show" in cleaned and "files" in cleaned and
            ("folder" in cleaned or "directory" in cleaned))
        or ("list" in cleaned and "files" in cleaned)
    ):
        list_files()

    elif cleaned in {"show folder sizes", "show file sizes",
                     "list files with sizes", "show sizes", "folder sizes"}:
        list_files(show_sizes=True)

    elif cleaned in {"where am i", "where ami", "pwd", "current folder",
                     "show current directory", "current path", "show path", "where am i?"}:
        print("Current directory:", Path.cwd())

    elif cleaned in {"check system health", "system health",
                     "system info", "check my computer", "system status"}:
        system_health()

    elif cleaned in {"find python files", "find all python files",
                     "find .py files", "show python files"}:
        find_files("*.py")

    elif cleaned.startswith("find file named "):
        find_files(cleaned[len("find file named "):].strip())

    elif cleaned.startswith("find files named "):
        find_files(cleaned[len("find files named "):].strip())

    elif cleaned in {"create a python calculator", "make a python calculator",
                     "create calculator", "create a calculator", "make calculator"}:
        make_python_file("calculator.py", calculator=True)

    elif cleaned.startswith("make a python file named ") or \
            cleaned.startswith("make python file named "):
        prefix = ("make a python file named "
                  if cleaned.startswith("make a python file named ")
                  else "make python file named ")
        name = text[len(prefix):].rstrip("?!.,:;").strip()
        make_python_file(name)

    elif cleaned.startswith("create a python project named ") or \
            cleaned.startswith("create project named "):
        prefix = ("create a python project named "
                  if cleaned.startswith("create a python project named ")
                  else "create project named ")
        name = text[len(prefix):].rstrip("?!.,:;").strip()
        create_project(name)

    elif cleaned.startswith("explain "):
        explain_command(cleaned[len("explain "):])

    elif cleaned.startswith("run "):
        run_safe_command(cleaned[4:])

    elif cleaned in {"check python version", "python version"}:
        run_safe_command("python version")

    elif cleaned in {"check git version", "git version"}:
        run_safe_command("git version")

    elif cleaned in {"show history", "history", "view history"}:
        show_history()

    elif cleaned in {"clear screen", "clear", "cls", "clear terminal"}:
        if confirm("Clear screen", "Only the visible terminal screen will be cleared."):
            os.system("cls" if os.name == "nt" else "clear")

    elif cleaned.startswith("make file named ") or \
            cleaned.startswith("create file named "):
        prefix = ("make file named " if cleaned.startswith("make file named ")
                  else "create file named ")
        name = text[len(prefix):].rstrip("?!.,:;").strip()
        if not Path(name).suffix:
            name += ".txt"
        write_new_file(name, "", "Create empty text file")

    else:
        print("I don't recognize that request yet.")
        print("Type help to see supported requests.")

    return True


def main():
    WORKSPACE.mkdir(parents=True, exist_ok=True)

    print("=" * 58)
    print(f"  {APP_NAME} v{VERSION}")
    print("  Offline | Rule-based | No API required")
    print("=" * 58)
    print("Type help for examples, or exit to quit.")
    print("Workspace:", WORKSPACE)

    while True:
        try:
            if not handle_request(input("\nYou > ")):
                break
        except (KeyboardInterrupt, EOFError):
            print("\nTermMate session ended.")
            break
        except Exception as error:
            print(f"TermMate caught an unexpected error: {error}")
            print("Your session can continue. Please report this error.")


if __name__ == "__main__":
    main()
