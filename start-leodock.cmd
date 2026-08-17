@echo off
setlocal
cd /d "%~dp0"

where pyw.exe >nul 2>nul
if errorlevel 1 goto :missing_python

py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>nul
if errorlevel 1 goto :old_python

start "" pyw.exe -3 "%~dp0leodock.py" --launcher
exit /b 0

:missing_python
echo Error: Python 3 was not found. Install Python 3.12 or newer first.
echo https://www.python.org/downloads/windows/
pause
exit /b 127

:old_python
echo Error: LeoDock requires Python 3.12 or newer.
py -3 --version
pause
exit /b 126
