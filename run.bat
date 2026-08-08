@echo off
setlocal

cd /d "%~dp0"

set "BUILD=0"
set "TARGET=test"

rem ------------------------------------------------------------
rem Parse arguments
rem ------------------------------------------------------------

if /I "%~1"=="-o" (
    set "BUILD=1"

    if not "%~2"=="" (
        set "TARGET=%~2"
    )
) else (
    if not "%~1"=="" (
        set "TARGET=%~1"
    )
)

rem ------------------------------------------------------------
rem Build if -o is specified
rem ------------------------------------------------------------

if "%BUILD%"=="1" (
    echo.
    echo ===== Configure =====
    cmake -S . -B build
    if errorlevel 1 exit /b 1

    echo.
    echo ===== Build %TARGET% =====
    cmake --build build --target "%TARGET%"
    if errorlevel 1 exit /b 1
)

rem ------------------------------------------------------------
rem Run
rem ------------------------------------------------------------

echo.
echo ===== Run %TARGET% =====
echo.

if not exist ".\build\%TARGET%.exe" (
    echo Error: build\%TARGET%.exe does not exist.
    echo Use:
    echo     run -o %TARGET%
    echo to build it first.
    exit /b 1
)

".\build\%TARGET%.exe"

endlocal