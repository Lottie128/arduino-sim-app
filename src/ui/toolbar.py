"""
Application Toolbar
"""

from .qt_compat import (
    QToolBar, QAction, QComboBox, QLabel,
    pyqtSignal
)


class AppToolBar(QToolBar):
    """Application toolbar"""
    
    simulation_started = pyqtSignal()
    simulation_stopped = pyqtSignal()
    compile_requested = pyqtSignal()
    upload_requested = pyqtSignal()
    board_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__("Main Toolbar", parent)
        self.setMovable(False)
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        # Simulation controls
        self.start_action = QAction("▶ Start", self)
        self.start_action.setToolTip("Start simulation (F5)")
        self.start_action.triggered.connect(self.simulation_started.emit)
        self.addAction(self.start_action)
        
        self.stop_action = QAction("⏹ Stop", self)
        self.stop_action.setToolTip("Stop simulation (Shift+F5)")
        self.stop_action.triggered.connect(self.simulation_stopped.emit)
        self.addAction(self.stop_action)
        
        self.addSeparator()
        
        # Board selection
        self.addWidget(QLabel(" Board: "))
        self.board_combo = QComboBox()
        self.board_combo.addItems([
            "Arduino Uno",
            "Arduino Nano", 
            "Arduino Mega",
            "ESP32",
            "ESP8266"
        ])
        self.board_combo.currentTextChanged.connect(self.board_changed.emit)
        self.addWidget(self.board_combo)
        
        self.addSeparator()
        
        # Compile and upload
        self.compile_action = QAction("⚙ Compile", self)
        self.compile_action.setToolTip("Compile code (F7)")
        self.compile_action.triggered.connect(self.compile_requested.emit)
        self.addAction(self.compile_action)
        
        self.upload_action = QAction("⬆ Upload", self)
        self.upload_action.setToolTip("Upload to board (F9)")
        self.upload_action.triggered.connect(self.upload_requested.emit)
        self.addAction(self.upload_action)
        
    def set_simulation_running(self, running: bool):
        """Update toolbar state based on simulation status"""
        self.start_action.setEnabled(not running)
        self.stop_action.setEnabled(running)
