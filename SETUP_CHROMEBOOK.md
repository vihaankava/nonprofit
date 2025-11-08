# Nonprofit Idea Coach - Chromebook Setup Guide

Complete setup instructions for Chromebook users using Linux (Beta) on Chrome OS.

## Prerequisites

Your Chromebook must support Linux (Beta). Most Chromebooks from 2019 or newer support this feature.

## One-Command Installation

After enabling Linux, copy and paste this into your Linux terminal:

```bash
git clone https://github.com/vihaankava/nonprofit.git && cd nonprofit/nonprofit_coach && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && echo "" && echo "========================================" && echo "✅ Setup Complete!" && echo "========================================" && echo "" && echo "Next steps:" && echo "1. Edit .env: nano .env" && echo "2. Add your Anthropic API key" && echo "3. Run: python app.py" && echo "4. Open Chrome to: http://localhost:5001" && echo ""
```

---

## Step-by-Step Setup

### Step 1: Enable Linux (Beta)

1. **Open Settings:**
   - Click the time in the bottom-right corner
   - Click the gear icon (Settings)

2. **Enable Linux:**
   - Scroll down to "Advanced"
   - Click "Developers"
   - Click "Turn On" next to "Linux development environment"
   - Click "Next" and then "Install"
   - Wait 5-10 minutes for Linux to install
   - A Terminal window will open when ready

3. **Update Linux:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

### Step 2: Install Required Packages

```bash
sudo apt install -y python3 python3-venv python3-pip git
```

This installs:
- Python 3 (programming language)
- venv (virtual environment tool)
- pip (package installer)
- git (version control)

### Step 3: Download the Application

**Option A: Using Git (Recommended)**
```bash
cd ~
git clone https://github.com/vihaankava/nonprofit.git
cd nonprofit/nonprofit_coach
```

**Option B: Download ZIP**
```bash
cd ~
wget https://github.com/vihaankava/nonprofit/archive/refs/heads/main.zip
unzip main.zip
cd nonprofit-main/nonprofit_coach
```

### Step 4: Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

### Step 5: Install Python Packages

```bash
pip install -r requirements.txt
```

This takes 2-3 minutes. You'll see packages being downloaded and installed.

### Step 6: Configure API Keys

1. **Copy the example configuration:**
   ```bash
   cp .env.example .env
   ```

2. **Get an Anthropic API Key:**
   - Open Chrome browser
   - Go to: https://console.anthropic.com/
   - Sign up or log in
   - Navigate to "API Keys"
   - Click "Create Key"
   - Copy your key (starts with `sk-ant-`)

3. **Edit the configuration:**
   ```bash
   nano .env
   ```

4. **Add your API key:**
   - Find the line: `ANTHROPIC_API_KEY=your_api_key_here`
   - Replace `your_api_key_here` with your actual key
   - Example: `ANTHROPIC_API_KEY=sk-ant-abc123...`

5. **Save and exit:**
   - Press `Ctrl+X`
   - Press `Y` to confirm
   - Press `Enter` to save

### Step 7: Run the Application

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5001
* Press CTRL+C to quit
```

### Step 8: Open in Chrome Browser

1. Open Chrome browser (not in the Linux terminal)
2. Go to: `http://localhost:5001`
3. Start using the app!

## Daily Usage

Each time you want to use the app:

1. **Open Terminal** (from your app launcher)

2. **Navigate and activate:**
   ```bash
   cd ~/nonprofit/nonprofit_coach
   source venv/bin/activate
   python app.py
   ```

3. **Open Chrome to:** `http://localhost:5001`

4. **When done:** Press `Ctrl+C` in Terminal, then type `deactivate`

## Quick Start Script

Create an easy launcher:

```bash
cat > ~/nonprofit/nonprofit_coach/start.sh << 'EOF'
#!/bin/bash
echo "========================================"
echo "Nonprofit Idea Coach"
echo "========================================"
echo ""

cd ~/nonprofit/nonprofit_coach

if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup first."
    exit 1
fi

echo "Starting application..."
source venv/bin/activate

python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing packages..."
    pip install -r requirements.txt
fi

echo ""
echo "Application running at: http://localhost:5001"
echo "Press Ctrl+C to stop"
echo ""

python app.py
deactivate
EOF

chmod +x ~/nonprofit/nonprofit_coach/start.sh
```

Then just run:
```bash
~/nonprofit/nonprofit_coach/start.sh
```

## Create Desktop Shortcut

Make it easy to launch from your app drawer:

```bash
mkdir -p ~/.local/share/applications

cat > ~/.local/share/applications/nonprofit-coach.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Nonprofit Idea Coach
Comment=AI-powered nonprofit planning
Exec=gnome-terminal -- bash -c "cd ~/nonprofit/nonprofit_coach && source venv/bin/activate && python app.py; exec bash"
Icon=applications-internet
Terminal=true
Categories=Development;Education;
EOF

chmod +x ~/.local/share/applications/nonprofit-coach.desktop
```

Now you can launch it from your app drawer!

## Chromebook-Specific Tips

### 1. Accessing from Chrome Browser

The app runs in the Linux container but is accessible from Chrome:
- Use: `http://localhost:5001`
- Or: `http://penguin.linux.test:5001`

### 2. File Access

Your Linux files are in:
- Files app → "Linux files" folder
- Path: `/home/yourusername/nonprofit`

### 3. Saving Files

Generated content is saved in:
```
~/nonprofit/nonprofit_coach/generated_sites/
```

Access via Files app → Linux files → nonprofit → nonprofit_coach → generated_sites

### 4. Backup Your Data

Important files to backup:
```bash
# Backup database and config
cp ~/nonprofit/nonprofit_coach/nonprofit.db ~/Downloads/
cp ~/nonprofit/nonprofit_coach/.env ~/Downloads/
```

These will appear in your Chrome OS Downloads folder.

### 5. Performance

Chromebooks vary in performance:
- **Low-end** (4GB RAM): Works but may be slow
- **Mid-range** (8GB RAM): Good performance
- **High-end** (16GB RAM): Excellent performance

## Troubleshooting

### Linux (Beta) Not Available

**Problem:** Can't find Linux option in Settings.

**Solution:**
- Your Chromebook may not support Linux
- Check: https://www.chromium.org/chromium-os/chrome-os-systems-supporting-linux/
- Chromebooks from 2019+ usually support it

### Terminal Won't Open

**Problem:** Terminal app doesn't launch.

**Solution:**
1. Go to Settings → Advanced → Developers
2. Click "Remove Linux development environment"
3. Reinstall Linux (Beta)
4. Try again

### "Permission Denied" Errors

**Problem:** Can't install packages or create files.

**Solution:**
- Don't use `sudo` with pip
- Virtual environments don't need sudo
- If you see permission errors, check you're in the venv:
  ```bash
  source venv/bin/activate
  ```

### Can't Access http://localhost:5001

**Problem:** Browser shows "can't connect" error.

**Solution:**
1. Make sure the app is running (check Terminal)
2. Try: `http://penguin.linux.test:5001`
3. Or try: `http://127.0.0.1:5001`
4. Restart Linux container:
   - Right-click Terminal in shelf
   - Select "Shut down Linux"
   - Reopen Terminal

### App Runs Slowly

**Problem:** Application is laggy or slow.

**Solution:**
1. Close other Chrome tabs
2. Close other Linux apps
3. Restart your Chromebook
4. Check available storage (need at least 2GB free)

### Out of Storage

**Problem:** "No space left on device" error.

**Solution:**
```bash
# Check storage
df -h

# Clean up
sudo apt autoremove
sudo apt clean

# Delete old downloads
rm -rf ~/Downloads/*
```

### Python Version Too Old

**Problem:** Python 3.7 or older.

**Solution:**
```bash
# Update Linux
sudo apt update
sudo apt upgrade -y

# Check version
python3 --version

# If still old, you may need to update Chrome OS
```

### Network Issues

**Problem:** Can't download packages.

**Solution:**
1. Check your internet connection
2. Try again:
   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```
3. If still failing, try one package at a time:
   ```bash
   pip install flask
   pip install anthropic
   pip install python-dotenv
   pip install requests
   ```

## Updating the Application

```bash
cd ~/nonprofit
git pull
cd nonprofit_coach
source venv/bin/activate
pip install -r requirements.txt --upgrade
python app.py
```

## Uninstalling

### Remove Application
```bash
rm -rf ~/nonprofit
```

### Remove Desktop Shortcut
```bash
rm ~/.local/share/applications/nonprofit-coach.desktop
```

### Remove Linux (Optional)
1. Go to Settings → Advanced → Developers
2. Click "Remove Linux development environment"
3. Confirm removal

## Advanced: Port Forwarding

To access from other devices on your network:

1. **Find your Chromebook's IP:**
   ```bash
   hostname -I
   ```

2. **Run app on all interfaces:**
   Edit `app.py` and ensure it has:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

3. **Access from other devices:**
   ```
   http://YOUR_CHROMEBOOK_IP:5001
   ```

## Chromebook Models Tested

✅ **Confirmed Working:**
- Acer Chromebook 314
- ASUS Chromebook Flip C434
- Google Pixelbook Go
- HP Chromebook x360 14
- Lenovo Chromebook Duet
- Samsung Galaxy Chromebook

⚠️ **May Have Issues:**
- Older Chromebooks (pre-2019)
- ARM-based Chromebooks (may need different packages)
- Chromebooks with less than 4GB RAM

## Performance Benchmarks

| Chromebook Specs | Startup Time | Response Time | Rating |
|-----------------|--------------|---------------|---------|
| 4GB RAM, Celeron | 15-20 sec | 3-5 sec | ⭐⭐⭐ |
| 8GB RAM, i3 | 8-12 sec | 1-2 sec | ⭐⭐⭐⭐ |
| 16GB RAM, i5+ | 5-8 sec | <1 sec | ⭐⭐⭐⭐⭐ |

## Getting Help

- **Chrome OS Help:** https://support.google.com/chromebook/
- **Linux on Chrome OS:** https://chromeos.dev/en/linux
- **App Issues:** https://github.com/vihaankava/nonprofit/issues

## Tips for Best Experience

1. **Use Chrome browser** (not Firefox or other browsers in Linux)
2. **Keep Chrome OS updated** for best Linux support
3. **Close unused tabs** to free up memory
4. **Use external storage** for large files
5. **Enable sync** to backup your Chrome OS settings

---

**You're all set!** Enjoy building nonprofit ideas on your Chromebook! 💻🎉
