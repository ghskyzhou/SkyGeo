@echo off
setlocal

if "%~1"=="" (
    echo Usage: visualize ^<experiment^>
    exit /b 1
)

set "ROOT=%~dp0"

"%ROOT%venv\Scripts\python.exe" "%ROOT%tools\visualize\visualize.py" "%~1"

endlocal