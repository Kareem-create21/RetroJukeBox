from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

class ThemeManager:
    """Manages application themes."""
    
    def __init__(self):
        """Initialize theme manager."""
        self.themes = {
            "light": self.light_theme,
            "dark": self.dark_theme,
            "retro_blue": self.retro_blue_theme,
            "retro_green": self.retro_green_theme,
            "retro_pink": self.retro_pink_theme
        }
    
    def apply_theme(self, window, theme_name):
        """Apply selected theme to the application."""
        if theme_name in self.themes:
            theme_func = self.themes[theme_name]
            theme_func(window)
        else:
            # Default to dark theme
            self.dark_theme(window)
    
    def light_theme(self, window):
        """Apply light theme to the application."""
        palette = QPalette()
        app = QApplication.instance()
        
        # Set base colors
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        # Set disabled colors
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(120, 120, 120))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 120, 120))
        
        # Apply palette
        app.setPalette(palette)
        
        # Set stylesheet for custom styles
        app.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QLabel { color: #000000; }
            QPushButton { 
                background-color: #e0e0e0; 
                border: 1px solid #a0a0a0; 
                border-radius: 4px; 
                padding: 5px; 
            }
            QPushButton:hover { background-color: #d0d0d0; }
            QPushButton:pressed { background-color: #c0c0c0; }
            QSlider::handle { background-color: #808080; border-radius: 5px; }
            QToolButton { 
                background-color: #e0e0e0; 
                border: 1px solid #a0a0a0; 
                border-radius: 4px; 
            }
            QToolButton:hover { background-color: #d0d0d0; }
            QToolButton:pressed { background-color: #c0c0c0; }
            QStatusBar { background-color: #e0e0e0; }
        """)
        
        # Set fonts
        default_font = QFont("Arial", 10)
        app.setFont(default_font)
    
    def dark_theme(self, window):
        """Apply dark theme to the application."""
        palette = QPalette()
        app = QApplication.instance()
        
        # Set base colors
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        # Set disabled colors
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(120, 120, 120))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 120, 120))
        
        # Apply palette
        app.setPalette(palette)
        
        # Set stylesheet for custom styles
        app.setStyleSheet("""
            QMainWindow { background-color: #353535; }
            QLabel { color: #ffffff; }
            QPushButton { 
                background-color: #454545; 
                border: 1px solid #555555; 
                border-radius: 4px; 
                padding: 5px; 
                color: #ffffff;
            }
            QPushButton:hover { background-color: #505050; }
            QPushButton:pressed { background-color: #606060; }
            QSlider::handle { background-color: #909090; border-radius: 5px; }
            QToolButton { 
                background-color: #454545; 
                border: 1px solid #555555; 
                border-radius: 4px; 
                color: #ffffff;
            }
            QToolButton:hover { background-color: #505050; }
            QToolButton:pressed { background-color: #606060; }
            QStatusBar { background-color: #252525; }
            QListWidget { background-color: #252525; color: #ffffff; }
            QListWidget::item:selected { background-color: #3a6ea5; }
            QTabWidget::pane { 
                border: 1px solid #555555;
                background-color: #353535;
            }
            QTabBar::tab {
                background-color: #252525;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px 10px;
            }
            QTabBar::tab:selected {
                background-color: #353535;
            }
            QTabBar::tab:hover {
                background-color: #454545;
            }
            QGroupBox { 
                border: 1px solid #555555;
                margin-top: 20px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
        """)
        
        # Set fonts
        default_font = QFont("Arial", 10)
        app.setFont(default_font)
    
    def retro_blue_theme(self, window):
        """Apply retro blue theme to the application."""
        palette = QPalette()
        app = QApplication.instance()
        
        # Set base colors (80s blue theme)
        palette.setColor(QPalette.Window, QColor(0, 51, 102))  # Dark blue
        palette.setColor(QPalette.WindowText, QColor(204, 255, 255))  # Light cyan
        palette.setColor(QPalette.Base, QColor(0, 102, 153))  # Medium blue
        palette.setColor(QPalette.AlternateBase, QColor(0, 76, 153))  # Blue
        palette.setColor(QPalette.ToolTipBase, QColor(0, 51, 102))  # Dark blue
        palette.setColor(QPalette.ToolTipText, QColor(204, 255, 255))  # Light cyan
        palette.setColor(QPalette.Text, QColor(204, 255, 255))  # Light cyan
        palette.setColor(QPalette.Button, QColor(0, 102, 204))  # Bright blue
        palette.setColor(QPalette.ButtonText, QColor(204, 255, 255))  # Light cyan
        palette.setColor(QPalette.BrightText, QColor(255, 0, 102))  # Hot pink
        palette.setColor(QPalette.Highlight, QColor(0, 204, 255))  # Cyan
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))  # Black
        
        # Apply palette
        app.setPalette(palette)
        
        # Set stylesheet for custom styles
        app.setStyleSheet("""
            QMainWindow { background-color: #003366; }
            QLabel { color: #ccffff; }
            QPushButton { 
                background-color: #0066cc; 
                border: 2px solid #00ccff; 
                border-radius: 4px; 
                padding: 5px; 
                color: #ccffff;
                font-family: "VCR OSD Mono", "Courier New", monospace;
            }
            QPushButton:hover { background-color: #0099ff; }
            QPushButton:pressed { background-color: #0033cc; }
            QSlider::handle { 
                background-color: #00ccff; 
                border-radius: 5px; 
                border: 1px solid #ccffff; 
            }
            QSlider::groove:horizontal {
                border: 1px solid #ccffff;
                height: 8px;
                background: #004080;
            }
            QToolButton { 
                background-color: #0066cc; 
                border: 2px solid #00ccff; 
                border-radius: 4px; 
                color: #ccffff;
            }
            QToolButton:hover { background-color: #0099ff; }
            QToolButton:pressed { background-color: #0033cc; }
            QListWidget { 
                background-color: #006699; 
                color: #ccffff; 
                font-family: "VCR OSD Mono", "Courier New", monospace;
            }
            QListWidget::item:selected { 
                background-color: #00ccff; 
                color: #000000;
            }
            QStatusBar { 
                background-color: #004080; 
                color: #ccffff;
            }
            QTabWidget::pane { 
                border: 2px solid #00ccff;
                background-color: #003366;
            }
            QTabBar::tab {
                background-color: #004080;
                color: #ccffff;
                border: 1px solid #00ccff;
                padding: 5px 10px;
                font-family: "VCR OSD Mono", "Courier New", monospace;
            }
            QTabBar::tab:selected {
                background-color: #0066cc;
            }
            QTabBar::tab:hover {
                background-color: #0099ff;
            }
        """)
        
        # Set retro font
        retro_font = QFont("Courier New", 10)
        app.setFont(retro_font)
    
    def retro_green_theme(self, window):
        """Apply retro green (terminal) theme to the application."""
        palette = QPalette()
        app = QApplication.instance()
        
        # Set base colors (terminal green theme)
        palette.setColor(QPalette.Window, QColor(0, 0, 0))  # Black
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0))  # Green
        palette.setColor(QPalette.Base, QColor(20, 20, 20))  # Dark gray
        palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))  # Slightly lighter
        palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))  # Black
        palette.setColor(QPalette.ToolTipText, QColor(0, 255, 0))  # Green
        palette.setColor(QPalette.Text, QColor(0, 255, 0))  # Green
        palette.setColor(QPalette.Button, QColor(40, 40, 40))  # Dark gray
        palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))  # Green
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))  # Red
        palette.setColor(QPalette.Highlight, QColor(0, 128, 0))  # Dark green
        palette.setColor(QPalette.HighlightedText, QColor(0, 255, 0))  # Green
        
        # Apply palette
        app.setPalette(palette)
        
        # Set stylesheet for custom styles
        app.setStyleSheet("""
            QMainWindow { background-color: #000000; }
            QLabel { color: #00ff00; }
            QPushButton { 
                background-color: #202020; 
                border: 1px solid #00ff00; 
                border-radius: 0px; 
                padding: 5px; 
                color: #00ff00;
                font-family: "Courier New", monospace;
            }
            QPushButton:hover { 
                background-color: #303030;
                border: 1px dashed #00ff00;
            }
            QPushButton:pressed { background-color: #008800; }
            QSlider::handle { 
                background-color: #00ff00; 
                border-radius: 0px; 
                border: 1px solid #00ff00; 
            }
            QSlider::groove:horizontal {
                border: 1px solid #00ff00;
                height: 8px;
                background: #202020;
            }
            QToolButton { 
                background-color: #202020; 
                border: 1px solid #00ff00; 
                border-radius: 0px; 
                color: #00ff00;
            }
            QToolButton:hover { 
                background-color: #303030;
                border: 1px dashed #00ff00;
            }
            QToolButton:pressed { background-color: #008800; }
            QListWidget { 
                background-color: #202020; 
                color: #00ff00; 
                font-family: "Courier New", monospace;
                alternate-background-color: #303030;
                border: 1px solid #00ff00;
            }
            QListWidget::item:selected { 
                background-color: #008800; 
                color: #00ff00;
            }
            QStatusBar { 
                background-color: #000000; 
                color: #00ff00;
                border-top: 1px solid #00ff00;
            }
            QTabWidget::pane { 
                border: 1px solid #00ff00;
                background-color: #000000;
            }
            QTabBar::tab {
                background-color: #202020;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 5px 10px;
                font-family: "Courier New", monospace;
            }
            QTabBar::tab:selected {
                background-color: #008800;
            }
            QTabBar::tab:hover {
                background-color: #303030;
            }
            QGroupBox { 
                border: 1px solid #00ff00;
                margin-top: 20px;
                color: #00ff00;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
            QLineEdit {
                background-color: #202020;
                border: 1px solid #00ff00;
                color: #00ff00;
            }
            QSpinBox {
                background-color: #202020;
                border: 1px solid #00ff00;
                color: #00ff00;
            }
            QComboBox {
                background-color: #202020;
                border: 1px solid #00ff00;
                color: #00ff00;
                padding: 1px 18px 1px 3px;
            }
            QComboBox::drop-down {
                border: 1px solid #00ff00;
            }
        """)
        
        # Set terminal font
        terminal_font = QFont("Courier New", 10)
        app.setFont(terminal_font)
    
    def retro_pink_theme(self, window):
        """Apply retro pink (vaporwave) theme to the application."""
        palette = QPalette()
        app = QApplication.instance()
        
        # Set base colors (vaporwave pink theme)
        palette.setColor(QPalette.Window, QColor(25, 5, 25))  # Dark purple
        palette.setColor(QPalette.WindowText, QColor(255, 128, 255))  # Pink
        palette.setColor(QPalette.Base, QColor(40, 10, 40))  # Dark purple
        palette.setColor(QPalette.AlternateBase, QColor(60, 20, 60))  # Lighter purple
        palette.setColor(QPalette.ToolTipBase, QColor(25, 5, 25))  # Dark purple
        palette.setColor(QPalette.ToolTipText, QColor(255, 128, 255))  # Pink
        palette.setColor(QPalette.Text, QColor(255, 128, 255))  # Pink
        palette.setColor(QPalette.Button, QColor(128, 0, 128))  # Purple
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))  # White
        palette.setColor(QPalette.BrightText, QColor(0, 255, 255))  # Cyan
        palette.setColor(QPalette.Highlight, QColor(200, 0, 200))  # Bright purple
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))  # White
        
        # Apply palette
        app.setPalette(palette)
        
        # Set stylesheet for custom styles
        app.setStyleSheet("""
            QMainWindow { background-color: #19051a; }
            QLabel { color: #ff80ff; }
            QPushButton { 
                background-color: #800080; 
                border: 2px solid #00ffff; 
                border-radius: 4px; 
                padding: 5px; 
                color: #ffffff;
                font-family: "Arial", sans-serif;
                font-weight: bold;
            }
            QPushButton:hover { 
                background-color: #aa00aa;
                border: 2px solid #fff000;
            }
            QPushButton:pressed { background-color: #c800c8; }
            QSlider::handle { 
                background-color: #00ffff; 
                border-radius: 5px; 
                border: 1px solid #ffffff; 
            }
            QSlider::groove:horizontal {
                border: 1px solid #ff80ff;
                height: 8px;
                background: #400040;
                border-radius: 4px;
            }
            QToolButton { 
                background-color: #800080; 
                border: 2px solid #00ffff; 
                border-radius: 4px; 
                color: #ffffff;
            }
            QToolButton:hover { 
                background-color: #aa00aa;
                border: 2px solid #fff000;
            }
            QToolButton:pressed { background-color: #c800c8; }
            QListWidget { 
                background-color: #280a28; 
                alternate-background-color: #3c143c;
                color: #ff80ff; 
                border: 2px solid #800080;
                border-radius: 4px;
                font-family: "Arial", sans-serif;
            }
            QListWidget::item:selected { 
                background-color: #c800c8; 
                color: #ffffff;
            }
            QStatusBar { 
                background-color: #19051a; 
                color: #ff80ff;
                border-top: 1px solid #800080;
            }
            QTabWidget::pane { 
                border: 2px solid #800080;
                background-color: #19051a;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #400040;
                color: #ff80ff;
                border: 1px solid #800080;
                padding: 5px 10px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #800080;
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background-color: #600060;
            }
            QScrollBar:vertical {
                border: 1px solid #800080;
                background: #280a28;
                width: 15px;
                margin: 22px 0 22px 0;
            }
            QScrollBar::handle:vertical {
                background: #800080;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                border: 1px solid #800080;
                background: #400040;
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                border: 1px solid #800080;
                background: #400040;
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """)
        
        # Set fancy font
        fancy_font = QFont("Arial", 10)
        app.setFont(fancy_font)
