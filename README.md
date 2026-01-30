# Arduino Simulation & Programming Platform (Desktop)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Arduino CLI](https://img.shields.io/badge/Arduino_CLI-Compatible-00979D.svg)](https://arduino.github.io/arduino-cli/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52.svg)](https://www.riverbankcomputing.com/software/pyqt/)

A comprehensive **offline desktop application** for Arduino and ESP32 electronics simulation and programming. Design circuits visually, simulate behavior in real-time, and upload code directly to physical boards - all without internet connection.

## ✨ Key Features

### 🖥️ Offline Desktop Application
- **No internet required** - fully functional offline
- **Native desktop performance** with PyQt6
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

## 🏗️ Application Architecture

```
arduino-sim-app/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── src/
│   ├── ui/                    # PyQt6 user interface
│   │   ├── main_window.py     # Main application window
│   │   ├── canvas_view.py     # Circuit design canvas
│   │   ├── code_editor.py     # Code editor widget
│   │   ├── serial_monitor.py  # Serial communication
│   │   ├── component_panel.py # Component library panel
│   │   └── toolbar.py         # Application toolbar
│   ├── simulation/            # Circuit simulation engine
│   │   ├── engine.py          # Main simulation loop
│   │   ├── components/        # Component models
│   │   ├── circuit.py         # Circuit graph manager
│   │   └── solver.py          # Circuit equation solver
│   ├── arduino/               # Arduino CLI wrapper
│   │   ├── cli_manager.py     # Arduino CLI interface
│   │   ├── board_manager.py   # Board detection and config
│   │   ├── compiler.py        # Sketch compilation
│   │   ├── uploader.py        # Firmware upload
│   │   └── serial_comm.py     # Serial communication
│   ├── models/                # Data models
│   │   ├── component.py       # Component definitions
│   │   ├── project.py         # Project structure
│   │   └── circuit.py         # Circuit data model
│   └── utils/                 # Utilities
│       ├── code_generator.py  # Arduino code generation
│       ├── file_manager.py    # Project save/load
│       └── validators.py      # Input validation
├── resources/                 # Application resources
│   ├── icons/                 # UI icons
│   ├── components/            # Component images
│   ├── templates/             # Code templates
│   └── examples/              # Example projects
├── data/                      # Component library data
│   ├── components.json        # Component definitions
│   ├── boards.json            # Board configurations
│   └── libraries.json         # Library catalog
├── tests/                     # Unit and integration tests
└── build/                     # Executable builds
```

## 🛠️ Technology Stack

### Desktop Framework
- **PyQt6** - Modern Qt6 bindings for Python
- **PyQtGraph** - Fast plotting for oscilloscope and serial plotter
- **QScintilla** - Advanced code editor with syntax highlighting

### Simulation Engine
- **NumPy** - Numerical computations for circuit solving
- **SciPy** - Advanced circuit analysis algorithms
- **Custom Python engine** - Component behavior modeling

### Hardware Communication
- **Arduino CLI** - Official Arduino toolchain
- **PySerial** - Serial port communication
- **pyusb** - USB device detection

### Data Management
- **SQLite** - Local project database
- **JSON** - Component and configuration storage
- **Pickle** - Fast project serialization

## 📋 Prerequisites

- Python 3.8 or higher
- Arduino CLI installed
- USB drivers for Arduino/ESP32 boards (typically auto-installed)
- 4GB RAM minimum, 8GB recommended
- 500MB free disk space

## 🚀 Installation

### Option 1: Run from Source (Developers)

#### 1. Clone Repository
```bash
git clone https://github.com/Lottie128/arduino-sim-app.git
cd arduino-sim-app
```

#### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install Arduino CLI

**Linux/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
export PATH=$PATH:$HOME/bin
arduino-cli core update-index
arduino-cli core install arduino:avr
arduino-cli core install esp32:esp32 --additional-urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

**Windows:**
```powershell
winget install ArduinoSA.CLI
arduino-cli core update-index
arduino-cli core install arduino:avr
arduino-cli core install esp32:esp32 --additional-urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

#### 5. Run Application
```bash
python main.py
```

### Option 2: Install Pre-built Executable (End Users)

1. Download the latest release for your platform from [Releases](https://github.com/Lottie128/arduino-sim-app/releases)
2. Extract the archive
3. Run the executable:
   - **Windows**: `ArduinoSimApp.exe`
   - **macOS**: `ArduinoSimApp.app`
   - **Linux**: `./ArduinoSimApp`

## 🎮 Usage Guide

### Creating Your First Circuit

1. **Launch the application** - Open ArduinoSimApp
2. **Select board** - Choose Arduino Uno, ESP32, etc. from the toolbar
3. **Add components**:
   - Browse component panel on the left
   - Drag components onto the canvas
   - Position them as desired
4. **Wire connections**:
   - Click on a component pin
   - Click on another pin to create connection
   - Right-click connection to delete
5. **Simulate**:
   - Click "▶ Start Simulation" button
   - Observe LED states, serial output, etc.
   - Adjust component values in real-time
6. **Write/Generate code**:
   - Switch to Code tab
   - Write custom code or click "Generate from Circuit"
   - Edit in the code editor
7. **Upload to hardware**:
   - Connect Arduino/ESP32 via USB
   - Select port from dropdown
   - Click "Upload" button

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
| Component Search | Ctrl+F |
| Zoom In | Ctrl++ |
| Zoom Out | Ctrl+- |
| Delete Selected | Delete |

### Project Structure

Projects are saved as `.ardusim` files containing:
- Circuit design (components and connections)
- Arduino code
- Board configuration
- Simulation settings
- Serial monitor data

## 🧩 Component Library

### Input Components
- **Buttons & Switches**: Push button, toggle switch, DIP switch
- **Sensors**: DHT11/22 (temp/humidity), DS18B20, BMP280, PIR motion, HC-SR04 ultrasonic
- **Input Devices**: Potentiometer, joystick, rotary encoder, keypad
- **Light Sensors**: LDR, photodiode, phototransistor
- **Motion**: MPU6050 (accelerometer/gyro), ADXL345

### Output Components
- **LEDs**: Standard LED, RGB LED, NeoPixel strips
- **Displays**: 16x2 LCD, 20x4 LCD, OLED (SSD1306), 7-segment display, TFT LCD
- **Motors**: DC motor, servo motor, stepper motor (28BYJ-48)
- **Sound**: Piezo buzzer, passive buzzer, speaker
- **Relays**: 5V relay module, solid-state relay

### Communication Modules
- **Serial**: UART, Software Serial
- **Wireless**: ESP32/ESP8266 WiFi, HC-05/06 Bluetooth, NRF24L01 RF
- **Protocols**: I2C devices, SPI devices

### Power & Passive
- **Power**: Battery, power supply, voltage regulator (7805, LM317)
- **Resistors**: Fixed, variable (potentiometer)
- **Capacitors**: Ceramic, electrolytic
- **Others**: Diode, transistor (NPN/PNP), LED

## 🔧 Arduino CLI Integration

### Board Management

```python
from src.arduino.cli_manager import ArduinoCLI

cli = ArduinoCLI()

# List available boards
boards = cli.list_boards()

# Detect connected boards
connected = cli.detect_boards()

# Install board package
cli.install_core('esp32:esp32')
```

### Compilation and Upload

```python
from src.arduino.compiler import Compiler
from src.arduino.uploader import Uploader

# Compile sketch
compiler = Compiler()
result = compiler.compile(
    sketch_path='project/sketch.ino',
    fqbn='arduino:avr:uno'
)

if result.success:
    # Upload to board
    uploader = Uploader()
    uploader.upload(
        sketch_path='project/sketch.ino',
        fqbn='arduino:avr:uno',
        port='/dev/ttyUSB0'
    )
```

### Serial Communication

```python
from src.arduino.serial_comm import SerialMonitor

monitor = SerialMonitor()
monitor.connect('/dev/ttyUSB0', baudrate=9600)

# Send data
monitor.write('Hello Arduino\n')

# Read data
data = monitor.read_line()
print(f'Received: {data}')

# Close connection
monitor.disconnect()
```

## 🎨 Code Generation

The app automatically generates Arduino code from your circuit:

```cpp
// Auto-generated from circuit design

// Pin definitions
#define LED_PIN 13
#define BUTTON_PIN 2
#define TEMP_SENSOR_PIN A0

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  // Button control
  if (digitalRead(BUTTON_PIN) == LOW) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  
  // Temperature reading
  int tempValue = analogRead(TEMP_SENSOR_PIN);
  float temperature = tempValue * (5.0 / 1023.0) * 100.0;
  Serial.println(temperature);
  
  delay(100);
}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_simulation.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run UI tests (requires display)
pytest tests/test_ui.py -v --no-headless
```

## 📦 Building Executables

### Using PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Build for current platform
pyinstaller --onefile --windowed \
  --name ArduinoSimApp \
  --icon resources/icons/app_icon.ico \
  --add-data "resources:resources" \
  --add-data "data:data" \
  main.py

# Output in dist/ folder
```

### Platform-Specific Builds

**Windows:**
```bash
pyinstaller build_windows.spec
```

**macOS:**
```bash
pyinstaller build_macos.spec
# Create DMG installer
hdiutil create -volname "ArduinoSimApp" -srcfolder dist/ArduinoSimApp.app -ov -format UDZO ArduinoSimApp.dmg
```

**Linux:**
```bash
pyinstaller build_linux.spec
# Create AppImage or DEB package
```

## 🐛 Troubleshooting

### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run with debug output
python main.py --debug
```

### Arduino CLI Not Found
```bash
# Verify installation
arduino-cli version

# Set custom path in settings
# Settings > Arduino CLI Path > Browse
```

### Port Access Denied (Linux)
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER
# Log out and back in
```

### ESP32 Upload Fails
```bash
# Install/update ESP32 core
arduino-cli core update-index
arduino-cli core install esp32:esp32 --additional-urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

# Hold BOOT button during upload
```

### Simulation Runs Slowly
- Reduce component count
- Lower simulation speed in settings
- Disable oscilloscope when not needed
- Close unused tabs

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewComponent`)
3. Commit changes (`git commit -m 'Add new component'`)
4. Push to branch (`git push origin feature/NewComponent`)
5. Open Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run code formatting
black src/
flake8 src/

# Type checking
mypy src/
```

### Adding New Components

1. Create component model in `src/simulation/components/`
2. Add component definition to `data/components.json`
3. Add icon to `resources/components/`
4. Write tests in `tests/test_components.py`
5. Update documentation

## 📝 Roadmap

### Version 1.1
- [ ] Advanced SPICE integration
- [ ] PCB layout generation export
- [ ] 3D component visualization
- [ ] Custom component creator

### Version 1.2
- [ ] Multi-language support (Spanish, French, German)
- [ ] Cloud project backup (optional)
- [ ] Collaborative editing (offline-first)
- [ ] Video tutorials integration

### Version 2.0
- [ ] Raspberry Pi support
- [ ] FPGA simulation
- [ ] AI circuit design assistant
- [ ] Augmented reality component preview

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Arduino CLI team for excellent tooling
- Qt Company for PyQt6 framework
- Wokwi and Tinkercad for inspiration
- Open-source electronics community

## 📧 Contact

**Developer**: Lottie Mukuka  
**GitHub**: [@Lottie128](https://github.com/Lottie128)  
**Organization**: Zero AI Technologies

---

**⭐ Star this repository if you find it useful!**
