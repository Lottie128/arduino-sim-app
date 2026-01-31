#!/usr/bin/env python3
"""
Arduino Simulation & Programming Platform
Offline Desktop Application
PyQt5 Version (Better macOS Compatibility)

Author: Lottie Mukuka
License: MIT
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt, QSettings
    from PyQt5.QtGui import QIcon
    PYQT_VERSION = 5
except ImportError:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt, QSettings
    from PyQt6.QtGui import QIcon
    PYQT_VERSION = 6

from src.ui.main_window import MainWindow
from src.utils.logger import setup_logger


def main():
    """Application entry point"""
    
    # Setup logging
    logger = setup_logger('arduino_sim_app')
    logger.info(f'Starting Arduino Simulation Platform (PyQt{PYQT_VERSION})')
    
    # Enable high DPI scaling
    if PYQT_VERSION == 6:
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    else:
        # PyQt5
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName('Arduino Simulation Platform')
    app.setApplicationVersion('1.0.0')
    app.setOrganizationName('Zero AI Technologies')
    app.setOrganizationDomain('zeroai.tech')
    
    # Set application icon
    icon_path = Path(__file__).parent / 'resources' / 'icons' / 'app_icon.png'
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Load settings
    settings = QSettings()
    
    # Apply theme
    theme = settings.value('theme', 'light')
    if theme == 'dark':
        apply_dark_theme(app)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    logger.info('Application started successfully')
    
    # Run application
    try:
        if PYQT_VERSION == 6:
            exit_code = app.exec()
        else:
            exit_code = app.exec_()
        logger.info(f'Application exited with code {exit_code}')
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f'Application crashed: {e}', exc_info=True)
        sys.exit(1)


def apply_dark_theme(app: QApplication):
    """Apply dark theme to application"""
    dark_stylesheet = """
    QMainWindow, QDialog, QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    QMenuBar {
        background-color: #3c3c3c;
        color: #ffffff;
    }
    QMenuBar::item:selected {
        background-color: #4a4a4a;
    }
    QMenu {
        background-color: #3c3c3c;
        color: #ffffff;
    }
    QMenu::item:selected {
        background-color: #4a4a4a;
    }
    QToolBar {
        background-color: #3c3c3c;
        border: none;
    }
    QPushButton {
        background-color: #4a4a4a;
        color: #ffffff;
        border: 1px solid #5a5a5a;
        padding: 5px 10px;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #5a5a5a;
    }
    QPushButton:pressed {
        background-color: #3a3a3a;
    }
    QTextEdit, QPlainTextEdit, QLineEdit {
        background-color: #1e1e1e;
        color: #d4d4d4;
        border: 1px solid #3c3c3c;
    }
    QTabWidget::pane {
        border: 1px solid #3c3c3c;
        background-color: #2b2b2b;
    }
    QTabBar::tab {
        background-color: #3c3c3c;
        color: #ffffff;
        padding: 8px 12px;
        border: 1px solid #3c3c3c;
    }
    QTabBar::tab:selected {
        background-color: #2b2b2b;
        border-bottom: 2px solid #007acc;
    }
    """
    app.setStyleSheet(dark_stylesheet)


if __name__ == '__main__':
    main()
