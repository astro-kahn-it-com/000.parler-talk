@echo off
echo ==============================================
echo Parler-TTS Local Generation
echo ==============================================

if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment. Ensure Python is installed.
        pause
        exit /b %errorlevel%
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install transformers soundfile
pip install git+https://github.com/huggingface/parler-tts.git

echo.
echo Running generation script...
python generate.py

echo.
pause
