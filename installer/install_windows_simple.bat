@echo off
REM Simple Windows Installer for Nonprofit Idea Coach
REM This installer checks for Python and creates a virtual environment

echo ========================================
echo Nonprofit Idea Coach - Simple Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed on this system.
    echo.
    echo Would you like to download Python now?
    echo.
    echo Press any key to open the Python download page...
    pause >nul
    start https://www.python.org/downloads/
    echo.
    echo After installing Python:
    echo 1. Restart this installer
    echo 2. Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Create installation directory
set INSTALL_DIR=%USERPROFILE%\NonprofitIdeaCoach
echo Installing to: %INSTALL_DIR%
echo.

if exist "%INSTALL_DIR%" (
    echo Installation directory already exists.
    echo Do you want to reinstall? This will delete the existing installation.
    choice /C YN /M "Continue"
    if errorlevel 2 exit /b 0
    rmdir /s /q "%INSTALL_DIR%"
)

mkdir "%INSTALL_DIR%"
cd "%INSTALL_DIR%"

echo Step 1: Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo.
echo Step 2: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 3: Copying application files...
xcopy /E /I /Y "%~dp0..\nonprofit_coach" "%INSTALL_DIR%\nonprofit_coach"

echo.
echo Step 4: Installing dependencies...
pip install -r nonprofit_coach\requirements.txt

echo.
echo Step 5: Creating launcher...
(
echo @echo off
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo echo.
echo echo ========================================
echo echo Nonprofit Idea Coach
echo echo ========================================
echo echo.
echo echo Starting server...
echo echo The application will open at: http://localhost:5001
echo echo.
echo echo Press Ctrl+C to stop the server
echo echo.
echo timeout /t 2 /nobreak ^>nul
echo start http://localhost:5001
echo cd nonprofit_coach
echo python app.py
echo pause
) > "%INSTALL_DIR%\Start Nonprofit Idea Coach.bat"

echo.
echo Step 6: Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Nonprofit Idea Coach.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\Start Nonprofit Idea Coach.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"

echo.
echo Step 7: Setting up configuration...
if not exist "%INSTALL_DIR%\nonprofit_coach\.env" (
    copy "%INSTALL_DIR%\nonprofit_coach\.env.example" "%INSTALL_DIR%\nonprofit_coach\.env"
    echo Configuration file created at: nonprofit_coach\.env
    echo You can edit this file to add your API keys.
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo The application has been installed to:
echo %INSTALL_DIR%
echo.
echo To start the application:
echo 1. Double-click the desktop shortcut "Nonprofit Idea Coach"
echo    OR
echo 2. Run: "%INSTALL_DIR%\Start Nonprofit Idea Coach.bat"
echo.
echo To configure API keys:
echo Edit: %INSTALL_DIR%\nonprofit_coach\.env
echo.
echo Press any key to start the application now...
pause >nul

start "" "%INSTALL_DIR%\Start Nonprofit Idea Coach.bat"
