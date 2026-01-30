# Arduino Simulation & Programming Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Arduino CLI](https://img.shields.io/badge/Arduino_CLI-Compatible-00979D.svg)](https://arduino.github.io/arduino-cli/)

A comprehensive web-based electronics simulation platform for Arduino and ESP32 that bridges virtual circuit design with real hardware deployment. Design, simulate, and upload code directly to physical boards - all from your browser.

## 🚀 Features

### Circuit Simulation
- **Interactive Circuit Builder**: Drag-and-drop interface for designing Arduino/ESP32 circuits
- **Component Library**: Extensive collection of sensors, actuators, displays, and passive components
- **Real-time Simulation**: Live circuit behavior visualization with WebSocket updates
- **Wiring Validation**: Automatic connection checking and error detection
- **Visual Debugging**: Pin state monitoring and serial output visualization

### Hardware Integration
- **Arduino CLI Integration**: Direct compilation and upload to physical boards
- **Multi-board Support**: Arduino Uno, Mega, Nano, ESP32, ESP8266, and more
- **Port Auto-detection**: Automatic USB device discovery
- **Serial Monitor**: Real-time serial communication with connected devices
- **OTA Updates**: Over-the-air programming for ESP32/ESP8266

### Code Management
- **Built-in Code Editor**: Syntax highlighting and auto-completion for Arduino C/C++
- **Code Generation**: Auto-generate Arduino sketches from circuit designs
- **Library Management**: Install and manage Arduino libraries
- **Version Control**: Save and load project configurations
- **Code Templates**: Pre-built examples for common projects

### Educational Features
- **Component Datasheets**: Integrated documentation and pinout diagrams
- **Tutorial Mode**: Step-by-step guidance for beginners
- **Project Examples**: Curated collection of starter projects
- **Virtual Oscilloscope**: Visualize analog signals and PWM outputs

## 🏗️ Architecture

```
arduino-sim-app/
├── backend/                  # Python FastAPI backend
│   ├── api/                  # REST API endpoints
│   ├── arduino_cli/          # Arduino CLI wrapper
│   ├── simulation/           # Circuit simulation engine
│   ├── websocket/            # Real-time communication
│   └── models/               # Data models and schemas
├── frontend/                 # React-based UI
│   ├── components/           # React components
│   ├── canvas/               # Circuit design canvas
│   ├── editor/               # Code editor integration
│   └── simulator/            # Simulation visualizer
├── components/               # Component library definitions
├── examples/                 # Sample projects
└── docs/                     # Documentation
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance async Python web framework
- **Arduino CLI**: Official Arduino command-line interface
- **PySerial**: Serial communication with hardware
- **WebSockets**: Real-time bidirectional communication
- **SQLite/PostgreSQL**: Project and user data storage
- **Pydantic**: Data validation and serialization

### Frontend
- **React**: Modern UI framework
- **Konva.js/Fabric.js**: Canvas-based circuit designer
- **Monaco Editor**: VS Code-powered code editor
- **Socket.io Client**: Real-time updates
- **Material-UI/Tailwind**: Component styling

### Simulation
- **Custom Python Engine**: Component behavior simulation
- **SPICE Integration** (optional): Advanced circuit analysis
- **WebGL**: Hardware-accelerated rendering

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16+ and npm (for frontend)
- Arduino CLI installed and configured
- USB drivers for Arduino/ESP32 boards
- Modern web browser (Chrome, Firefox, Edge)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Lottie128/arduino-sim-app.git
cd arduino-sim-app
```

### 2. Install Arduino CLI

**Linux/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
export PATH=$PATH:$HOME/bin
arduino-cli core update-index
arduino-cli core install arduino:avr
arduino-cli core install esp32:esp32
```

**Windows:**
```powershell
winget install ArduinoSA.CLI
arduino-cli core update-index
arduino-cli core install arduino:avr
arduino-cli core install esp32:esp32
```

### 3. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

### 5. Configuration

Create `.env` file in the backend directory:
```env
ARDUINO_CLI_PATH=/path/to/arduino-cli
PORT=8000
DATABASE_URL=sqlite:///./arduino_sim.db
CORS_ORIGINS=http://localhost:3000
WEBSOCKET_PORT=8001
```

## 🚀 Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Access the application at `http://localhost:3000`

### Production Deployment

```bash
# Build frontend
cd frontend
npm run build

# Run backend with production settings
cd ../backend
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📖 Usage Guide

### Creating a New Circuit

1. **Launch the App**: Open your browser and navigate to the application
2. **New Project**: Click "New Circuit" and select your target board (e.g., Arduino Uno, ESP32)
3. **Add Components**: Drag components from the library onto the canvas
4. **Wire Connections**: Click pins to create connections between components
5. **Simulate**: Click "Run Simulation" to test circuit behavior
6. **Generate Code**: Auto-generate Arduino sketch or write custom code
7. **Upload**: Connect your board and click "Upload to Board"

### Uploading to Physical Hardware

```python
# Example: Upload sketch via Python API
import requests

response = requests.post('http://localhost:8000/api/upload', json={
    'board': 'arduino:avr:uno',
    'port': '/dev/ttyUSB0',  # or COM3 on Windows
    'sketch': sketch_code
})
```

### Using Arduino CLI Wrapper

```python
from backend.arduino_cli import ArduinoManager

manager = ArduinoManager()

# List available boards
boards = manager.list_boards()

# Compile sketch
result = manager.compile(sketch_path, 'arduino:avr:uno')

# Upload to board
manager.upload(sketch_path, 'arduino:avr:uno', '/dev/ttyUSB0')

# Monitor serial output
manager.start_serial_monitor('/dev/ttyUSB0', 9600)
```

## 🧩 Component Library

### Currently Supported Components

**Input Devices:**
- Push buttons, switches, potentiometers
- Temperature sensors (DHT11, DHT22, DS18B20)
- Motion sensors (PIR, ultrasonic)
- Light sensors (LDR, photoresistor)
- Accelerometers and gyroscopes

**Output Devices:**
- LEDs (standard, RGB, NeoPixel)
- LCD displays (16x2, 20x4, I2C)
- OLED displays (SSD1306)
- Servo motors, DC motors, stepper motors
- Buzzers and speakers

**Communication:**
- UART, I2C, SPI interfaces
- Bluetooth modules (HC-05, HC-06)
- WiFi modules (ESP8266, ESP32 built-in)
- RF modules (NRF24L01)

**Passive Components:**
- Resistors, capacitors, inductors
- Transistors, diodes, voltage regulators

## 🔌 API Documentation

### REST Endpoints

```
GET    /api/boards              # List available boards
GET    /api/ports               # List connected devices
POST   /api/compile             # Compile Arduino sketch
POST   /api/upload              # Upload to board
GET    /api/libraries           # List installed libraries
POST   /api/libraries/install   # Install library
GET    /api/components          # Get component library
POST   /api/projects            # Save project
GET    /api/projects/:id        # Load project
```

### WebSocket Events

```javascript
// Client -> Server
socket.emit('simulate', { circuit: circuitData });
socket.emit('serial_connect', { port: '/dev/ttyUSB0', baudRate: 9600 });

// Server -> Client
socket.on('simulation_update', (data) => { /* Update UI */ });
socket.on('serial_data', (data) => { /* Display serial output */ });
socket.on('upload_progress', (progress) => { /* Show progress */ });
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=./

# Frontend tests
cd frontend
npm test

# Integration tests
pytest tests/integration/ -v
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/React
- Write unit tests for new features
- Update documentation for API changes
- Add component definitions for new hardware

## 📚 Project Structure Details

### Backend Components

- **`api/`**: REST API route handlers
- **`arduino_cli/`**: Arduino CLI wrapper and board management
- **`simulation/`**: Circuit simulation engine and component models
- **`websocket/`**: Real-time communication handlers
- **`models/`**: Pydantic models and database schemas
- **`utils/`**: Helper functions and utilities

### Frontend Components

- **`components/canvas/`**: Circuit design drag-and-drop interface
- **`components/editor/`**: Code editor with syntax highlighting
- **`components/simulator/`**: Real-time simulation visualizer
- **`components/hardware/`**: Board connection and upload UI
- **`services/`**: API client and WebSocket manager

## 🐛 Troubleshooting

### Arduino CLI Not Found
```bash
# Verify installation
arduino-cli version

# Update PATH if needed
export PATH=$PATH:/path/to/arduino-cli
```

### Port Access Denied (Linux)
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER
# Log out and back in
```

### ESP32 Upload Issues
```bash
# Install ESP32 board support
arduino-cli core install esp32:esp32 --additional-urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

### WebSocket Connection Failed
- Check CORS settings in backend `.env`
- Verify firewall allows port 8001
- Ensure backend is running before frontend

## 📝 Roadmap

- [ ] Advanced SPICE simulation integration
- [ ] Collaborative circuit editing
- [ ] Mobile app (React Native)
- [ ] Cloud project storage
- [ ] AI-powered circuit design assistant
- [ ] PCB layout generation
- [ ] 3D component visualization
- [ ] Multi-language support
- [ ] Raspberry Pi integration
- [ ] Custom component creator

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Arduino CLI team for excellent tooling
- Wokwi and Tinkercad for inspiration
- Open-source electronics community
- All contributors to this project

## 📧 Contact

**Developer**: Lottie Mukuka  
**GitHub**: [@Lottie128](https://github.com/Lottie128)  
**Organization**: Zero AI Technologies

---

**Star ⭐ this repository if you find it useful!**
