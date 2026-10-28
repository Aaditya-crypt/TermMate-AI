\# TermMate AI



\*\*An offline, rule-based terminal assistant built with Python.\*\*



TermMate AI helps users perform common development and terminal tasks through simple natural-language requests. It runs locally and does not require an AI API key.



\## Features



\- \*\*List files and folders\*\* in the current directory.

\- \*\*View file sizes\*\* to understand how much space files use.

\- \*\*Search for files\*\* by name or pattern, including Python files.

\- \*\*Show the current working directory.\*\*

\- \*\*Display system information\*\*, including operating system, Python version, and disk usage.

\- \*\*Generate a Python calculator\*\* with addition, subtraction, multiplication, and division.

\- \*\*Create Python starter files\*\* with a basic `main()` function.

\- \*\*Create starter Python projects\*\* with `main.py`, `README.md`, and `requirements.txt`.

\- \*\*Explain common terminal commands\*\*, such as `mkdir`, `cd`, `python`, and `git`.

\- \*\*Keep a local request history\*\* of recent TermMate interactions.



\## Requirements



\- Windows, macOS, or Linux (some system commands are platform-specific).

\- Python 3.11 or newer recommended.

\- No third-party Python packages are required for the core prototype.



\## Run locally



1\. Install Python if it is not already installed.

2\. Open a terminal in the project directory.

3\. Start the application:



&#x20;  `py termmate.py`



&#x20;  If the `py` launcher is unavailable, try `python3 termmate.py`.



4\. Type `help` to see supported requests.

5\. Type `exit` to close TermMate AI.



\## Example requests



\- `Show me all files in this folder`

\- `Show folder sizes`

\- `Find Python files`

\- `Find file named main.py`

\- `Where am I?`

\- `Check system health`

\- `Create a Python calculator`

\- `Make a Python file named hello`

\- `Create a Python project named StudentManager`

\- `Explain mkdir`

\- `Run git version`

\- `Show history`



\## Safety



\- Generated files are saved in the `TermMate\_Workspace` folder.

\- TermMate asks for confirmation before creating files or running supported commands.

\- Existing files are not intentionally overwritten.

\- Only a small allowlist of terminal commands is supported; arbitrary shell commands are not executed.

\- Request history is stored locally in `termmate\_history.json`.



\*\*Limitations:\*\* This is an early rule-based prototype. It recognizes supported phrases rather than understanding every request like a large language model. System information and command support can vary by operating system.



\## Roadmap



\- Improve natural-language request matching.

\- Add more safe, permission-based file and folder operations.

\- Add automated tests for supported requests.

\- Improve cross-platform compatibility.

\- Improve error messages and logging.



\## License



No license has been specified yet. Unless a license is added, standard copyright applies; others do not automatically receive permission to reuse or redistribute this project.



