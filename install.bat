@echo off
echo ===================================
echo Retro MP3 Player Installer
echo ===================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in the PATH.
    echo Please install Python 3.9 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Checking Python version...
for /f "tokens=2" %%V in ('python --version 2^>^&1') do set PYTHON_VERSION=%%V
echo Found Python %PYTHON_VERSION%
echo.

echo Installing required packages...
pip install PyQt5 mutagen
if %errorlevel% neq 0 (
    echo Failed to install required packages. Please check your internet connection.
    pause
    exit /b 1
)

echo.
echo ===================================
echo Installation complete!
echo.
echo To run the Retro MP3 Player, use one of the following options:
echo 1. Double-click the run.bat file
echo 2. Open command prompt and run: python main.py
echo ===================================
echo.

REM Create a run.bat file for easy launching
echo @echo off > run.bat
echo python main.py >> run.bat

pause