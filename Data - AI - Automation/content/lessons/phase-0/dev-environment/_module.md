Every later phase, from pandas and Airflow to LLM apps and agents, runs on the same base: **Python**, an editor (**VS Code**), isolated project environments (**uv**) and a way to find bugs (the **debugger**). Set this up once, properly, and you'll avoid the "it works on my machine" problems that waste hours.

!!! tip "What you'll install"
    - **Python 3.14**: the current stable version. Python 3.15 is being released this month (October 2026). Wait until the libraries you need support it.
    - **VS Code** with the **Python** extension. It installs Pylance, Python Debugger and Python Environments automatically.
    - **uv**: one fast tool for Python versions, virtual environments and packages.

**By the end of this module you can:** create a project with its own environment, add and lock packages, run code from VS Code and the terminal, and track down a bug with breakpoints instead of guessing.
