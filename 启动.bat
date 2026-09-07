@echo off
cd /d "%~dp0"
set PORT=8080
set PY_CMD=

rem Prefer "python" directly (works even when where.exe is missing from PATH)
python --version >nul 2>&1 && set PY_CMD=python
if not defined PY_CMD py --version >nul 2>&1 && set PY_CMD=py

echo ========================================
echo   PEP Grade 6 English Trainer
echo ========================================
echo.

if defined PY_CMD (
  for /f "delims=" %%v in ('"%PY_CMD%" --version 2^>^&1') do echo [OK] %%v
  echo.
  echo [1/4] Import cards...
  "%PY_CMD%" "%~dp0scripts\import-question-cards.py"
  if errorlevel 1 goto :error

  echo [2/4] Sync question banks...
  "%PY_CMD%" "%~dp0scripts\sync-question-banks.py"
  if errorlevel 1 goto :error

  echo [3/4] CSV import + build study-hub...
  "%PY_CMD%" "%~dp0scripts\import-word-study.py"
  "%PY_CMD%" "%~dp0scripts\import-csv-to-library.py"
  "%PY_CMD%" "%~dp0scripts\build-study-hub.py"
  if errorlevel 1 goto :error
  "%PY_CMD%" "%~dp0scripts\verify-textbook-images.py"
  if errorlevel 1 echo [WARN] Some textbook images missing; server will still start.
  echo.
) else (
  echo [WARN] Python not found. Using existing JSON banks only.
  echo.
)

echo [4/4] Starting server on port %PORT% ...
echo   Stopping old process on port %PORT% if any...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%PORT%" ^| findstr LISTENING') do (
  taskkill /F /PID %%a >nul 2>&1
)
timeout /t 1 /nobreak >nul
echo   Local:  http://localhost:%PORT%
echo   Local:  http://127.0.0.1:%PORT%
echo   LAN:    check ipconfig for your IPv4 address
echo   Example: http://192.168.1.8:%PORT%
echo   LAN sync: tap Sync Data button on PC and phone
echo.
echo Press Ctrl+C to stop the server.
echo.

if not defined PY_CMD goto :no_python

start "" "http://localhost:%PORT%"
"%PY_CMD%" "%~dp0scripts\lan_server.py" %PORT%
goto :eof

:no_python
echo [ERROR] Python 3 not found in PATH.
echo   Install Python 3.8+ from https://www.python.org/downloads/
echo   Python 3.12 is supported. Check "Add python.exe to PATH" during install.
echo   Or run manually: python scripts\lan_server.py %PORT%
pause
goto :eof

:error
echo.
echo [ERROR] Bank sync failed. Check data\question-banks\
pause
exit /b 1
