# macOS Installation Guide

## Quick Fix for PyQt6 Symbol Error

If you encounter the error:
```
ImportError: Symbol not found: __Z13lcPermissionsv
```

This is caused by PyQt6 compatibility issues on macOS. Follow these steps:

### Solution 1: Clean Install in Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd arduino-sim-app

# Remove any existing PyQt6 installations
pip3 uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y

# Create fresh virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install PyQt6 with specific compatible versions
pip install PyQt6==6.6.1 PyQt6-sip==13.6.0

# Install other dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Solution 2: Use Homebrew Python

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python via Homebrew
brew install python@3.11

# Create virtual environment with Homebrew Python
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run application
python main.py
```

### Solution 3: Downgrade to PyQt5 (Most Stable for macOS)

If PyQt6 continues to have issues, PyQt5 is more stable on older macOS versions:

```bash
# Activate virtual environment
source venv/bin/activate

# Uninstall PyQt6
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y

# Install PyQt5 instead
pip install PyQt5==5.15.10 PyQt5-sip==12.13.0
pip install QScintilla==2.13.4
pip install pyqtgraph==0.13.3

# The code will work with minimal changes
python main.py
```

### Solution 4: Use System Python with User Install

```bash
# Uninstall from user site-packages
python3 -m pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y

# Clean pip cache
python3 -m pip cache purge

# Install with --user flag and specific version
python3 -m pip install --user --force-reinstall PyQt6==6.6.1 PyQt6-sip==13.6.0

# Install other dependencies
python3 -m pip install --user -r requirements.txt

# Run with full path
python3 main.py
```

## Verify Installation

Test if PyQt6 is working:

```bash
python3 -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"
```

If successful, you should see: `PyQt6 OK`

## Common Issues

### Issue: Multiple Python Versions

```bash
# Check which Python you're using
which python3
python3 --version

# Check where PyQt6 is installed
python3 -m pip show PyQt6
```

### Issue: Architecture Mismatch (Apple Silicon)

If you're on Apple Silicon (M1/M2/M3):

```bash
# Check architecture
uname -m

# Install Rosetta 2 if needed
softwareupdate --install-rosetta

# Use native ARM Python
arch -arm64 python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Outdated Xcode Command Line Tools

```bash
# Update Xcode Command Line Tools
xcode-select --install

# Accept license
sudo xcodebuild -license accept
```

## Run the Battery-LED Example

```bash
# After successful installation
source venv/bin/activate
python examples/battery_led.py
```

You should see a window with a battery, resistor, and LED circuit that automatically simulates.

## Alternative: Run with Docker (No macOS Installation Issues)

If all else fails, use Docker with X11 forwarding:

```bash
# Install XQuartz for X11
brew install --cask xquartz

# Start XQuartz and enable network connections
open -a XQuartz
# In XQuartz preferences: Security > "Allow connections from network clients"

# Get your IP
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')

# Allow X11 connections
xhost + $IP

# Build and run Docker container
docker build -t arduino-sim-app .
docker run -e DISPLAY=$IP:0 -v /tmp/.X11-unix:/tmp/.X11-unix arduino-sim-app
```

## Getting Help

If you continue to have issues:

1. Check macOS version: `sw_vers`
2. Check Python version: `python3 --version`
3. Check chip architecture: `uname -m`
4. Share the output in GitHub issues
