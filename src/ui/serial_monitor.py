"""
Serial Monitor Widget
"""

from .qt_compat import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QComboBox, QLabel
)


class SerialMonitor(QWidget):
    """Serial monitor for Arduino communication"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Top controls
        control_layout = QHBoxLayout()
        
        control_layout.addWidget(QLabel("Port:"))
        self.port_combo = QComboBox()
        self.port_combo.addItems(["Select port..."])
        control_layout.addWidget(self.port_combo)
        
        control_layout.addWidget(QLabel("Baud:"))
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "115200", "57600", "38400", "19200"])
        control_layout.addWidget(self.baud_combo)
        
        self.connect_button = QPushButton("Connect")
        control_layout.addWidget(self.connect_button)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_output)
        control_layout.addWidget(self.clear_button)
        
        control_layout.addStretch()
        
        layout.addLayout(control_layout)
        
        # Output area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlainText("Serial monitor ready...\n")
        layout.addWidget(self.output)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type message to send...")
        self.send_button = QPushButton("Send")
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
    def clear_output(self):
        """Clear output text"""
        self.output.clear()
        self.output.setPlainText("Serial monitor cleared...\n")
        
    def append_output(self, text: str):
        """Append text to output"""
        self.output.append(text)
