"""
Main Application Window
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTabWidget, QStatusBar, QMenuBar,
    QMenu, QToolBar, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QKeySequence

from .canvas_view import CanvasView
from .code_editor import CodeEditor
from .serial_monitor import SerialMonitor
from .component_panel import ComponentPanel
from .toolbar import AppToolBar
from ..models.project import Project
from ..arduino.cli_manager import ArduinoCLI


class MainWindow(QMainWindow):
    """Main application window"""
    
    project_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.project = Project()
        self.arduino_cli = ArduinoCLI()
        self.init_ui()
        self.setup_connections()
        self.update_title()
        
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle('Arduino Simulation Platform')
        self.setGeometry(100, 100, 1400, 900)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.toolbar = AppToolBar(self)
        self.addToolBar(self.toolbar)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left panel - Component library
        self.component_panel = ComponentPanel()
        
        # Center - Main workspace
        center_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Top - Circuit/Code tabs
        self.tab_widget = QTabWidget()
        self.canvas_view = CanvasView()
        self.code_editor = CodeEditor()
        
        self.tab_widget.addTab(self.canvas_view, "Circuit Design")
        self.tab_widget.addTab(self.code_editor, "Code")
        
        # Bottom - Serial monitor
        self.serial_monitor = SerialMonitor()
        
        center_splitter.addWidget(self.tab_widget)
        center_splitter.addWidget(self.serial_monitor)
        center_splitter.setStretchFactor(0, 3)
        center_splitter.setStretchFactor(1, 1)
        
        # Add panels to main layout
        main_layout.addWidget(self.component_panel, 1)
        main_layout.addWidget(center_splitter, 4)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        new_action = QAction('&New Project', self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction('&Open Project...', self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction('&Save Project', self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('Save Project &As...', self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('&Edit')
        
        undo_action = QAction('&Undo', self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('&Redo', self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction('Cu&t', self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction('&Copy', self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('&Paste', self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        edit_menu.addAction(paste_action)
        
        # Simulation menu
        sim_menu = menubar.addMenu('&Simulation')
        
        start_sim_action = QAction('&Start Simulation', self)
        start_sim_action.setShortcut('F5')
        start_sim_action.triggered.connect(self.start_simulation)
        sim_menu.addAction(start_sim_action)
        
        stop_sim_action = QAction('S&top Simulation', self)
        stop_sim_action.setShortcut('Shift+F5')
        stop_sim_action.triggered.connect(self.stop_simulation)
        sim_menu.addAction(stop_sim_action)
        
        # Arduino menu
        arduino_menu = menubar.addMenu('&Arduino')
        
        compile_action = QAction('&Compile', self)
        compile_action.setShortcut('F7')
        compile_action.triggered.connect(self.compile_code)
        arduino_menu.addAction(compile_action)
        
        upload_action = QAction('&Upload', self)
        upload_action.setShortcut('F9')
        upload_action.triggered.connect(self.upload_code)
        arduino_menu.addAction(upload_action)
        
        arduino_menu.addSeparator()
        
        serial_action = QAction('Serial &Monitor', self)
        serial_action.setShortcut('Ctrl+Shift+M')
        serial_action.triggered.connect(self.toggle_serial_monitor)
        arduino_menu.addAction(serial_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        docs_action = QAction('&Documentation', self)
        docs_action.setShortcut('F1')
        help_menu.addAction(docs_action)
        
        examples_action = QAction('&Examples', self)
        help_menu.addAction(examples_action)
        
        help_menu.addSeparator()
        
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_connections(self):
        """Setup signal-slot connections"""
        self.toolbar.simulation_started.connect(self.start_simulation)
        self.toolbar.simulation_stopped.connect(self.stop_simulation)
        self.toolbar.compile_requested.connect(self.compile_code)
        self.toolbar.upload_requested.connect(self.upload_code)
        
        self.component_panel.component_selected.connect(
            self.canvas_view.add_component
        )
        
    def new_project(self):
        """Create new project"""
        # TODO: Check for unsaved changes
        self.project = Project()
        self.canvas_view.clear()
        self.code_editor.clear()
        self.update_title()
        self.status_bar.showMessage('New project created')
        
    def open_project(self):
        """Open existing project"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            'Open Project',
            '',
            'Arduino Sim Projects (*.ardusim);;All Files (*)'
        )
        if filename:
            # TODO: Load project
            self.status_bar.showMessage(f'Opened: {filename}')
            
    def save_project(self):
        """Save current project"""
        if self.project.filename:
            # TODO: Save project
            self.status_bar.showMessage('Project saved')
        else:
            self.save_project_as()
            
    def save_project_as(self):
        """Save project with new name"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Save Project As',
            '',
            'Arduino Sim Projects (*.ardusim)'
        )
        if filename:
            # TODO: Save project
            self.project.filename = filename
            self.update_title()
            self.status_bar.showMessage(f'Saved as: {filename}')
            
    def start_simulation(self):
        """Start circuit simulation"""
        self.canvas_view.start_simulation()
        self.status_bar.showMessage('Simulation running')
        
    def stop_simulation(self):
        """Stop circuit simulation"""
        self.canvas_view.stop_simulation()
        self.status_bar.showMessage('Simulation stopped')
        
    def compile_code(self):
        """Compile Arduino code"""
        code = self.code_editor.get_code()
        self.status_bar.showMessage('Compiling...')
        # TODO: Implement compilation
        
    def upload_code(self):
        """Upload code to Arduino board"""
        self.status_bar.showMessage('Uploading...')
        # TODO: Implement upload
        
    def toggle_serial_monitor(self):
        """Show/hide serial monitor"""
        if self.serial_monitor.isVisible():
            self.serial_monitor.hide()
        else:
            self.serial_monitor.show()
            
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            'About Arduino Simulation Platform',
            '<h3>Arduino Simulation Platform</h3>'
            '<p>Version 1.0.0</p>'
            '<p>Offline electronics simulation and programming</p>'
            '<p>© 2026 Zero AI Technologies</p>'
            '<p>Developer: Lottie Mukuka</p>'
        )
        
    def update_title(self):
        """Update window title"""
        title = 'Arduino Simulation Platform'
        if self.project.filename:
            title += f' - {self.project.filename}'
        if self.project.is_modified:
            title += ' *'
        self.setWindowTitle(title)
        
    def closeEvent(self, event):
        """Handle window close event"""
        # TODO: Check for unsaved changes
        event.accept()
