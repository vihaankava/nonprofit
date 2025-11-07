#!/bin/bash

echo "=========================================="
echo "Nonprofit Idea Coach - Manual Test Guide"
echo "=========================================="
echo ""
echo "Choose your testing method:"
echo ""
echo "1. Web Interface (Recommended)"
echo "   - Start server: python3 app.py"
echo "   - Visit: http://localhost:5000/test"
echo "   - Click buttons to test each function"
echo ""
echo "2. Command Line (curl)"
echo "   - See manual_test_guide.md for curl commands"
echo ""
echo "3. Automated Test Script"
echo "   - Run: python3 test_integration.py"
echo ""
echo "=========================================="
echo ""
read -p "Start Flask server now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Starting Flask server on http://localhost:5000"
    echo "Test interface: http://localhost:5000/test"
    echo ""
    python3 app.py
fi
