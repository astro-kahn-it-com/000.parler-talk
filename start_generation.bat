@echo off
setlocal

:: Define the python command
set PYTHON_CMD=python

:: Check if Python is installed
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not added to your PATH.
    echo Please install Python and try again.
    pause
    exit /b 1
)

:: Define the virtual environment directory name
set VENV_DIR=venv

:: Check if the virtual environment directory already exists
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv "%VENV_DIR%"
)

:: Activate the virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

:: Check if the activation was successful
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Installing dependencies...
:: Upgrade pip first
python -m pip install --upgrade pip

:: Install torch with CUDA support
:: Note: The index-url here gets the appropriate wheels for PyTorch on Windows
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

:: Install transformers and soundfile
pip install transformers soundfile

:: Install parler-tts directly from the huggingface github repo
pip install git+https://github.com/huggingface/parler-tts.git

echo.
echo ==============================================
echo Dependencies installed/verified successfully.
echo Starting Generation Script...
echo ==============================================
echo.

:: Run the script
python generate.py

echo.
echo ==============================================
echo Generation Complete or Terminated with Errors.
echo ==============================================

:: Pause at the end to allow reading errors
pause
