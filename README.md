# Arduino Simulation & Programming Platform (Desktop)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Arduino CLI](https://img.shields.io/badge/Arduino_CLI-Compatible-00979D.svg)](https://arduino.github.io/arduino-cli/)
[![PyQt](https://img.shields.io/badge/GUI-PyQt5/6-41CD52.svg)](https://www.riverbankcomputing.com/software/pyqt/)

A comprehensive **offline desktop application** for Arduino and ESP32 electronics simulation and programming. Design circuits visually, simulate behavior in real-time, and upload code directly to physical boards - all without internet connection.

## ✨ Key Features

### 🖥️ Offline Desktop Application
- **No internet required** - fully functional offline
- **Native desktop performance** with PyQt5/6
- **Cross-platform** - Windows, macOS, Linux
- **Standalone executable** - no Python installation needed for end users

### 🔌 Circuit Simulation
- **Visual circuit designer** - drag-and-drop component placement
- **Extensive component library** - sensors, actuators, displays, passive components
- **Real-time simulation** - live circuit behavior with instant feedback
- **Connection validation** - automatic wiring error detection
- **Pin state visualization** - LED indicators and voltage monitoring
- **Virtual oscilloscope** - signal waveform display

### 📡 Hardware Integration
- **Arduino CLI integration** - direct compilation and upload
- **Multi-board support** - Arduino Uno, Mega, Nano, ESP32, ESP8266, and more
- **Auto port detection** - automatic USB device discovery
- **Serial monitor** - real-time serial communication
- **Serial plotter** - visualize sensor data
- **OTA programming** - wireless upload for ESP32/ESP8266

### 💻 Code Editor
- **Syntax highlighting** - Arduino C/C++ with color coding
- **Auto-completion** - intelligent code suggestions
- **Error highlighting** - real-time syntax checking
- **Code templates** - pre-built examples and snippets
- **Auto-generate code** - from circuit design
- **Library manager** - install and manage Arduino libraries

### 📚 Educational Features
- **Component datasheets** - built-in documentation
- **Tutorial projects** - step-by-step learning
- **Example circuits** - 50+ ready-to-use projects
- **Interactive help** - context-sensitive guidance

## 🚀 Quick Start

### macOS Installation

```bash
# Clone repository
git clone https://github.com/Lottie128/arduino-sim-app.git
cd arduino-sim-app

# Run automated setup
chmod +x setup_mac.sh
./setup_mac.sh

# Run application
source venv/bin/activate
python main.py  # or main_pyqt5.py for PyQt5
```

**Having issues on macOS?** See [INSTALL_MAC.md](INSTALL_MAC.md) for detailed troubleshooting.

### Linux Installation

```bash
# Clone repository
git clone https://github.com/Lottie128/arduino-sim-app.git
cd arduino-sim-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Windows Installation

```powershell
# Clone repository
git clone https://github.com/Lottie128/arduino-sim-app.git
cd arduino-sim-app

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 🎮 Try the Example

Run the battery-LED example to see the simulation in action:

```bash
source venv/bin/activate  # Windows: venv\Scripts\activate
python examples/battery_led.py
```

You'll see a complete circuit with:
- 5V battery
- 220Ω current-limiting resistor
- Red LED that lights up with realistic glow
- Real-time current and voltage calculations

## 📋 Prerequisites

- Python 3.8 or higher
- Arduino CLI (optional, for hardware upload)
- 4GB RAM minimum, 8GB recommended
- 500MB free disk space

### Installing Arduino CLI

**macOS:**
```bash
brew install arduino-cli
```

**Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
export PATH=$PATH:$HOME/bin
```

**Windows:**
```powershell
winget install ArduinoSA.CLI
```

Then install board cores:
```bash
arduino-cli core update-index
arduino-cli core install arduino:avr
arduino-cli core install esp32:esp32 --additional-urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

## 🏗️ Application Architecture

```
arduino-sim-app/
├── main.py                    # Application entry point (PyQt6)
├── main_pyqt5.py              # Alternative entry point (PyQt5)
├── requirements.txt           # Python dependencies
├── requirements-mac.txt       # macOS-specific (PyQt5)
├── setup_mac.sh               # Automated macOS setup
├── INSTALL_MAC.md             # macOS troubleshooting guide
├── src/
│   ├── ui/                    # PyQt user interface
│   │   ├── main_window.py     # Main application window
│   │   ├── canvas_view.py     # Circuit design canvas
│   │   ├── code_editor.py     # Code editor widget
│   │   ├── serial_monitor.py  # Serial communication
│   │   ├── component_panel.py # Component library panel
│   │   └── toolbar.py         # Application toolbar
│   ├── simulation/            # Circuit simulation engine
│   │   ├── engine.py          # Nodal analysis solver
│   │   ├── components/        # Component models
│   ├── arduino/               # Arduino CLI wrapper
│   ├── models/                # Data models
│   └── utils/                 # Utilities
├── examples/                  # Example projects
│   └── battery_led.py         # Battery + LED example
└── tests/                     # Unit tests
```

## 🛠️ Technology Stack

### Desktop Framework
- **PyQt5/PyQt6** - Qt bindings for Python
- **PyQtGraph** - Fast plotting for oscilloscope
- **QScintilla** - Advanced code editor

### Simulation Engine
- **NumPy** - Numerical computations
- **Modified Nodal Analysis** - Circuit equation solving
- **Real-time updates** - 20 FPS simulation loop

### Hardware Communication
- **Arduino CLI** - Official toolchain
- **PySerial** - Serial communication
- **pyusb** - USB device detection

## 🎮 Usage Guide

### Creating Your First Circuit

1. **Launch the application**
2. **Select board** - Choose Arduino Uno, ESP32, etc.
3. **Add components** - Drag from component panel
4. **Wire connections** - Right-click pins to connect
5. **Simulate** - Press F5 or click ▶ Start
6. **Write code** - Switch to Code tab
7. **Upload** - Connect board and click Upload

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New Project | Ctrl+N |
| Open Project | Ctrl+O |
| Save Project | Ctrl+S |
| Start/Stop Simulation | F5 |
| Compile Code | F7 |
| Upload to Board | F9 |
| Serial Monitor | Ctrl+Shift+M |

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 📦 Building Executables

```bash
# Install PyInstaller
pip install pyinstaller

# Build for current platform
pyinstaller --onefile --windowed --name ArduinoSimApp main.py

# Output in dist/ folder
```

## 🐛 Troubleshooting

### macOS Issues
See [INSTALL_MAC.md](INSTALL_MAC.md) for comprehensive macOS troubleshooting, including:
- PyQt6 symbol errors
- Virtual environment setup
- Apple Silicon compatibility
- Xcode Command Line Tools

### Linux Port Access
```bash
sudo usermod -a -G dialout $USER
# Log out and back in
```

### Windows Serial Port
- Install CH340/CP2102 drivers for Arduino clones
- Run as Administrator if port access denied

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📝 Roadmap

- [ ] SPICE integration for advanced analysis
- [ ] PCB layout export
- [ ] 3D component visualization
- [ ] Custom component creator
- [ ] Multi-language support
- [ ] Raspberry Pi support

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Arduino CLI team
- Qt Company for PyQt
- Wokwi and Tinkercad for inspiration
- Open-source electronics community

## 📧 Contact

**Developer**: Lottie Mukuka  
**GitHub**: [@Lottie128](https://github.com/Lottie128)  
**Organization**: Zero AI Technologies

---

**⭐ Star this repository if you find it useful!**
