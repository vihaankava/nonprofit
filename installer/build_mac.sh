#!/bin/bash
# macOS Installer Build Script for Nonprofit Idea Coach
# This script creates a standalone macOS application bundle with Python embedded

set -e  # Exit on error

echo "========================================"
echo "Nonprofit Idea Coach - macOS Installer Builder"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher from python.org or using Homebrew"
    exit 1
fi

echo "Step 1: Installing build dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install pyinstaller requests

echo ""
echo "Step 2: Installing application dependencies..."
cd ..
python3 -m pip install -r nonprofit_coach/requirements.txt

echo ""
echo "Step 3: Creating standalone application..."
pyinstaller --clean --noconfirm \
    --name "NonprofitIdeaCoach" \
    --onefile \
    --console \
    --add-data "nonprofit_coach/templates:templates" \
    --add-data "nonprofit_coach/static:static" \
    --add-data "nonprofit_coach/.env.example:." \
    --add-data "nonprofit_coach/README.md:." \
    --hidden-import "anthropic" \
    --hidden-import "flask" \
    --hidden-import "dotenv" \
    --hidden-import "sqlite3" \
    --hidden-import "gunicorn" \
    --hidden-import "nonprofit_coach.search_providers.brave" \
    --hidden-import "nonprofit_coach.search_providers.base" \
    --collect-all "anthropic" \
    --collect-all "flask" \
    nonprofit_coach/app.py

echo ""
echo "Step 4: Creating application bundle..."
cd installer
mkdir -p dist/macos

# Copy executable
cp ../dist/NonprofitIdeaCoach dist/macos/

# Create launcher script
cat > dist/macos/start.command << 'EOF'
#!/bin/bash
# Nonprofit Idea Coach Launcher

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Starting Nonprofit Idea Coach..."
echo ""
echo "The application will open in your web browser at http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Open browser after a short delay
(sleep 2 && open http://localhost:5001) &

# Run the application
./NonprofitIdeaCoach
EOF

chmod +x dist/macos/start.command
chmod +x dist/macos/NonprofitIdeaCoach

# Copy configuration files
cp ../nonprofit_coach/.env.example dist/macos/.env.example
cp ../nonprofit_coach/README.md dist/macos/README.md

# Create setup instructions
cat > dist/macos/INSTALL.txt << 'EOF'
# Nonprofit Idea Coach - macOS Installation

## Quick Start

1. Double-click "start.command" to launch the application
2. If you see a security warning, go to System Preferences > Security & Privacy and click "Open Anyway"
3. The application will open in your web browser
4. Follow the on-screen instructions

## Configuration (Optional)

To configure API keys and settings:
1. Copy ".env.example" to ".env"
2. Edit ".env" with your API keys using any text editor
3. Restart the application

## Requirements

- macOS 10.13 (High Sierra) or later
- Internet connection
- Anthropic API key (can be entered in the app)

## Troubleshooting

If you see "cannot be opened because the developer cannot be verified":
1. Right-click (or Control-click) on "start.command"
2. Select "Open" from the menu
3. Click "Open" in the dialog

For more information, see README.md
EOF

echo ""
echo "Step 5: Creating DMG installer..."

# Create a temporary directory for DMG contents
DMG_DIR="dist/dmg_temp"
mkdir -p "$DMG_DIR"
cp -r dist/macos/* "$DMG_DIR/"

# Create DMG
hdiutil create -volname "Nonprofit Idea Coach" \
    -srcfolder "$DMG_DIR" \
    -ov -format UDZO \
    dist/NonprofitIdeaCoach-macOS-v1.0.0.dmg

# Clean up
rm -rf "$DMG_DIR"

# Also create a ZIP for easier distribution
echo ""
echo "Step 6: Creating ZIP archive..."
cd dist/macos
zip -r ../NonprofitIdeaCoach-macOS-v1.0.0.zip .
cd ../..

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Installer packages created at:"
echo "  - installer/dist/NonprofitIdeaCoach-macOS-v1.0.0.dmg"
echo "  - installer/dist/NonprofitIdeaCoach-macOS-v1.0.0.zip"
echo ""
echo "To distribute:"
echo "1. Share the DMG or ZIP file"
echo "2. Users open and run 'start.command'"
echo ""
