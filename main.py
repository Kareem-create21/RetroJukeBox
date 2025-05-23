#!/usr/bin/env python3
<<<<<<< HEAD

import sys
import os
import argparse
import time
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from ui.main_window import RetroPlayerWindow
from ui.splash_screen import RetroSplashScreen
from ui.retro_style import RetroStyle

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Retro MP3 Player')
    parser.add_argument('command', nargs='?', choices=['play', 'pause', 'next', 'previous'],
                        help='Command to execute')
    parser.add_argument('--file', help='MP3 file to play')
    parser.add_argument('--no-splash', action='store_true', help='Skip splash screen')
    parser.add_argument('--theme', choices=['green', 'blue', 'pink'], default='green',
                       help='Choose a theme (default: green)')
    return parser.parse_args()

def handle_command_line(app, player, args):
    """Handle command line arguments."""
    if args.command == 'play':
        player.play_button_clicked()
    elif args.command == 'pause':
        player.pause_button_clicked()
    elif args.command == 'next':
        player.next_track()
    elif args.command == 'previous':
        player.previous_track()
    
    if args.file and os.path.exists(args.file):
        player.add_file_to_playlist(args.file)
        player.play_button_clicked()

def main():
    """Main entry point for the application."""
    # Create application
    app = QApplication(sys.argv)
    args = parse_args()
    
    # Set application name and organization for settings
    app.setApplicationName("RetroMP3Player")
    app.setOrganizationName("RetroPlayer")
    
    # Apply retro style based on theme argument
    theme_map = {
        'green': 'retro_green',
        'blue': 'retro_blue',
        'pink': 'retro_pink'
    }
    
    theme = theme_map.get(args.theme, 'retro_green')
    style = RetroStyle(theme)
    app.setStyle(style)
    style.apply_retro_palette(app)
    
    # Create the player window (but don't show it yet)
    player = RetroPlayerWindow()
    
    # Show splash screen if not disabled
    if not args.no_splash and not (args.command or args.file):
        splash = RetroSplashScreen()
        splash.show()
        
        # Start the loading animation
        splash.start_loading()
        
        # When splash screen finishes, show the main window
        def on_splash_finished():
            splash.finish(player)
            player.show()
            
            # Handle command line arguments if provided
            if args.command or args.file:
                handle_command_line(app, player, args)
        
        splash.finished.connect(on_splash_finished)
        
    else:
        # No splash screen, show window directly
        player.show()
        
        # Handle command line arguments if provided
        if args.command or args.file:
            handle_command_line(app, player, args)
    
    # Start the application event loop
=======
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
>>>>>>> 7931bac3b70b4ade7d98445fc1a06d706a28aa92
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
