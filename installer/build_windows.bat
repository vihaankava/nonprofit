@echo off
REM Windows Installer Build Script for Nonprofit Idea Coach
REM This script creates a standalone Windows installer with Python embedded

echo ========================================
echo Nonprofit Idea Coach - Windows Installer Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Step 1: Installing build dependencies...
python -m pip install --upgrade pip
python -m pip install pyinstaller requests

echo.
echo Step 2: Installing application dependencies...
cd ..
python -m pip install -r nonprofit_coach/requirements.txt

echo.
echo Step 3: Creating standalone executable...
pyinstaller --clean --noconfirm ^
    --name "NonprofitIdeaCoach" ^
    --onefile ^
    --console ^
    --add-data "nonprofit_coach/templates;templates" ^
    --add-data "nonprofit_coach/static;static" ^
    --add-data "nonprofit_coach/.env.example;." ^
    --add-data "nonprofit_coach/README.md;." ^
    --hidden-import "anthropic" ^
    --hidden-import "flask" ^
    --hidden-import "dotenv" ^
    --hidden-import "sqlite3" ^
    --hidden-import "gunicorn" ^
    --hidden-import "nonprofit_coach.search_providers.brave" ^
    --hidden-import "nonprofit_coach.search_providers.base" ^
    --collect-all "anthropic" ^
    --collect-all "flask" ^
    nonprofit_coach/app.py

echo.
echo Step 4: Creating installer package...
cd installer
if not exist "dist\windows" mkdir dist\windows

REM Copy executable
copy ..\dist\NonprofitIdeaCoach.exe dist\windows\

REM Create launcher script
echo @echo off > dist\windows\start.bat
echo echo Starting Nonprofit Idea Coach... >> dist\windows\start.bat
echo echo. >> dist\windows\start.bat
echo echo The application will open in your web browser at http://localhost:5001 >> dist\windows\start.bat
echo echo. >> dist\windows\start.bat
echo echo Press Ctrl+C to stop the server >> dist\windows\start.bat
echo echo. >> dist\windows\start.bat
echo start http://localhost:5001 >> dist\windows\start.bat
echo NonprofitIdeaCoach.exe >> dist\windows\start.bat

REM Copy configuration files
copy ..\nonprofit_coach\.env.example dist\windows\.env.example
copy ..\nonprofit_coach\README.md dist\windows\README.md

REM Create setup instructions
echo # Nonprofit Idea Coach - Windows Installation > dist\windows\INSTALL.txt
echo. >> dist\windows\INSTALL.txt
echo ## Quick Start >> dist\windows\INSTALL.txt
echo. >> dist\windows\INSTALL.txt
echo 1. Double-click "start.bat" to launch the application >> dist\windows\INSTALL.txt
echo 2. The application will open in your web browser >> dist\windows\INSTALL.txt
echo 3. Follow the on-screen instructions >> dist\windows\INSTALL.txt
echo. >> dist\windows\INSTALL.txt
echo ## Configuration (Optional) >> dist\windows\INSTALL.txt
echo. >> dist\windows\INSTALL.txt
echo To configure API keys and settings: >> dist\windows\INSTALL.txt
echo 1. Copy ".env.example" to ".env" >> dist\windows\INSTALL.txt
echo 2. Edit ".env" with your API keys >> dist\windows\INSTALL.txt
echo 3. Restart the application >> dist\windows\INSTALL.txt
echo. >> dist\windows\INSTALL.txt
echo ## Requirements >> dist\windows\INSTALL.txt
echo. >> dist\windows\INSTALL.txt
echo - Windows 10 or later >> dist\windows\INSTALL.txt
echo - Internet connection >> dist\windows\INSTALL.txt
echo - Anthropic API key (can be entered in the app) >> dist\windows\INSTALL.txt
echo. >> dist\windows\INSTALL.txt
echo For more information, see README.md >> dist\windows\INSTALL.txt

echo.
echo Step 5: Creating ZIP archive...
cd dist\windows
powershell Compress-Archive -Path * -DestinationPath ..\NonprofitIdeaCoach-Windows-v1.0.0.zip -Force
cd ..\..

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Installer package created at:
echo installer\dist\NonprofitIdeaCoach-Windows-v1.0.0.zip
echo.
echo To distribute:
echo 1. Share the ZIP file
echo 2. Users extract and run "start.bat"
echo.
pause
