"""
Component Library Panel
"""

from .qt_compat import (
    QWidget, QVBoxLayout, QListWidget, QLabel,
    QListWidgetItem, QPushButton, QHBoxLayout, pyqtSignal
)


class ComponentPanel(QWidget):
    """Component library panel"""
    
    component_selected = pyqtSignal(str, object)  # component_type, position
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Header
        header = QLabel("<b>Components</b>")
        layout.addWidget(header)
        
        # Component list
        self.list_widget = QListWidget()
        
        # Power sources
        self.add_category("Power Sources")
        self.list_widget.addItem("  Battery (5V)")
        self.list_widget.addItem("  Battery (3.3V)")
        
        self.add_category("Output Devices")
        self.list_widget.addItem("  LED (Red)")
        self.list_widget.addItem("  LED (Green)")
        self.list_widget.addItem("  LED (Blue)")
        self.list_widget.addItem("  RGB LED")
        
        self.add_category("Passive Components")
        self.list_widget.addItem("  Resistor (220Ω)")
        self.list_widget.addItem("  Resistor (1kΩ)")
        self.list_widget.addItem("  Resistor (10kΩ)")
        self.list_widget.addItem("  Capacitor")
        
        self.add_category("Input Devices")
        self.list_widget.addItem("  Push Button")
        self.list_widget.addItem("  Potentiometer")
        
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        layout.addWidget(self.list_widget)
        
        # Add button
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add to Canvas")
        self.add_button.clicked.connect(self.on_add_clicked)
        button_layout.addWidget(self.add_button)
        layout.addLayout(button_layout)
        
    def add_category(self, name: str):
        """Add category header"""
        item = QListWidgetItem(name)
        try:
            from .qt_compat import Qt
            item.setFlags(Qt.ItemFlag.NoItemFlags)  # PyQt6
        except:
            from .qt_compat import Qt
            item.setFlags(Qt.NoItemFlags)  # PyQt5
        try:
            from .qt_compat import QFont
            font = QFont()
            font.setBold(True)
            item.setFont(font)
        except:
            pass
        self.list_widget.addItem(item)
        
    def on_item_double_clicked(self, item: QListWidgetItem):
        """Handle item double click"""
        text = item.text().strip()
        if not text or text.endswith(":"):
            return
            
        component_type = self.parse_component_type(text)
        if component_type:
            self.component_selected.emit(component_type, None)
            
    def on_add_clicked(self):
        """Handle add button click"""
        current = self.list_widget.currentItem()
        if current:
            self.on_item_double_clicked(current)
            
    def parse_component_type(self, text: str) -> str:
        """Parse component type from list item text"""
        text = text.lower()
        if "battery" in text:
            return "battery"
        elif "led" in text and "rgb" not in text:
            return "led"
        elif "resistor" in text:
            return "resistor"
        elif "button" in text:
            return "button"
        elif "potentiometer" in text:
            return "potentiometer"
        return ""
