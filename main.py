#!/usr/bin/env python3
"""
RetroJukebox - A desktop music player with retro-styled UI themes
Main entry point for the application
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
from ui.main_window import MainWindow
from loading_screen import RetroLoadingScreen, SimpleLoadingScreen

def main():
    """
    Main function to initialize and run the application
    """
    # Set environment variables
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    
    # Check for platform-specific issues
    if sys.platform.startswith('linux'):
        # Try to use offscreen as most reliable option in containerized environments
        if 'QT_QPA_PLATFORM' not in os.environ:
            os.environ['QT_QPA_PLATFORM'] = 'offscreen'
            
    # For Windows systems
    elif sys.platform.startswith('win'):
        if 'QT_QPA_PLATFORM' not in os.environ:
            os.environ['QT_QPA_PLATFORM'] = 'windows'
            
    # For macOS systems
    elif sys.platform.startswith('darwin'):
        if 'QT_QPA_PLATFORM' not in os.environ:
            os.environ['QT_QPA_PLATFORM'] = 'cocoa'
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("RetroJukebox")
    app.setOrganizationName("RetroJukebox")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Application version
    app_version = "1.2.0"
    
    # Determine which loading screen to use based on system resources/arguments
    use_simple_loading = "--simple" in sys.argv or os.environ.get("SIMPLE_LOADING", "0") == "1"
    
    # Create and show the appropriate loading screen
    if use_simple_loading:
        loading_screen = SimpleLoadingScreen(app_name="RetroJukebox", version=app_version)
    else:
        loading_screen = RetroLoadingScreen(app_name="RetroJukebox", version=app_version)
    
    loading_screen.show()
    
    # Create the main window but don't show it yet
    window = MainWindow()
    
    # When the loading screen completes, show the main window and close the loading screen
    def on_loading_completed():
        window.show()
        loading_screen.close()
    
    # Connect loading screen completed signal
    loading_screen.completed.connect(on_loading_completed)
    
    # Run application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
