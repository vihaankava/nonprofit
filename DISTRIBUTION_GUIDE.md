# Nonprofit Idea Coach - Distribution Guide

This guide explains how to create installers for distributing the Nonprofit Idea Coach application to end users who may not have Python installed.

## Two Installation Methods

We provide two different installation approaches:

### 1. **Standalone Executable** (Recommended for Most Users)
- **Pros**: No Python required, single executable, easiest for end users
- **Cons**: Larger file size (~100-200 MB), longer build time
- **Best for**: General distribution, non-technical users

### 2. **Simple Installer with Virtual Environment** (Lightweight)
- **Pros**: Smaller download (~5-10 MB), faster build, easier to update
- **Cons**: Requires Python installation, slightly more complex for users
- **Best for**: Technical users, development teams, frequent updates

---

## Method 1: Standalone Executable

### Building the Installer

#### Windows
```cmd
cd installer
build_windows.bat
```

**Output**: `installer/dist/NonprofitIdeaCoach-Windows-v1.0.0.zip` (~150 MB)

#### macOS
```bash
cd installer
./build_mac.sh
```

**Output**: 
- `installer/dist/NonprofitIdeaCoach-macOS-v1.0.0.dmg` (~150 MB)
- `installer/dist/NonprofitIdeaCoach-macOS-v1.0.0.zip` (~150 MB)

### What's Included
- Python runtime (embedded)
- All Python dependencies
- Application code and assets
- SQLite database
- Configuration templates
- Easy launcher scripts

### End User Installation

#### Windows
1. Download and extract the ZIP file
2. Double-click `start.bat`
3. Application opens in browser at http://localhost:5001

#### macOS
1. Download and open the DMG (or extract ZIP)
2. Double-click `start.command`
3. If security warning: Right-click → Open
4. Application opens in browser at http://localhost:5001

### Distribution
- Upload to file sharing service (Dropbox, Google Drive, etc.)
- Share download link with users
- No additional setup required

---

## Method 2: Simple Installer (Virtual Environment)

### Creating the Installer

#### Windows
```cmd
cd installer
# Copy install_windows_simple.bat to a distribution folder
# Include the entire nonprofit_coach directory
```

#### macOS
```bash
cd installer
# Copy install_mac_simple.sh to a distribution folder
# Include the entire nonprofit_coach directory
```

### What's Included
- Installation script
- Application source code
- Requirements file
- Configuration templates

### End User Installation

#### Windows
1. Download the installer package
2. Double-click `install_windows_simple.bat`
3. Follow the prompts (will install Python if needed)
4. Use desktop shortcut or Start menu to launch

#### macOS
1. Download the installer package
2. Open Terminal and run: `./install_mac_simple.sh`
3. Follow the prompts (will install Python if needed)
4. Use Applications folder shortcut to launch

### Distribution
- Create a ZIP with:
  - `install_windows_simple.bat` or `install_mac_simple.sh`
  - `nonprofit_coach/` directory
- Upload to file sharing service
- Share download link with instructions

---

## Comparison Table

| Feature | Standalone Executable | Simple Installer |
|---------|----------------------|------------------|
| File Size | ~150 MB | ~5 MB |
| Python Required | No | Yes (auto-installs) |
| Build Time | 5-10 minutes | Instant |
| User Setup Time | 1 minute | 3-5 minutes |
| Updates | Rebuild entire package | Update code only |
| Best For | End users | Developers/Technical users |

---

## Configuration for End Users

Both methods support two configuration approaches:

### Option 1: In-App Configuration (Easiest)
1. Launch the application
2. Enter Anthropic API key when prompted
3. Optionally save for future sessions

### Option 2: Environment File
1. Copy `.env.example` to `.env`
2. Edit `.env` with API keys:
   ```
   ANTHROPIC_API_KEY=your_key_here
   BRAVE_API_KEY=your_brave_key_here
   ```
3. Restart the application

---

## System Requirements

### Windows
- Windows 10 or later (64-bit)
- 4 GB RAM minimum
- 500 MB free disk space
- Internet connection
- Modern web browser

### macOS
- macOS 10.13 (High Sierra) or later
- 4 GB RAM minimum
- 500 MB free disk space
- Internet connection
- Modern web browser

---

## Building for Distribution - Step by Step

### For Standalone Executables

1. **Prepare the build environment**:
   ```bash
   # Install PyInstaller
   pip install pyinstaller
   
   # Install all dependencies
   cd nonprofit_coach
   pip install -r requirements.txt
   cd ..
   ```

2. **Run the build script**:
   - Windows: `installer\build_windows.bat`
   - macOS: `installer/build_mac.sh`

3. **Test the installer**:
   - Extract/mount the package
   - Run the launcher
   - Test all features
   - Verify on a clean machine (VM recommended)

4. **Distribute**:
   - Upload to hosting service
   - Create download page with instructions
   - Include system requirements

### For Simple Installers

1. **Prepare the package**:
   ```bash
   mkdir distribution
   cp -r nonprofit_coach distribution/
   cp installer/install_mac_simple.sh distribution/
   # or for Windows:
   # copy installer\install_windows_simple.bat distribution\
   ```

2. **Create archive**:
   ```bash
   cd distribution
   zip -r NonprofitIdeaCoach-Simple.zip .
   ```

3. **Test the installer**:
   - Extract on a test machine
   - Run the installer script
   - Verify installation completes
   - Test the application

4. **Distribute**:
   - Upload ZIP file
   - Provide installation instructions
   - Include Python installation guide

---

## Troubleshooting Common Issues

### Build Issues

**"Python not found"**
- Install Python 3.8+ from python.org
- Ensure Python is in system PATH

**"PyInstaller failed"**
- Update PyInstaller: `pip install --upgrade pyinstaller`
- Check all dependencies are installed
- Review build logs for specific errors

**"Module not found" during build**
- Add missing module to hidden imports in build script
- Install missing dependency: `pip install <module>`

### User Installation Issues

**Windows: "Windows protected your PC"**
- Click "More info" → "Run anyway"
- This is normal for unsigned executables

**macOS: "Cannot be opened because developer cannot be verified"**
- Right-click → Open → Open
- Or: System Preferences → Security & Privacy → Open Anyway

**"Port 5001 already in use"**
- Close other applications using port 5001
- Or modify the port in app.py

---

## Security Considerations

### Code Signing (Recommended for Production)

**Windows**:
- Obtain Authenticode certificate
- Sign executable: `signtool sign /f cert.pfx NonprofitIdeaCoach.exe`

**macOS**:
- Enroll in Apple Developer Program
- Sign app: `codesign --sign "Developer ID" NonprofitIdeaCoach`
- Notarize: `xcrun notarytool submit`

### Best Practices
- Scan installers with antivirus before distribution
- Use HTTPS for download links
- Provide SHA256 checksums for verification
- Keep dependencies updated for security patches

---

## Updating the Application

### Standalone Executable
1. Make code changes
2. Rebuild installer with build script
3. Increment version number
4. Distribute new installer
5. Users download and replace old version

### Simple Installer
1. Make code changes
2. Create new ZIP with updated code
3. Users can update by:
   - Re-running installer (overwrites)
   - Or manually replacing files in installation directory

---

## Support and Documentation

### For Builders
- See `installer/README.md` for detailed build instructions
- Check PyInstaller docs: https://pyinstaller.org
- Review build logs for troubleshooting

### For End Users
- Include `INSTALL.txt` in packages
- Provide README.md with usage instructions
- Create FAQ for common issues
- Set up support channel (email, forum, etc.)

---

## Quick Start Checklist

- [ ] Choose installation method (standalone vs simple)
- [ ] Install build dependencies (PyInstaller for standalone)
- [ ] Test build on your development machine
- [ ] Test installer on clean VM or test machine
- [ ] Verify all features work in installed version
- [ ] Create distribution package (ZIP/DMG)
- [ ] Write installation instructions for users
- [ ] Test installation process as end user would
- [ ] Upload to distribution platform
- [ ] Share with users and gather feedback

---

## Example Distribution Email

```
Subject: Nonprofit Idea Coach - Installation Instructions

Hello!

Thank you for your interest in Nonprofit Idea Coach!

DOWNLOAD:
[Link to installer]

INSTALLATION:
1. Download the file for your operating system
2. Extract the ZIP file (or open the DMG on Mac)
3. Double-click the launcher:
   - Windows: "start.bat"
   - Mac: "start.command"
4. The app will open in your web browser

CONFIGURATION:
You'll need an Anthropic API key to use the AI features.
You can enter this when you first launch the app.

SYSTEM REQUIREMENTS:
- Windows 10+ or macOS 10.13+
- Internet connection
- Modern web browser

SUPPORT:
If you encounter any issues, please contact [support email]

Best regards,
[Your Name]
```

---

## Version History

- **v1.0.0** - Initial release
  - Standalone executables for Windows and macOS
  - Simple installers with virtual environment
  - Full feature set with AI and search integration
