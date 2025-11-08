#!/bin/bash
# macOS Installer Build Script for Nonprofit Idea Coach
# Run this from the project root directory

set -e  # Exit on error

echo "========================================"
echo "Nonprofit Idea Coach - macOS Installer Builder"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -d "nonprofit_coach" ]; then
    echo "ERROR: nonprofit_coach directory not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo "Step 1: Installing build dependencies..."
python3 -m pip install --upgrade pip --user
python3 -m pip install pyinstaller requests --user

echo ""
echo "Step 2: Installing application dependencies..."
python3 -m pip install -r nonprofit_coach/requirements.txt --user

echo ""
echo "Step 3: Creating standalone application..."
python3 -m PyInstaller --clean --noconfirm \
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
mkdir -p installer/dist/macos

# Copy executable
cp dist/NonprofitIdeaCoach installer/dist/macos/

# Create launcher script
cat > installer/dist/macos/start.command << 'EOF'
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

chmod +x installer/dist/macos/start.command
chmod +x installer/dist/macos/NonprofitIdeaCoach

# Copy configuration files
cp nonprofit_coach/.env.example installer/dist/macos/.env.example
cp nonprofit_coach/README.md installer/dist/macos/README.md

# Create setup instructions
cat > installer/dist/macos/INSTALL.txt << 'EOF'
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
echo "Step 5: Creating ZIP archive..."
pushd installer/dist/macos > /dev/null
zip -r ../NonprofitIdeaCoach-macOS-v1.0.0.zip .
popd > /dev/null

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Installer package created at:"
echo "  installer/dist/NonprofitIdeaCoach-macOS-v1.0.0.zip"
echo ""
echo "To distribute:"
echo "1. Share the ZIP file"
echo "2. Users extract and run 'start.command'"
echo ""
