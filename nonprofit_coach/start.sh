#!/bin/bash
# Nonprofit Idea Coach - Linux/macOS Launcher
# Run this script to start the application

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
    echo ""
    echo "Please run setup first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if packages are installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Required packages not installed!"
    echo ""
    echo "Installing packages now..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "Installation failed. Please check your internet connection."
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo ""
echo "Starting Nonprofit Idea Coach..."
echo ""
echo "The application will be available at:"
echo "http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Try to open browser (works on macOS and most Linux)
(sleep 2 && (open http://localhost:5001 2>/dev/null || xdg-open http://localhost:5001 2>/dev/null)) &

# Run the application
python app.py

# Deactivate when done
deactivate
