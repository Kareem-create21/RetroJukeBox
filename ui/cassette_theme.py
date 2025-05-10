"""
Cassette theme implementation
"""

from PyQt5.QtGui import QPalette, QColor, QBrush, QLinearGradient, QFont
from PyQt5.QtCore import Qt

class CassetteTheme:
    """
    Cassette-style theme implementation
    """
    
    def __init__(self):
        # Define theme colors
        self.primary_color = QColor(45, 45, 45)        # Dark gray
        self.secondary_color = QColor(65, 65, 65)      # Medium gray
        self.accent_color = QColor(255, 165, 0)        # Orange
        self.text_color = QColor(220, 220, 220)        # Light gray
        self.highlight_color = QColor(255, 200, 0)     # Amber
        self.background_color = QColor(30, 30, 30)     # Very dark gray
        
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
            border: 1px solid {secondary};
            border-radius: 5px;
            padding: 5px 10px;
            min-width: 80px;
        }}
        
        QPushButton:hover {{
            background-color: {secondary};
            color: {highlight};
        }}
        
        QPushButton:pressed {{
            background-color: {secondary};
            border: 2px solid {accent};
        }}
        
        /* Playback control buttons */
        QPushButton#playButton, QPushButton#pauseButton, QPushButton#stopButton, 
        QPushButton#prevButton, QPushButton#nextButton {{
            background-color: {primary};
            border: 2px solid {accent};
            border-radius: 15px;
            padding: 5px;
            min-width: 30px;
            min-height: 30px;
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
            border: 1px solid {secondary};
            border-radius: 3px;
        }}
        
        QListView::item:selected, QTreeView::item:selected, QTableView::item:selected {{
            background-color: {accent};
            color: {background};
        }}
        
        /* Sliders */
        QSlider::groove:horizontal {{
            border: 1px solid {secondary};
            height: 8px;
            background: {primary};
            margin: 2px 0;
            border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
            background: {accent};
            border: 1px solid {secondary};
            width: 14px;
            height: 14px;
            margin: -4px 0;
            border-radius: 7px;
        }}
        
        QSlider::handle:horizontal:hover {{
            background: {highlight};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {secondary};
            border-radius: 5px;
            text-align: center;
            background-color: {primary};
            color: {text};
        }}
        
        QProgressBar::chunk {{
            background-color: {accent};
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
        
        /* Cassette-specific elements */
        QFrame#cassetteFrame {{
            background-color: {primary};
            border: 2px solid {accent};
            border-radius: 10px;
        }}
        
        QWidget#spoolWidget {{
            background-color: {background};
            border: 1px solid {secondary};
            border-radius: 25px;
        }}
        
        /* Scroll Bars */
        QScrollBar:vertical {{
            border: 1px solid {secondary};
            background: {primary};
            width: 12px;
            margin: 16px 0 16px 0;
            border-radius: 3px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {secondary};
            min-height: 20px;
            border-radius: 2px;
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: 1px solid {secondary};
            background: {primary};
            height: 15px;
            border-radius: 3px;
        }}
        
        QScrollBar:horizontal {{
            border: 1px solid {secondary};
            background: {primary};
            height: 12px;
            margin: 0 16px 0 16px;
            border-radius: 3px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {secondary};
            min-width: 20px;
            border-radius: 2px;
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            border: 1px solid {secondary};
            background: {primary};
            width: 15px;
            border-radius: 3px;
        }}
        
        /* Tab Widget */
        QTabWidget {{
            border: 1px solid {secondary};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {secondary};
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
            border-bottom-left-radius: 3px;
        }}
        
        QTabBar::tab {{
            background-color: {primary};
            color: {text};
            border: 1px solid {secondary};
            border-bottom: none;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
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
        palette.setColor(QPalette.HighlightedText, self.background_color)
        
        # Link colors
        palette.setColor(QPalette.Link, self.accent_color)
        palette.setColor(QPalette.LinkVisited, self.highlight_color)
        
        # Apply palette
        widget.setPalette(palette)
        
        # Apply stylesheet
        widget.setStyleSheet(self.stylesheet)
        
        # Set fonts
        widget.setFont(self.normal_font)
    
    def get_cassette_svg(self):
        """
        Get SVG code for cassette graphic
        
        Returns:
            str: SVG code for cassette
        """
        # Cassette tape SVG - uses colors from the theme
        primary = self.primary_color.name()
        secondary = self.secondary_color.name()
        accent = self.accent_color.name()
        
        svg_code = f'''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 230">
            <!-- Cassette Body -->
            <rect x="10" y="10" width="380" height="210" rx="15" ry="15" fill="{primary}" stroke="{accent}" stroke-width="3"/>
            
            <!-- Label Area -->
            <rect x="40" y="30" width="320" height="80" rx="5" ry="5" fill="{secondary}" stroke="{accent}" stroke-width="2"/>
            
            <!-- Tape Window -->
            <rect x="80" y="120" width="240" height="60" rx="5" ry="5" fill="{secondary}" stroke="{accent}" stroke-width="2"/>
            
            <!-- Spools -->
            <circle cx="140" cy="150" r="30" fill="{primary}" stroke="{accent}" stroke-width="2"/>
            <circle cx="260" cy="150" r="30" fill="{primary}" stroke="{accent}" stroke-width="2"/>
            
            <!-- Sprocket Holes -->
            <circle cx="140" cy="150" r="5" fill="{accent}"/>
            <circle cx="260" cy="150" r="5" fill="{accent}"/>
            
            <!-- Tape Visible Between Spools -->
            <path d="M170,150 L230,150" stroke="{accent}" stroke-width="3"/>
            
            <!-- Write Protection Tabs -->
            <rect x="40" y="190" width="20" height="10" rx="2" ry="2" fill="{accent}"/>
            <rect x="340" y="190" width="20" height="10" rx="2" ry="2" fill="{accent}"/>
        </svg>
        '''
        
        return svg_code
