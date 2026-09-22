@echo off
set VENV_PYTHON="%~dp0.venv\Scripts\pythonw.exe"

start "" %VENV_PYTHON% "%~dp0main.py"
exit