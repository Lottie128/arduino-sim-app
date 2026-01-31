#!/bin/bash
# macOS Setup Script for Arduino Simulation Platform

set -e  # Exit on error

echo "========================================"
echo "Arduino Simulation Platform - macOS Setup"
echo "========================================"
echo ""

# Check macOS version
echo "Checking macOS version..."
sw_vers
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "Found: $PYTHON_VERSION"
else
    echo "ERROR: Python 3 not found!"
    echo "Please install Python 3.8 or higher from python.org or using Homebrew:"
    echo "  brew install python@3.11"
    exit 1
fi
echo ""

# Check architecture
echo "Checking architecture..."
ARCH=$(uname -m)
echo "Architecture: $ARCH"
if [ "$ARCH" = "arm64" ]; then
    echo "Apple Silicon detected"
else
    echo "Intel Mac detected"
fi
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Removing..."
    rm -rf venv
fi

python3 -m venv venv
echo "Virtual environment created."
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "Choose installation option:"
echo "1) PyQt6 (Latest, may have compatibility issues)"
echo "2) PyQt5 (Recommended for macOS, more stable)"
read -p "Enter choice (1 or 2): " CHOICE

if [ "$CHOICE" = "2" ]; then
    echo "Installing with PyQt5..."
    pip install -r requirements-mac.txt
else
    echo "Installing with PyQt6..."
    # Try PyQt6 first
    if pip install PyQt6==6.6.1 PyQt6-sip==13.6.0; then
        echo "PyQt6 installed successfully"
        pip install -r requirements.txt
    else
        echo "PyQt6 installation failed. Falling back to PyQt5..."
        pip install -r requirements-mac.txt
    fi
fi
echo ""

# Test PyQt installation
echo "Testing PyQt installation..."
if python3 -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')" 2>/dev/null; then
    echo "✓ PyQt6 working"
    PYQT_VERSION=6
elif python3 -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 OK')" 2>/dev/null; then
    echo "✓ PyQt5 working"
    PYQT_VERSION=5
else
    echo "✗ PyQt installation failed!"
    echo "Please check the error messages above and try manual installation."
    exit 1
fi
echo ""

# Check for Arduino CLI
echo "Checking for Arduino CLI..."
if command -v arduino-cli &> /dev/null; then
    echo "✓ Arduino CLI found: $(arduino-cli version)"
else
    echo "⚠ Arduino CLI not found"
    echo "Install Arduino CLI:"
    echo "  brew install arduino-cli"
    echo "Or download from: https://arduino.github.io/arduino-cli/"
fi
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
if [ "$PYQT_VERSION" = "5" ]; then
    echo "  python main_pyqt5.py"
else
    echo "  python main.py"
fi
echo ""
echo "To run the battery-LED example:"
echo "  source venv/bin/activate"
echo "  python examples/battery_led.py"
echo ""
echo "For troubleshooting, see: INSTALL_MAC.md"
echo ""
