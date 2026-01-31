"""
PyQt5/PyQt6 Compatibility Layer
Automatically imports from PyQt5 or PyQt6 depending on what's available
"""

try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    PYQT_VERSION = 6
    
    # PyQt6 renames some enums
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QApplication
    
    # Compatibility aliases
    def exec_app(app):
        return app.exec()
        
except ImportError:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    PYQT_VERSION = 5
    
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication
    
    # Compatibility aliases
    def exec_app(app):
        return app.exec_()

print(f"Using PyQt{PYQT_VERSION}")
