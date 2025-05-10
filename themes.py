"""
Theme management module
"""

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from ui.cassette_theme import CassetteTheme
from ui.vinyl_theme import VinylTheme

class ThemeManager(QObject):
    """
    Class to manage application themes
    """
    theme_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.themes = {}
        self.current_theme = None
        
        # Register built-in themes
        self._register_built_in_themes()
    
    def _register_built_in_themes(self):
        """Register the built-in themes"""
        # Register Cassette theme
        self.register_theme("Cassette Mode", CassetteTheme())
        
        # Register Vinyl theme
        self.register_theme("Vinyl View", VinylTheme())
        
        # Set default theme
        self.current_theme = "Cassette Mode"
    
    def register_theme(self, name, theme):
        """
        Register a new theme
        
        Args:
            name (str): Name of the theme
            theme: Theme object
        """
        self.themes[name] = theme
    
    def get_theme(self, name):
        """
        Get a theme by name
        
        Args:
            name (str): Name of the theme
            
        Returns:
            theme: The requested theme, or None if not found
        """
        return self.themes.get(name)
    
    def get_current_theme(self):
        """
        Get the current theme
        
        Returns:
            theme: The current theme
        """
        return self.themes.get(self.current_theme)
    
    def set_theme(self, name):
        """
        Set the current theme
        
        Args:
            name (str): Name of the theme to set
            
        Returns:
            bool: True if theme was set, False otherwise
        """
        if name in self.themes:
            self.current_theme = name
            self.theme_changed.emit(name)
            return True
        return False
    
    def get_theme_names(self):
        """
        Get the names of all registered themes
        
        Returns:
            list: List of theme names
        """
        return list(self.themes.keys())
    
    def apply_theme_to_widget(self, widget):
        """
        Apply the current theme to a widget
        
        Args:
            widget: Widget to apply the theme to
        """
        theme = self.get_current_theme()
        if theme:
            theme.apply_to_widget(widget)
