@echo off

chcp 65001 >nul

cd /d "%~dp0"

set PY_CMD=

python --version >nul 2>&1 && set PY_CMD=python

if not defined PY_CMD py --version >nul 2>&1 && set PY_CMD=py

if not defined PY_CMD (

  echo [ERROR] 未找到 Python。请安装 Python 3.8+（含 3.12），并勾选 Add to PATH。

  pause

  exit /b 1

)

for /f "delims=" %%v in ('"%PY_CMD%" --version 2^>^&1') do echo 使用 %%v

echo 正在生成学生学习辅导手册（Word + PDF）...

"%PY_CMD%" scripts\generate_student_handbook.py

if %ERRORLEVEL% NEQ 0 (

  echo.

  echo 生成失败。请确认已安装 python-docx：pip install python-docx

  pause

  exit /b 1

)

echo.

echo 文件位置：docs\学生学习辅导手册.docx

echo            docs\学生学习辅导手册.pdf

echo.

start "" "docs"

pause

