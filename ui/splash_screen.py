from PyQt5.QtWidgets import QSplashScreen, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QColor, QPainter, QLinearGradient

class RetroSplashScreen(QSplashScreen):
    """A retro-themed splash screen with loading progress bar."""
    
    # Signal to notify when loading is complete
    finished = pyqtSignal()
    
    def __init__(self):
        """Initialize the splash screen."""
        # Create a retro pixmap for the splash screen
        pixmap = QPixmap(500, 300)
        pixmap.fill(Qt.black)
        super().__init__(pixmap)
        
        # Setup the layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        self.title_label = QLabel("Retro MP3 Player")
        self.title_label.setStyleSheet("""
            color: #0f0;
            font-family: 'Courier New', monospace;
            font-size: 28px;
            font-weight: bold;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # Subtitle
        self.subtitle_label = QLabel("Loading the nostalgia...")
        self.subtitle_label.setStyleSheet("""
            color: #0f0;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        """)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        
        # Version
        self.version_label = QLabel("v1.0.0")
        self.version_label.setStyleSheet("""
            color: #0f0;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        """)
        self.version_label.setAlignment(Qt.AlignRight)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #0f0;
                border-radius: 5px;
                text-align: center;
                color: #0f0;
                background-color: #000;
                font-family: 'Courier New', monospace;
            }
            QProgressBar::chunk {
                background-color: #0f0;
            }
        """)
        
        # Status message
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet("""
            color: #0f0;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # Add widgets to layout
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.subtitle_label)
        self.layout.addStretch()
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.version_label)
        
        # Create a container widget
        self.container = QWidget()
        self.container.setLayout(self.layout)
        
        # Set up animation timers
        self.loading_timer = QTimer(self)
        self.loading_timer.timeout.connect(self.update_progress)
        
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status)
        
        self.progress_value = 0
        self.status_index = 0
        self.status_messages = [
            "Initializing...",
            "Loading audio engine...",
            "Loading user interface...",
            "Preparing playlist manager...",
            "Loading theme engine...",
            "Configuring audio visualizer...",
            "Almost ready...",
            "Welcome to the 80s!"
        ]
    
    def drawContents(self, painter):
        """Draw the splash screen contents."""
        # Draw a retro grid background
        self.draw_retro_background(painter)
        
        # Draw the container with all widgets
        self.container.setGeometry(0, 0, self.width(), self.height())
        self.container.render(painter)
    
    def draw_retro_background(self, painter):
        """Draw a retro grid background."""
        painter.fillRect(self.rect(), Qt.black)
        
        # Draw horizontal lines
        pen = painter.pen()
        pen.setColor(QColor(0, 128, 0, 40))  # Transparent green
        pen.setWidth(1)
        painter.setPen(pen)
        
        for y in range(0, self.height(), 10):
            painter.drawLine(0, y, self.width(), y)
        
        # Draw vertical lines
        for x in range(0, self.width(), 10):
            painter.drawLine(x, 0, x, self.height())
        
        # Draw a glowing horizontal line
        gradient = QLinearGradient(0, self.height() // 2, self.width(), self.height() // 2)
        gradient.setColorAt(0, QColor(0, 255, 0, 0))
        gradient.setColorAt(0.5, QColor(0, 255, 0, 128))
        gradient.setColorAt(1, QColor(0, 255, 0, 0))
        
        pen.setColor(QColor(0, 255, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(gradient)
        
        y = self.height() // 2
        painter.drawLine(0, y, self.width(), y)
    
    def start_loading(self):
        """Start the loading animation."""
        self.loading_timer.start(80)  # Update progress every 80ms
        self.status_timer.start(1500)  # Update status message every 1.5s
    
    def update_progress(self):
        """Update the progress bar."""
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        
        # Refresh the splash screen
        self.repaint()
        
        # When loading completes
        if self.progress_value >= 100:
            self.loading_timer.stop()
            self.status_timer.stop()
            self.finished.emit()
    
    def update_status(self):
        """Update the status message."""
        if self.status_index < len(self.status_messages):
            self.status_label.setText(self.status_messages[self.status_index])
            self.status_index += 1
            self.repaint()