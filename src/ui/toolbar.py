"""
Application Toolbar
"""

from .qt_compat import (
    QToolBar, QAction, QComboBox,
    pyqtSignal
)


class AppToolBar(QToolBar):
    """Application toolbar"""
    
    simulation_started = pyqtSignal()
    simulation_stopped = pyqtSignal()
    compile_requested = pyqtSignal()
    upload_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        # Simulation controls
        self.start_action = QAction("▶ Start", self)
        self.start_action.triggered.connect(self.simulation_started.emit)
        self.addAction(self.start_action)
        
        self.stop_action = QAction("⬜ Stop", self)
        self.stop_action.triggered.connect(self.simulation_stopped.emit)
        self.addAction(self.stop_action)
        
        self.addSeparator()
        
        # Board selection
        self.board_combo = QComboBox()
        self.board_combo.addItems(["Arduino Uno", "ESP32", "Arduino Nano"])
        self.addWidget(self.board_combo)
        
        self.addSeparator()
        
        # Compile and upload
        self.compile_action = QAction("⚙ Compile", self)
        self.compile_action.triggered.connect(self.compile_requested.emit)
        self.addAction(self.compile_action)
        
        self.upload_action = QAction("⬆ Upload", self)
        self.upload_action.triggered.connect(self.upload_requested.emit)
        self.addAction(self.upload_action)
