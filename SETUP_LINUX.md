# Nonprofit Idea Coach - Linux Setup Guide

Complete setup instructions for Linux users (Ubuntu, Debian, Fedora, Arch, etc.).

## One-Command Installation

Copy and paste this entire command block into your terminal:

```bash
# Clone repository and setup
git clone https://github.com/vihaankava/nonprofit.git && \
cd nonprofit/nonprofit_coach && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
cp .env.example .env && \
echo "" && \
echo "========================================" && \
echo "Setup Complete!" && \
echo "========================================" && \
echo "" && \
echo "Next steps:" && \
echo "1. Edit .env file and add your Anthropic API key" && \
echo "2. Run: python app.py" && \
echo "3. Open browser to: http://localhost:5001" && \
echo ""
```

Then edit your API key:
```bash
nano .env  # or use vim, gedit, etc.
```

And start the app:
```bash
python app.py
```

---

## Detailed Step-by-Step Instructions

### Prerequisites

Most Linux distributions come with Python 3 pre-installed. Check your version:

```bash
python3 --version
```

You should see Python 3.8 or higher. If not, install it:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip git
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip git
```

**openSUSE:**
```bash
sudo zypper install python3 python3-pip git
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/vihaankava/nonprofit.git
cd nonprofit/nonprofit_coach
```

Or download and extract the ZIP:
```bash
wget https://github.com/vihaankava/nonprofit/archive/refs/heads/main.zip
unzip main.zip
cd nonprofit-main/nonprofit_coach
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
```

This creates an isolated Python environment in the `venv` folder.

### Step 3: Activate Virtual Environment

```bash
source venv/bin/activate
```

Your prompt should now show `(venv)` at the beginning.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Anthropic (AI integration)
- python-dotenv (configuration)
- requests (HTTP library)

### Step 5: Configure API Keys

1. **Copy the example configuration:**
   ```bash
   cp .env.example .env
   ```

2. **Get an Anthropic API Key:**
   - Visit: https://console.anthropic.com/
   - Sign up or log in
   - Go to "API Keys"
   - Create a new key
   - Copy it (starts with `sk-ant-`)

3. **Edit the configuration file:**
   ```bash
   nano .env
   ```
   
   Or use your preferred editor:
   ```bash
   vim .env
   # or
   gedit .env
   # or
   kate .env
   ```

4. **Add your API key:**
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   SECRET_KEY=change-this-to-something-random
   ```

5. **Optional - Enable web search:**
   ```
   SEARCH_ENABLED=true
   SEARCH_PROVIDER=brave
   BRAVE_API_KEY=your-brave-api-key-here
   ```

6. **Save and exit:**
   - In nano: Press `Ctrl+X`, then `Y`, then `Enter`
   - In vim: Press `Esc`, type `:wq`, press `Enter`

### Step 6: Run the Application

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5001
* Press CTRL+C to quit
```

### Step 7: Open in Browser

Open your web browser and go to:
```
http://localhost:5001
```

Or:
```
http://127.0.0.1:5001
```

## Daily Usage

After initial setup, use these commands:

```bash
cd ~/nonprofit/nonprofit_coach
source venv/bin/activate
python app.py
```

When done, press `Ctrl+C` to stop the server, then:
```bash
deactivate
```

## Quick Start Script

Create a launcher script for easy startup:

```bash
cat > start.sh << 'EOF'
#!/bin/bash
# Nonprofit Idea Coach Launcher

echo "========================================"
echo "Nonprofit Idea Coach"
echo "========================================"
echo ""

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if packages are installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Required packages not installed!"
    echo "Installing packages now..."
    pip install -r requirements.txt
fi

echo ""
echo "Starting Nonprofit Idea Coach..."
echo ""
echo "The application will be available at:"
echo "http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Open browser after 2 seconds (if available)
(sleep 2 && xdg-open http://localhost:5001 2>/dev/null) &

# Run the application
python app.py

# Deactivate when done
deactivate
EOF

chmod +x start.sh
```

Then just run:
```bash
./start.sh
```

## Desktop Shortcut (Optional)

Create a desktop launcher:

```bash
cat > ~/.local/share/applications/nonprofit-coach.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Nonprofit Idea Coach
Comment=AI-powered nonprofit planning tool
Exec=$HOME/nonprofit/nonprofit_coach/start.sh
Icon=applications-internet
Terminal=true
Categories=Development;Education;
EOF

chmod +x ~/.local/share/applications/nonprofit-coach.desktop
```

## Systemd Service (Advanced)

To run as a background service:

```bash
sudo tee /etc/systemd/system/nonprofit-coach.service > /dev/null << EOF
[Unit]
Description=Nonprofit Idea Coach
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/nonprofit/nonprofit_coach
Environment="PATH=$HOME/nonprofit/nonprofit_coach/venv/bin"
ExecStart=$HOME/nonprofit/nonprofit_coach/venv/bin/python app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable nonprofit-coach
sudo systemctl start nonprofit-coach
```

Check status:
```bash
sudo systemctl status nonprofit-coach
```

## Troubleshooting

### Python 3 Not Found

**Problem:** `python3: command not found`

**Solution:** Install Python 3:
```bash
# Ubuntu/Debian
sudo apt install python3 python3-venv python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

### Permission Denied

**Problem:** Can't create virtual environment or install packages.

**Solution:** Don't use `sudo` with pip. Use virtual environments instead (which you're already doing).

### Port 5001 Already in Use

**Problem:** Another process is using port 5001.

**Solution:**
```bash
# Find what's using the port
sudo lsof -i :5001

# Kill the process
kill -9 <PID>

# Or change the port in app.py
nano app.py
# Change: app.run(debug=True, host='0.0.0.0', port=5001)
# To:     app.run(debug=True, host='0.0.0.0', port=5002)
```

### Module Not Found Errors

**Problem:** Python can't find installed packages.

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt

# If still not working, recreate venv
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Browser Doesn't Open

**Problem:** `xdg-open` not available or browser doesn't open.

**Solution:** Manually open your browser and go to `http://localhost:5001`

### Firewall Blocking

**Problem:** Can't access the application.

**Solution:**
```bash
# UFW (Ubuntu)
sudo ufw allow 5001/tcp

# Firewalld (Fedora/CentOS)
sudo firewall-cmd --add-port=5001/tcp --permanent
sudo firewall-cmd --reload

# iptables
sudo iptables -A INPUT -p tcp --dport 5001 -j ACCEPT
```

### SELinux Issues (Fedora/RHEL)

**Problem:** SELinux blocking the application.

**Solution:**
```bash
# Temporarily disable
sudo setenforce 0

# Or configure properly
sudo setsebool -P httpd_can_network_connect 1
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

```bash
# Stop the service (if running)
sudo systemctl stop nonprofit-coach
sudo systemctl disable nonprofit-coach
sudo rm /etc/systemd/system/nonprofit-coach.service

# Remove the application
rm -rf ~/nonprofit

# Remove desktop shortcut
rm ~/.local/share/applications/nonprofit-coach.desktop
```

## Performance Tips

### Run on Different Port

Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Use Production Server

For better performance, use Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Access from Other Devices

The app binds to `0.0.0.0` by default, so you can access it from other devices on your network:
```
http://YOUR_LINUX_IP:5001
```

Find your IP:
```bash
ip addr show | grep inet
```

## Distribution-Specific Notes

### Ubuntu/Debian
- Python 3 is usually pre-installed
- Use `apt` for system packages
- Virtual environments work out of the box

### Fedora/RHEL/CentOS
- May need to enable EPEL repository
- Use `dnf` or `yum` for packages
- SELinux may need configuration

### Arch Linux
- Python 3 is the default Python
- Use `pacman` for packages
- Very up-to-date packages

### Raspberry Pi (Raspbian)
- Works great on Pi 3 or newer
- May be slower on older models
- Same commands as Debian

## Getting Help

- **Documentation:** See `README.md`
- **Issues:** https://github.com/vihaankava/nonprofit/issues
- **API Help:** https://docs.anthropic.com

---

**You're all set!** Enjoy building your nonprofit ideas on Linux! 🐧🚀
