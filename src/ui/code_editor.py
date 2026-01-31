"""
Code Editor Widget
"""

from .qt_compat import QWidget, QVBoxLayout, QPlainTextEdit


class CodeEditor(QWidget):
    """Arduino code editor"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlainText("// Arduino code here\nvoid setup() {\n  \n}\n\nvoid loop() {\n  \n}")
        
        layout.addWidget(self.text_edit)
        
    def get_code(self):
        """Get current code"""
        return self.text_edit.toPlainText()
        
    def set_code(self, code: str):
        """Set code"""
        self.text_edit.setPlainText(code)
        
    def clear(self):
        """Clear editor"""
        self.text_edit.clear()
