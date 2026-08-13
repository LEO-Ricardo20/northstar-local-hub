@echo off
setlocal
cd /d "%~dp0"

where py.exe >nul 2>nul
if errorlevel 1 (
  echo Error: Python 3 was not found. Install Python 3.12 or newer first.
  echo https://www.python.org/downloads/windows/
  pause
  exit /b 127
)

py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)"
if errorlevel 1 (
  echo Error: Console requires Python 3.12 or newer.
  py -3 --version
  pause
  exit /b 126
)

py -3 server.py --launcher
if errorlevel 1 pause
