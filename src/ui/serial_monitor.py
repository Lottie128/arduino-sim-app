"""
Serial Monitor Widget
"""

from .qt_compat import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout


class SerialMonitor(QWidget):
    """Serial monitor for Arduino communication"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.send_button = QPushButton("Send")
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
