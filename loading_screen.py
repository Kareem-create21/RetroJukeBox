"""
Loading screen module with retro computer boot animation
"""

import time
import random
import sys
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QRect, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPalette, QFontDatabase
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar, 
    QSplashScreen, QGraphicsOpacityEffect
)

class BootText:
    """Class for managing boot sequence text elements"""
    def __init__(self, text, delay, color=Qt.green, is_command=False, blink=False):
        self.text = text
        self.delay = delay  # delay in milliseconds
        self.color = color
        self.is_command = is_command
        self.blink = blink
        self.completed = False
        self.current_text = ""
        self.char_index = 0
        self.visible = True  # For blinking

class RetroLoadingScreen(QWidget):
    """
    A nostalgic retro-style loading screen resembling an old computer boot sequence
    """
    completed = pyqtSignal()
    
    def __init__(self, parent=None, app_name="RetroJukebox", version="1.0"):
        super().__init__(parent)
        self.app_name = app_name
        self.version = version
        self.setWindowTitle("Starting " + app_name)
        self.setMinimumSize(600, 400)
        
        # Get screen dimensions and center the window
        screen_size = QApplication.desktop().screenGeometry()
        self.move((screen_size.width() - self.width()) // 2,
                 (screen_size.height() - self.height()) // 2)
        
        # Use a styled dark background
        self.setStyleSheet("""
            RetroLoadingScreen {
                background-color: #000000;
            }
            QProgressBar {
                border: 1px solid #4A4A4A;
                border-radius: 0px;
                text-align: center;
                background-color: #000000;
                color: #00FF00;
                font-family: "Courier New";
            }
            QProgressBar::chunk {
                background-color: #00AA00;
            }
        """)
        
        # Set monospace font
        font_id = QFontDatabase.addApplicationFont(":/fonts/courier.ttf")
        if font_id < 0:
            # Fallback to system monospace font
            self.font = QFont("Courier New", 10)
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family, 10)
        
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Set up the UI components"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Terminal-like container
        self.terminal = QLabel(self)
        self.terminal.setStyleSheet("background-color: #000000; color: #00FF00; border: 1px solid #333;")
        self.terminal.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.terminal.setFont(self.font)
        self.terminal.setTextFormat(Qt.RichText)
        self.terminal.setWordWrap(True)
        self.terminal.setText("")
        
        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setFont(self.font)
        self.progress_bar.setFormat("Loading: %p%")
        
        # Status label
        self.status_label = QLabel("Initializing system...", self)
        self.status_label.setStyleSheet("color: #00FF00;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(self.font)
        
        # Add widgets to layout
        layout.addWidget(self.terminal, 1)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Boot sequence text
        self.boot_sequence = [
            BootText("RETRO SYSTEM BIOS v2.8", 300),
            BootText("Copyright (c) 1982-2025", 300),
            BootText("", 300),  # Empty line
            BootText("PERFORMING SYSTEM CHECK...", 500),
            BootText("MEMORY TEST: OK", 400),
            BootText("SOUND SYSTEM: INITIALIZED", 400),
            BootText("GRAPHICS SUBSYSTEM: INITIALIZED", 400),
            BootText("FILE SYSTEM: MOUNTED", 400),
            BootText("", 200),  # Empty line
            BootText("> LOAD RETROMUSIC.SYS", 300, is_command=True),
            BootText("LOADING AUDIO DRIVERS...", 800),
            BootText("INITIALIZING AUDIO PLUGINS...", 800),
            BootText("SCANNING MUSIC LIBRARY...", 800),
            BootText("", 200),  # Empty line
            BootText(f"STARTING {self.app_name} v{self.version}", 500, color=Qt.yellow),
            BootText("WELCOME TO THE NOSTALGIC ERA OF MUSIC", 600, color=Qt.yellow),
            BootText("", 200),  # Empty line
            BootText("SYSTEM READY", 300, color=Qt.cyan, blink=True)
        ]
        
        self.current_boot_index = 0
        self.current_text_timer = QTimer(self)
        self.current_text_timer.timeout.connect(self.update_boot_text)
        
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_blinking_text)
        self.blink_timer.start(500)  # Blink every 500ms
        
        # Start processing
        self.current_text_timer.start(50)  # Update every 50ms

    def setup_animations(self):
        """Set up animations for UI elements"""
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(100)  # Update every 100ms
        
        # For random "processing" messages
        self.status_messages = [
            "Rewinding cassette tapes...",
            "Dusting off vinyl records...",
            "Calibrating equalizer...",
            "Adjusting tape heads...",
            "Connecting to music database...",
            "Loading visualization modules...",
            "Tuning radio frequencies...",
            "Optimizing playback engine...",
        ]
        
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1500)  # Update every 1.5 seconds
    
    def update_boot_text(self):
        """Update the boot sequence text with typing effect"""
        if self.current_boot_index >= len(self.boot_sequence):
            self.current_text_timer.stop()
            return
        
        current_boot_item = self.boot_sequence[self.current_boot_index]
        
        # If this item is not yet started or waiting for its delay
        if current_boot_item.char_index == 0:
            time.sleep(current_boot_item.delay / 1000)  # Convert ms to seconds
        
        if current_boot_item.char_index < len(current_boot_item.text):
            # Still typing out this line
            current_boot_item.char_index += 1
            current_boot_item.current_text = current_boot_item.text[:current_boot_item.char_index]
            self.update_terminal_text()
        else:
            # Line is complete
            current_boot_item.completed = True
            self.current_boot_index += 1
            
            # If we're done with all text, emit completed signal
            if self.current_boot_index >= len(self.boot_sequence):
                QTimer.singleShot(1000, self.completed.emit)
    
    def update_terminal_text(self):
        """Update the terminal text display"""
        html_text = ""
        
        for i, boot_item in enumerate(self.boot_sequence[:self.current_boot_index + 1]):
            text = boot_item.current_text
            
            # Apply text color
            color_hex = self.qt_color_to_hex(boot_item.color)
            
            # Special formatting for command
            if boot_item.is_command:
                text = f"<span style='color: #FFFFFF;'>{text}</span>"
            else:
                text = f"<span style='color: {color_hex};'>{text}</span>"
            
            # Add blinking effect if needed and item is completely typed
            if boot_item.blink and boot_item.completed and not boot_item.visible:
                text = ""
            
            # Add the text with a line break
            html_text += text + "<br>"
        
        self.terminal.setText(html_text)
    
    def toggle_blinking_text(self):
        """Toggle visibility of blinking text elements"""
        changed = False
        
        for boot_item in self.boot_sequence:
            if boot_item.blink and boot_item.completed:
                boot_item.visible = not boot_item.visible
                changed = True
        
        if changed:
            self.update_terminal_text()
    
    def update_progress(self):
        """Update the progress bar value"""
        current_value = self.progress_bar.value()
        
        # Calculate target value based on boot sequence progress
        if self.current_boot_index < len(self.boot_sequence):
            target_value = int((self.current_boot_index / len(self.boot_sequence)) * 100)
        else:
            target_value = 100
        
        # Move toward target value gradually
        if current_value < target_value:
            self.progress_bar.setValue(current_value + 1)
        
        # If we're done, stop the timer
        if current_value >= 100:
            self.progress_timer.stop()
    
    def update_status(self):
        """Update the status message with random "processing" messages"""
        if self.progress_bar.value() < 100:
            self.status_label.setText(random.choice(self.status_messages))
        else:
            self.status_label.setText("Ready to launch!")
            self.status_timer.stop()
    
    def qt_color_to_hex(self, color):
        """Convert Qt color to hex string for HTML"""
        if color == Qt.green:
            return "#00FF00"
        elif color == Qt.yellow:
            return "#FFFF00"
        elif color == Qt.red:
            return "#FF0000"
        elif color == Qt.cyan:
            return "#00FFFF"
        elif color == Qt.white:
            return "#FFFFFF"
        else:
            return "#00FF00"  # Default to green

    def paintEvent(self, event):
        """Override paint event for custom drawing"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw scan lines effect
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 30)))
        
        for y in range(0, self.height(), 2):
            painter.drawRect(0, y, self.width(), 1)
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.current_text_timer.stop()
        self.progress_timer.stop()
        self.status_timer.stop()
        self.blink_timer.stop()
        super().closeEvent(event)


# Stand-alone test function
class SimpleLoadingScreen(QWidget):
    """
    A simpler version of the loading screen for systems with limited resources
    """
    completed = pyqtSignal()
    
    def __init__(self, parent=None, app_name="RetroJukebox", version="1.0"):
        super().__init__(parent)
        self.app_name = app_name
        self.version = version
        self.setWindowTitle("Starting " + app_name)
        self.setMinimumSize(400, 250)
        
        # Set styles
        self.setStyleSheet("""
            SimpleLoadingScreen {
                background-color: #000000;
                color: #00FF00;
            }
            QProgressBar {
                border: 1px solid #4A4A4A;
                border-radius: 0px;
                text-align: center;
                background-color: #000000;
                color: #00FF00;
            }
            QProgressBar::chunk {
                background-color: #00AA00;
            }
            QLabel {
                color: #00FF00;
                font-family: "Courier New";
            }
        """)
        
        # Layout
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel(f"{app_name} v{version}", self)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        
        # Boot message
        self.message = QLabel("Initializing system...", self)
        self.message.setAlignment(Qt.AlignCenter)
        
        # Progress bar
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        
        # Status label
        self.status = QLabel("Please wait...", self)
        self.status.setAlignment(Qt.AlignCenter)
        
        # Add widgets to layout
        layout.addWidget(header)
        layout.addSpacing(20)
        layout.addWidget(self.message)
        layout.addSpacing(20)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)
        layout.addStretch()
        
        # Set up timers
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)
        
        self.message_timer = QTimer(self)
        self.message_timer.timeout.connect(self.update_message)
        self.message_timer.start(1000)
        
        # Boot messages
        self.boot_messages = [
            "Initializing system...",
            "Loading audio drivers...",
            "Starting playback engine...",
            "Scanning music library...",
            "Preparing user interface...",
            f"Starting {app_name}...",
            "Ready to launch!"
        ]
        self.current_message = 0
    
    def update_progress(self):
        """Update the progress bar"""
        current = self.progress.value()
        if current < 100:
            self.progress.setValue(current + 1)
        else:
            self.timer.stop()
            self.completed.emit()
    
    def update_message(self):
        """Update the boot message"""
        if self.current_message < len(self.boot_messages):
            self.message.setText(self.boot_messages[self.current_message])
            self.current_message += 1
            
            # Update status with a more detailed message
            progress = self.progress.value()
            if progress < 30:
                self.status.setText("Loading core components...")
            elif progress < 60:
                self.status.setText("Initializing audio subsystem...")
            elif progress < 90:
                self.status.setText("Preparing user interface...")
            else:
                self.status.setText("Almost ready...")


def test_loading_screen():
    app = QApplication(sys.argv)
    
    # Determine which loading screen to use based on system resources
    # This is just a placeholder - you might want to check actual system specs
    use_simple = "--simple" in sys.argv
    
    if use_simple:
        loading = SimpleLoadingScreen()
    else:
        loading = RetroLoadingScreen()
        
    loading.completed.connect(loading.close)
    loading.show()
    
    return app.exec_()

if __name__ == "__main__":
    test_loading_screen()