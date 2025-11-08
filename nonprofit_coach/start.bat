@echo off
REM Nonprofit Idea Coach - Windows Launcher
REM Double-click this file to start the application

echo ========================================
echo Nonprofit Idea Coach
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run setup first:
    echo 1. Open Command Prompt in this folder
    echo 2. Run: python -m venv venv
    echo 3. Run: venv\Scripts\activate
    echo 4. Run: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if packages are installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ERROR: Required packages not installed!
    echo.
    echo Installing packages now...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Installation failed. Please check your internet connection.
        pause
        exit /b 1
    )
)

echo.
echo Starting Nonprofit Idea Coach...
echo.
echo The application will open in your browser at:
echo http://localhost:5001
echo.
echo Press Ctrl+C to stop the server
echo.

REM Open browser after 2 seconds
timeout /t 2 /nobreak >nul
start http://localhost:5001

REM Run the application
python app.py

REM Deactivate when done
deactivate
