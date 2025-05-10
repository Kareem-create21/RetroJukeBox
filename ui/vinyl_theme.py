"""
Vinyl theme implementation
"""

from PyQt5.QtGui import QPalette, QColor, QBrush, QLinearGradient, QFont
from PyQt5.QtCore import Qt

class VinylTheme:
    """
    Vinyl record-style theme implementation
    """
    
    def __init__(self):
        # Define theme colors
        self.primary_color = QColor(25, 25, 30)        # Very dark blue-gray
        self.secondary_color = QColor(45, 45, 50)      # Dark blue-gray
        self.accent_color = QColor(70, 130, 180)       # Steel blue
        self.text_color = QColor(220, 220, 220)        # Light gray
        self.highlight_color = QColor(100, 149, 237)   # Cornflower blue
        self.background_color = QColor(20, 20, 25)     # Almost black with blue tint
        
        # Define fonts
        self.heading_font = QFont("Arial", 12, QFont.Bold)
        self.normal_font = QFont("Arial", 10)
        self.small_font = QFont("Arial", 9)
        
        # Define stylesheet components
        self._init_stylesheet()
    
    def _init_stylesheet(self):
        """Initialize the stylesheet for this theme"""
        # Convert colors to hexadecimal strings
        primary = self.primary_color.name()
        secondary = self.secondary_color.name()
        accent = self.accent_color.name()
        text = self.text_color.name()
        highlight = self.highlight_color.name()
        background = self.background_color.name()
        
        # Main stylesheet
        self.stylesheet = f"""
        /* Main Window */
        QMainWindow, QDialog {{
            background-color: {background};
            color: {text};
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {primary};
            color: {text};
            border-bottom: 1px solid {secondary};
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 8px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {secondary};
            color: {highlight};
        }}
        
        QMenu {{
            background-color: {primary};
            color: {text};
            border: 1px solid {secondary};
        }}
        
        QMenu::item:selected {{
            background-color: {secondary};
            color: {highlight};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {primary};
            color: {text};
            border: 1px solid {accent};
            border-radius: 15px;
            padding: 5px 10px;
            min-width: 80px;
        }}
        
        QPushButton:hover {{
            background-color: {secondary};
            color: {highlight};
            border: 1px solid {highlight};
        }}
        
        QPushButton:pressed {{
            background-color: {secondary};
            border: 2px solid {highlight};
        }}
        
        /* Playback control buttons - circular like vinyl records */
        QPushButton#playButton, QPushButton#pauseButton, QPushButton#stopButton, 
        QPushButton#prevButton, QPushButton#nextButton {{
            background-color: {primary};
            border: 2px solid {accent};
            border-radius: 20px;
            padding: 5px;
            min-width: 40px;
            min-height: 40px;
        }}
        
        QPushButton#playButton:hover, QPushButton#pauseButton:hover, QPushButton#stopButton:hover,
        QPushButton#prevButton:hover, QPushButton#nextButton:hover {{
            background-color: {secondary};
            border: 2px solid {highlight};
        }}
        
        /* List and Tree Views */
        QListView, QTreeView, QTableView {{
            background-color: {primary};
            color: {text};
            alternate-background-color: {secondary};
            border: 1px solid {accent};
            border-radius: 5px;
        }}
        
        QListView::item:selected, QTreeView::item:selected, QTableView::item:selected {{
            background-color: {accent};
            color: {text};
        }}
        
        /* Sliders - styled like tone arm */
        QSlider::groove:horizontal {{
            border: 1px solid {accent};
            height: 8px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                      stop:0 {primary}, stop:1 {secondary});
            margin: 2px 0;
            border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
            background: {accent};
            border: 1px solid {highlight};
            width: 18px;
            height: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }}
        
        QSlider::handle:horizontal:hover {{
            background: {highlight};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {accent};
            border-radius: 5px;
            text-align: center;
            background-color: {primary};
            color: {text};
        }}
        
        QProgressBar::chunk {{
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 {accent}, stop:1 {highlight});
            width: 20px;
            border-radius: 5px;
        }}
        
        /* Labels */
        QLabel {{
            color: {text};
        }}
        
        QLabel#trackTitleLabel, QLabel#artistLabel {{
            color: {highlight};
            font-weight: bold;
        }}
        
        /* Vinyl-specific elements */
        QFrame#vinylFrame {{
            background-color: {primary};
            border: 2px solid {accent};
            border-radius: 150px; /* Make it circular */
        }}
        
        QLabel#albumLabel {{
            border: 1px solid {accent};
            border-radius: 75px;
            background-color: {secondary};
        }}
        
        /* Scroll Bars */
        QScrollBar:vertical {{
            border: 1px solid {accent};
            background: {primary};
            width: 12px;
            margin: 16px 0 16px 0;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {accent};
            min-height: 20px;
            border-radius: 6px;
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: 1px solid {accent};
            background: {primary};
            height: 15px;
            border-radius: 6px;
        }}
        
        QScrollBar:horizontal {{
            border: 1px solid {accent};
            background: {primary};
            height: 12px;
            margin: 0 16px 0 16px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {accent};
            min-width: 20px;
            border-radius: 6px;
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            border: 1px solid {accent};
            background: {primary};
            width: 15px;
            border-radius: 6px;
        }}
        
        /* Tab Widget */
        QTabWidget {{
            border: 1px solid {accent};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {accent};
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            border-bottom-left-radius: 5px;
        }}
        
        QTabBar::tab {{
            background-color: {primary};
            color: {text};
            border: 1px solid {accent};
            border-bottom: none;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            min-width: 8ex;
            padding: 5px 10px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {secondary};
            color: {highlight};
        }}
        
        QTabBar::tab:hover {{
            background-color: {secondary};
        }}
        """
    
    def apply_to_widget(self, widget):
        """
        Apply the theme to a widget
        
        Args:
            widget: Widget to apply the theme to
        """
        # Set palette
        palette = QPalette()
        
        # General colors
        palette.setColor(QPalette.Window, self.background_color)
        palette.setColor(QPalette.WindowText, self.text_color)
        palette.setColor(QPalette.Base, self.primary_color)
        palette.setColor(QPalette.AlternateBase, self.secondary_color)
        palette.setColor(QPalette.ToolTipBase, self.primary_color)
        palette.setColor(QPalette.ToolTipText, self.text_color)
        
        # Button colors
        palette.setColor(QPalette.Button, self.primary_color)
        palette.setColor(QPalette.ButtonText, self.text_color)
        
        # Highlight colors
        palette.setColor(QPalette.Highlight, self.accent_color)
        palette.setColor(QPalette.HighlightedText, self.text_color)
        
        # Link colors
        palette.setColor(QPalette.Link, self.accent_color)
        palette.setColor(QPalette.LinkVisited, self.highlight_color)
        
        # Apply palette
        widget.setPalette(palette)
        
        # Apply stylesheet
        widget.setStyleSheet(self.stylesheet)
        
        # Set fonts
        widget.setFont(self.normal_font)
    
    def get_vinyl_svg(self):
        """
        Get SVG code for vinyl record graphic
        
        Returns:
            str: SVG code for vinyl record
        """
        # Vinyl record SVG - uses colors from the theme
        primary = self.primary_color.name()
        secondary = self.secondary_color.name()
        accent = self.accent_color.name()
        highlight = self.highlight_color.name()
        
        svg_code = f'''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
            <!-- Vinyl Record -->
            <circle cx="150" cy="150" r="145" fill="{primary}" stroke="{accent}" stroke-width="2"/>
            
            <!-- Outer Groove -->
            <circle cx="150" cy="150" r="140" fill="none" stroke="{accent}" stroke-width="1"/>
            
            <!-- Middle Groove -->
            <circle cx="150" cy="150" r="100" fill="none" stroke="{accent}" stroke-width="1"/>
            
            <!-- Inner Groove -->
            <circle cx="150" cy="150" r="60" fill="none" stroke="{accent}" stroke-width="1"/>
            
            <!-- Record Grooves - simplified representation -->
            <circle cx="150" cy="150" r="135" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="130" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="125" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="120" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="115" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="110" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="105" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="95" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="90" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="85" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="80" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="75" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="70" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            <circle cx="150" cy="150" r="65" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="0.5"/>
            
            <!-- Label Area -->
            <circle cx="150" cy="150" r="50" fill="{secondary}" stroke="{accent}" stroke-width="2"/>
            
            <!-- Center Hole -->
            <circle cx="150" cy="150" r="7" fill="{highlight}" stroke="{accent}" stroke-width="1"/>
        </svg>
        '''
        
        return svg_code
