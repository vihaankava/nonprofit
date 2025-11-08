#!/bin/bash
# Simple macOS Installer for Nonprofit Idea Coach
# This installer checks for Python and creates a virtual environment

set -e

echo "========================================"
echo "Nonprofit Idea Coach - Simple Installer"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed on this system."
    echo ""
    echo "Would you like to install Python using Homebrew?"
    echo ""
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Homebrew is not installed either."
        echo ""
        echo "Please install Python 3 by either:"
        echo "1. Installing Homebrew: https://brew.sh"
        echo "   Then run: brew install python3"
        echo "2. Downloading from: https://www.python.org/downloads/"
        echo ""
        read -p "Press Enter to open Python download page..."
        open https://www.python.org/downloads/
        exit 1
    else
        read -p "Install Python 3 with Homebrew? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            brew install python3
        else
            echo "Installation cancelled."
            exit 1
        fi
    fi
fi

echo "Python found!"
python3 --version
echo ""

# Set installation directory
INSTALL_DIR="$HOME/NonprofitIdeaCoach"
echo "Installing to: $INSTALL_DIR"
echo ""

if [ -d "$INSTALL_DIR" ]; then
    echo "Installation directory already exists."
    read -p "Do you want to reinstall? This will delete the existing installation. (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
    rm -rf "$INSTALL_DIR"
fi

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo ""
echo "Step 2: Upgrading pip..."
python -m pip install --upgrade pip

echo ""
echo "Step 3: Copying application files..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp -r "$SCRIPT_DIR/../nonprofit_coach" "$INSTALL_DIR/"

echo ""
echo "Step 4: Installing dependencies..."
pip install -r nonprofit_coach/requirements.txt

echo ""
echo "Step 5: Creating launcher..."
cat > "$INSTALL_DIR/start.command" << 'EOF'
#!/bin/bash
# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Activate virtual environment
source venv/bin/activate

echo ""
echo "========================================"
echo "Nonprofit Idea Coach"
echo "========================================"
echo ""
echo "Starting server..."
echo "The application will open at: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Open browser after a short delay
(sleep 2 && open http://localhost:5001) &

# Start the application
cd nonprofit_coach
python app.py
EOF

chmod +x "$INSTALL_DIR/start.command"

echo ""
echo "Step 6: Creating application alias..."
# Create an alias in Applications folder
mkdir -p "$HOME/Applications"
ln -sf "$INSTALL_DIR/start.command" "$HOME/Applications/Nonprofit Idea Coach.command"

echo ""
echo "Step 7: Setting up configuration..."
if [ ! -f "$INSTALL_DIR/nonprofit_coach/.env" ]; then
    cp "$INSTALL_DIR/nonprofit_coach/.env.example" "$INSTALL_DIR/nonprofit_coach/.env"
    echo "Configuration file created at: nonprofit_coach/.env"
    echo "You can edit this file to add your API keys."
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "The application has been installed to:"
echo "$INSTALL_DIR"
echo ""
echo "To start the application:"
echo "1. Double-click: ~/Applications/Nonprofit Idea Coach.command"
echo "   OR"
echo "2. Run: $INSTALL_DIR/start.command"
echo ""
echo "To configure API keys:"
echo "Edit: $INSTALL_DIR/nonprofit_coach/.env"
echo ""
read -p "Press Enter to start the application now..."

open "$INSTALL_DIR/start.command"
