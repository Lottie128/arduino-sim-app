"""
Component Library Panel
"""

from .qt_compat import (
    QWidget, QVBoxLayout, QListWidget, QLabel,
    QListWidgetItem, pyqtSignal
)


class ComponentPanel(QWidget):
    """Component library panel"""
    
    component_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        label = QLabel("Components")
        layout.addWidget(label)
        
        self.list_widget = QListWidget()
        self.list_widget.addItem("Battery (5V)")
        self.list_widget.addItem("LED")
        self.list_widget.addItem("Resistor")
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        layout.addWidget(self.list_widget)
        
    def on_item_double_clicked(self, item: QListWidgetItem):
        """Handle item double click"""
        component_type = item.text().split()[0].lower()
        self.component_selected.emit(component_type)
