@echo off
setlocal
set "PYTHONPATH=%~dp0src;%PYTHONPATH%"
if exist "%~dp0.venv\Scripts\python.exe" (
  "%~dp0.venv\Scripts\python.exe" -m gpower_clone %*
) else (
  python -m gpower_clone %*
)
exit /b %ERRORLEVEL%
