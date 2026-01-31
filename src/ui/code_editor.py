"""
Code Editor Widget
"""

from .qt_compat import QWidget, QVBoxLayout, QPlainTextEdit, QFont


class CodeEditor(QWidget):
    """Arduino code editor"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlainText(
            "// Arduino code\n"
            "\n"
            "void setup() {\n"
            "  Serial.begin(9600);\n"
            "  pinMode(13, OUTPUT);\n"
            "}\n"
            "\n"
            "void loop() {\n"
            "  digitalWrite(13, HIGH);\n"
            "  delay(1000);\n"
            "  digitalWrite(13, LOW);\n"
            "  delay(1000);\n"
            "}\n"
        )
        
        # Set monospace font
        font = QFont("Courier")
        font.setPointSize(12)
        self.text_edit.setFont(font)
        
        layout.addWidget(self.text_edit)
        
    def get_code(self):
        """Get current code"""
        return self.text_edit.toPlainText()
        
    def set_code(self, code: str):
        """Set code"""
        self.text_edit.setPlainText(code)
        
    def clear(self):
        """Clear editor"""
        self.set_code("// Arduino code\n\nvoid setup() {\n  \n}\n\nvoid loop() {\n  \n}\n")
