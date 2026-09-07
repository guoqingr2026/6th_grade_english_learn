@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   PEP6 学习系统 — 发布打包
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
  echo [错误] 未检测到 Python，请先安装 Python 3.10+
  pause
  exit /b 1
)

echo [1/2] 生成版本清单与文件差异记录...
python scripts\release_pack.py
if errorlevel 1 (
  echo [错误] release_pack.py 执行失败
  pause
  exit /b 1
)

echo.
echo [2/2] 同步 release 运行包...
call "%~dp0sync-release.bat" nopause
if errorlevel 1 (
  echo [错误] sync-release 失败
  pause
  exit /b 1
)

echo.
echo ========================================
echo [全部完成]
echo   - VERSION / manifests / docs\VERSION_HISTORY.md 已更新
echo   - release\ 目录已同步
echo ========================================
pause
