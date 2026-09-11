@echo off
setlocal enabledelayedexpansion

REM ====================================================
REM  000.parler-talk : Standalone Generation Launcher
REM ====================================================

REM Resolve the root project directory (with trailing backslash)
set "SCRIPT_DIR=%~dp0"

REM ----------------------------------------------------
REM 1. DIRECTORY CONTAINMENT (ISOLATION GUARDS)
REM ----------------------------------------------------
REM Lock all temporary files, pip caches, and model downloads locally
set "TEMP=%SCRIPT_DIR%cache\temp"
set "TMP=%SCRIPT_DIR%cache\temp"
set "PIP_CACHE_DIR=%SCRIPT_DIR%cache\pip"
set "HF_HOME=%SCRIPT_DIR%models"
set "HUGGINGFACE_HUB_CACHE=%SCRIPT_DIR%models"

REM Create local containment folders if they do not exist
if not exist "%SCRIPT_DIR%cache\temp" mkdir "%SCRIPT_DIR%cache\temp"
if not exist "%SCRIPT_DIR%cache\pip" mkdir "%SCRIPT_DIR%cache\pip"
if not exist "%SCRIPT_DIR%models" mkdir "%SCRIPT_DIR%models"
if not exist "%SCRIPT_DIR%output" mkdir "%SCRIPT_DIR%output"

REM ----------------------------------------------------
REM 2. PYTHON RUNTIME TARGETING
REM ----------------------------------------------------
REM Point directly to the shared embedded Python executable
set "PYTHON_EXE=%SCRIPT_DIR%ComfyUI_windows_portable\python_embeded\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Embedded Python executable not found at:
    echo "%PYTHON_EXE%"
    echo.
    echo Please ensure the 'python_embeded' directory is placed inside 'ComfyUI_windows_portable'.
    echo.
    pause
    exit /b 1
)

REM ----------------------------------------------------
REM 3. SCRIPT EXECUTION
REM ----------------------------------------------------
set "SCRIPT_FILE=%SCRIPT_DIR%generate.py"

if not exist "%SCRIPT_FILE%" (
    echo [ERROR] Target generation script not found at:
    echo "%SCRIPT_FILE%"
    echo.
    pause
    exit /b 1
)

echo [INFO] Starting Parler-TTS standalone generation...
echo [INFO] Python Engine : "%PYTHON_EXE%"
echo [INFO] Model Storage : "%HF_HOME%"
echo [INFO] Output Folder : "%SCRIPT_DIR%output"
echo ----------------------------------------------------

REM Execute the Python script
"%PYTHON_EXE%" "%SCRIPT_FILE%"

echo ----------------------------------------------------
echo [INFO] Process completed.
echo.
pause