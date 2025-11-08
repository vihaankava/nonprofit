# Nonprofit Idea Coach - Windows Setup Guide

Complete setup instructions for Windows 10/11 users.

## Prerequisites

- Windows 10 or Windows 11
- Administrator access (for Python installation)

## Step-by-Step Installation

### Step 1: Install Python

1. **Download Python:**
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Click "Download Python 3.12.x" (or latest version)
   - Save the installer file

2. **Run the Installer:**
   - Double-click the downloaded `.exe` file
   - ⚠️ **IMPORTANT:** Check the box "Add Python to PATH"
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Installation:**
   - Open Command Prompt (press `Win + R`, type `cmd`, press Enter)
   - Type: `python --version`
   - You should see: `Python 3.12.x` or similar
   - If you see an error, restart your computer and try again

### Step 2: Download the Project

**Option A: Using Git (Recommended)**
1. Install Git from [git-scm.com](https://git-scm.com/download/win)
2. Open Command Prompt
3. Navigate to where you want the project:
   ```cmd
   cd C:\Users\YourUsername\Documents
   ```
4. Clone the repository:
   ```cmd
   git clone https://github.com/vihaankava/nonprofit.git
   cd nonprofit
   ```

**Option B: Download ZIP**
1. Go to [github.com/vihaankava/nonprofit](https://github.com/vihaankava/nonprofit)
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to a folder (e.g., `C:\Users\YourUsername\Documents\nonprofit`)
5. Open Command Prompt and navigate to the folder:
   ```cmd
   cd C:\Users\YourUsername\Documents\nonprofit
   ```

### Step 3: Set Up the Application

1. **Navigate to the nonprofit_coach folder:**
   ```cmd
   cd nonprofit_coach
   ```

2. **Create a Virtual Environment:**
   ```cmd
   python -m venv venv
   ```
   
   This creates a folder called `venv` that will contain all the Python packages.

3. **Activate the Virtual Environment:**
   ```cmd
   venv\Scripts\activate
   ```
   
   You should see `(venv)` appear at the beginning of your command prompt line.
   
   Example:
   ```
   (venv) C:\Users\YourUsername\Documents\nonprofit\nonprofit_coach>
   ```

4. **Install Required Packages:**
   ```cmd
   pip install -r requirements.txt
   ```
   
   This will install:
   - Flask (web framework)
   - Anthropic (AI integration)
   - python-dotenv (configuration)
   - requests (HTTP library)
   
   Wait for all packages to install (takes 1-2 minutes).

### Step 4: Configure API Keys

1. **Get an Anthropic API Key:**
   - Go to [console.anthropic.com](https://console.anthropic.com/)
   - Sign up or log in
   - Go to "API Keys"
   - Click "Create Key"
   - Copy your API key (starts with `sk-ant-`)

2. **Create Configuration File:**
   
   In the `nonprofit_coach` folder, you'll see a file called `.env.example`.
   
   **Option A: Using Notepad**
   ```cmd
   copy .env.example .env
   notepad .env
   ```
   
   **Option B: Using File Explorer**
   - Open File Explorer
   - Navigate to the `nonprofit_coach` folder
   - Right-click `.env.example`
   - Select "Copy"
   - Right-click in empty space
   - Select "Paste"
   - Rename the copy to `.env` (remove `.example`)
   - Right-click `.env` and open with Notepad

3. **Edit the Configuration:**
   
   Replace `your_api_key_here` with your actual API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   SECRET_KEY=change-this-to-something-random
   ```
   
   Optional - Enable web search (recommended):
   ```
   SEARCH_ENABLED=true
   SEARCH_PROVIDER=brave
   BRAVE_API_KEY=your-brave-api-key-here
   ```
   
   Save and close the file.

### Step 5: Run the Application

1. **Make sure your virtual environment is activated** (you should see `(venv)` in the prompt)

2. **Start the application:**
   ```cmd
   python app.py
   ```

3. **You should see:**
   ```
   * Running on http://127.0.0.1:5001
   * Press CTRL+C to quit
   ```

4. **Open your web browser:**
   - Go to: `http://localhost:5001`
   - Or: `http://127.0.0.1:5001`

5. **Start using the app!** 🎉

## Daily Usage

After the initial setup, here's how to use the app:

1. **Open Command Prompt**

2. **Navigate to the project:**
   ```cmd
   cd C:\Users\YourUsername\Documents\nonprofit\nonprofit_coach
   ```

3. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```

4. **Run the app:**
   ```cmd
   python app.py
   ```

5. **Open browser to:** `http://localhost:5001`

6. **When done, press `Ctrl+C` in Command Prompt to stop the server**

7. **Deactivate virtual environment:**
   ```cmd
   deactivate
   ```

## Quick Start Script

To make it easier, create a file called `start.bat` in the `nonprofit_coach` folder:

```batch
@echo off
echo Starting Nonprofit Idea Coach...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the application
echo Opening browser to http://localhost:5001
echo Press Ctrl+C to stop the server
echo.

REM Open browser after 2 seconds
timeout /t 2 /nobreak >nul
start http://localhost:5001

REM Run the app
python app.py

REM Deactivate when done
deactivate
```

Then just double-click `start.bat` to launch the app!

## Troubleshooting

### "Python is not recognized"

**Problem:** Command Prompt doesn't recognize `python` command.

**Solution:**
1. Reinstall Python and make sure to check "Add Python to PATH"
2. Or manually add Python to PATH:
   - Search for "Environment Variables" in Windows
   - Click "Environment Variables"
   - Under "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python312`
   - Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\Scripts`
   - Click OK on all windows
   - Restart Command Prompt

### "venv\Scripts\activate" not working

**Problem:** Virtual environment won't activate.

**Solution:**
1. Make sure you're in the `nonprofit_coach` folder
2. Try running as Administrator:
   - Right-click Command Prompt
   - Select "Run as administrator"
3. Or use PowerShell instead:
   ```powershell
   venv\Scripts\Activate.ps1
   ```

### "Cannot find .env file"

**Problem:** App can't find configuration.

**Solution:**
1. Make sure you created `.env` (not `.env.txt`)
2. In File Explorer, enable "File name extensions":
   - Click "View" tab
   - Check "File name extensions"
3. Rename the file to exactly `.env` with no extension

### Port 5001 Already in Use

**Problem:** Another program is using port 5001.

**Solution:**
1. Find what's using the port:
   ```cmd
   netstat -ano | findstr :5001
   ```
2. Kill that process:
   ```cmd
   taskkill /PID <process_id> /F
   ```
3. Or change the port in `app.py`:
   - Open `app.py` in Notepad
   - Find the last line: `app.run(debug=True, host='0.0.0.0', port=5001)`
   - Change `5001` to another number like `5002`
   - Save the file

### "Module not found" errors

**Problem:** Python can't find installed packages.

**Solution:**
1. Make sure virtual environment is activated (you see `(venv)`)
2. Reinstall packages:
   ```cmd
   pip install -r requirements.txt
   ```
3. If still not working, delete `venv` folder and start over:
   ```cmd
   rmdir /s venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Firewall Warnings

**Problem:** Windows Firewall blocks the app.

**Solution:**
1. Click "Allow access" when prompted
2. The app only runs locally on your computer
3. It's safe to allow

### Browser Doesn't Open Automatically

**Problem:** Browser doesn't open to the app.

**Solution:**
1. Manually open your browser
2. Type in the address bar: `http://localhost:5001`
3. Bookmark it for easy access

## Updating the Application

To get the latest version:

1. **If you used Git:**
   ```cmd
   cd C:\Users\YourUsername\Documents\nonprofit
   git pull
   cd nonprofit_coach
   venv\Scripts\activate
   pip install -r requirements.txt --upgrade
   ```

2. **If you downloaded ZIP:**
   - Download the new ZIP
   - Extract to a new folder
   - Copy your `.env` file from the old folder to the new one
   - Follow setup steps 3-5 again

## Uninstalling

To remove the application:

1. **Delete the project folder:**
   - Close the app (Ctrl+C in Command Prompt)
   - Delete the `nonprofit` folder

2. **Optional - Uninstall Python:**
   - Go to Settings > Apps
   - Find "Python 3.12.x"
   - Click "Uninstall"

## Getting Help

- **Documentation:** See `README.md` in the project folder
- **Issues:** Report bugs at [github.com/vihaankava/nonprofit/issues](https://github.com/vihaankava/nonprofit/issues)
- **API Help:** [docs.anthropic.com](https://docs.anthropic.com)

## Tips for Windows Users

1. **Use Windows Terminal** (better than Command Prompt):
   - Install from Microsoft Store
   - Supports tabs and better colors

2. **Pin Command Prompt to Taskbar:**
   - Right-click Command Prompt
   - Select "Pin to taskbar"

3. **Create Desktop Shortcut:**
   - Right-click `start.bat`
   - Select "Create shortcut"
   - Drag shortcut to Desktop

4. **Use VS Code** for editing files:
   - Free from [code.visualstudio.com](https://code.visualstudio.com)
   - Better than Notepad for code

---

**You're all set!** Enjoy building your nonprofit ideas! 🚀
