# Nonprofit Idea Coach - Installer Build Guide

This directory contains everything needed to create distributable installers for Windows and macOS that work on machines without Python installed.

## 📦 Quick Start

### Windows
```cmd
cd installer
build_windows.bat
```
Output: `dist/NonprofitIdeaCoach-Windows-v1.0.0.zip`

### macOS
```bash
cd installer
./build_mac.sh
```
Output: `dist/NonprofitIdeaCoach-macOS-v1.0.0.dmg`

## 📚 Documentation

- **[INSTALLER_SUMMARY.md](INSTALLER_SUMMARY.md)** - Complete overview of what's included
- **[USER_QUICK_START.md](USER_QUICK_START.md)** - End user installation guide
- **[../DISTRIBUTION_GUIDE.md](../DISTRIBUTION_GUIDE.md)** - Distribution strategy and comparison

---

This directory contains scripts to build standalone installers for Windows and macOS that include Python and all dependencies.

## Overview

The build process creates self-contained installers that:
- Bundle Python runtime (no Python installation required on target machine)
- Include all Python dependencies (Flask, Anthropic, etc.)
- Package all application files (templates, static assets, etc.)
- Create easy-to-use launcher scripts
- Include configuration templates

## Prerequisites for Building

### Windows
- Windows 10 or later
- Python 3.8 or higher installed
- Administrator privileges (for some operations)

### macOS
- macOS 10.13 or later
- Python 3.8 or higher installed
- Xcode Command Line Tools (for DMG creation)

## Building Installers

### Windows Installer

1. Open Command Prompt or PowerShell
2. Navigate to the installer directory:
   ```cmd
   cd installer
   ```
3. Run the build script:
   ```cmd
   build_windows.bat
   ```
4. Wait for the build to complete (5-10 minutes)
5. Find the installer at: `installer/dist/NonprofitIdeaCoach-Windows-v1.0.0.zip`

### macOS Installer

1. Open Terminal
2. Navigate to the installer directory:
   ```bash
   cd installer
   ```
3. Run the build script:
   ```bash
   ./build_mac.sh
   ```
4. Wait for the build to complete (5-10 minutes)
5. Find the installers at:
   - `installer/dist/NonprofitIdeaCoach-macOS-v1.0.0.dmg`
   - `installer/dist/NonprofitIdeaCoach-macOS-v1.0.0.zip`

## What Gets Built

### Windows Package Contents
```
NonprofitIdeaCoach-Windows-v1.0.0.zip
├── NonprofitIdeaCoach.exe    # Standalone executable
├── start.bat                  # Easy launcher script
├── .env.example              # Configuration template
├── README.md                 # Application documentation
└── INSTALL.txt               # Installation instructions
```

### macOS Package Contents
```
NonprofitIdeaCoach-macOS-v1.0.0.dmg (or .zip)
├── NonprofitIdeaCoach        # Standalone executable
├── start.command             # Easy launcher script
├── .env.example              # Configuration template
├── README.md                 # Application documentation
└── INSTALL.txt               # Installation instructions
```

## Distribution

### For Windows Users
1. Share the ZIP file
2. Users extract the ZIP to any folder
3. Users double-click `start.bat` to launch
4. Application opens in their default web browser

### For macOS Users
1. Share the DMG or ZIP file
2. Users open the DMG (or extract ZIP)
3. Users double-click `start.command` to launch
4. If security warning appears, users right-click and select "Open"
5. Application opens in their default web browser

## End User Requirements

### Windows
- Windows 10 or later
- Internet connection
- Web browser (Chrome, Firefox, Edge, Safari)
- Anthropic API key (can be entered in the app or configured in .env)

### macOS
- macOS 10.13 (High Sierra) or later
- Internet connection
- Web browser (Chrome, Firefox, Safari)
- Anthropic API key (can be entered in the app or configured in .env)

## Configuration

Users can configure the application by:

1. **In-App Configuration** (Recommended for beginners):
   - Launch the application
   - Enter API key when prompted
   - Optionally save API key for future sessions

2. **Environment File** (Recommended for advanced users):
   - Copy `.env.example` to `.env`
   - Edit `.env` with a text editor
   - Add API keys and customize settings
   - Restart the application

## Troubleshooting Build Issues

### Windows

**Issue**: "Python is not installed or not in PATH"
- **Solution**: Install Python from python.org and ensure "Add to PATH" is checked

**Issue**: "pyinstaller: command not found"
- **Solution**: Run `python -m pip install pyinstaller`

**Issue**: Build fails with import errors
- **Solution**: Ensure all dependencies are installed: `pip install -r ../nonprofit_coach/requirements.txt`

### macOS

**Issue**: "command not found: python3"
- **Solution**: Install Python from python.org or using Homebrew: `brew install python3`

**Issue**: "Permission denied"
- **Solution**: Make script executable: `chmod +x build_mac.sh`

**Issue**: DMG creation fails
- **Solution**: Install Xcode Command Line Tools: `xcode-select --install`

**Issue**: Build fails with import errors
- **Solution**: Ensure all dependencies are installed: `pip3 install -r ../nonprofit_coach/requirements.txt`

## Advanced Options

### Custom Build Names

Edit the build scripts to change version numbers or app names:

**Windows** (`build_windows.bat`):
```batch
--name "YourAppName"
```

**macOS** (`build_mac.sh`):
```bash
--name "YourAppName"
```

### Adding Additional Files

To include additional files in the installer, add them to the `--add-data` flags:

**Windows**:
```batch
--add-data "path/to/file;destination"
```

**macOS**:
```bash
--add-data "path/to/file:destination"
```

### Optimizing Build Size

To reduce the installer size:
1. Remove unused dependencies from `requirements.txt`
2. Add `--exclude-module` flags for unused Python modules
3. Use UPX compression (already enabled)

## Testing the Installer

Before distributing:

1. **Test on a clean machine** (or VM) without Python installed
2. **Verify all features work**:
   - Application launches
   - Web interface loads
   - API key configuration works
   - Content generation works
   - Database operations work
3. **Test configuration options**:
   - In-app API key entry
   - .env file configuration
4. **Check for errors** in the console output

## Security Notes

- The installers are not code-signed by default
- Users may see security warnings on first launch
- For production distribution, consider:
  - Code signing certificates (Windows: Authenticode, macOS: Apple Developer)
  - Notarization (macOS)
  - Antivirus scanning

## Support

For build issues or questions:
1. Check the troubleshooting section above
2. Review PyInstaller documentation: https://pyinstaller.org
3. Check application logs in the console output

## Version History

- **v1.0.0** - Initial release with Windows and macOS installers
