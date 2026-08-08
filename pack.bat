@echo off
setlocal

cd /d "%~dp0"

python tools\pack\pack.py %*

endlocal