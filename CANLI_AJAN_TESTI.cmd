@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Once python tools/check_all.py --install komutunu calistirin.
  pause
  exit /b 2
)
".venv\Scripts\python.exe" tools\run_live_local.py
set "task_exit=%errorlevel%"
echo.
echo Tamamlandiginda bu sohbete "test bitti" yazabilirsiniz. Anahtari gondermeyin.
pause
exit /b %task_exit%
