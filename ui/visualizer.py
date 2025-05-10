from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QLinearGradient
from PyQt5.QtCore import Qt, QRect, QPoint

class AudioVisualizer(QWidget):
    """Simple audio visualizer widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(60)
        self.spectrum_data = []
        self.bar_count = 32  # Number of bars to display
        self.setStyleSheet("background-color: #222;")
    
    def update_spectrum(self, data):
        """Update the spectrum data."""
        # If provided data is smaller than bar_count, repeat it
        if len(data) < self.bar_count:
            multiplier = (self.bar_count // len(data)) + 1
            self.spectrum_data = (data * multiplier)[:self.bar_count]
        else:
            # If data is larger, use a subset or average it
            self.spectrum_data = data[:self.bar_count]
        
        # Make sure we have valid data
        if not self.spectrum_data:
            self.spectrum_data = [0] * self.bar_count
        
        # Repaint the widget
        self.update()
    
    def clear(self):
        """Clear the visualizer."""
        self.spectrum_data = [0] * self.bar_count
        self.update()
    
    def paintEvent(self, event):
        """Paint the visualizer."""
        if not self.spectrum_data:
            self.spectrum_data = [0] * self.bar_count
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        painter.fillRect(event.rect(), QColor('#222'))
        
        # Draw bars
        bar_width = self.width() / (self.bar_count * 1.5)
        bar_spacing = (self.width() - (bar_width * self.bar_count)) / (self.bar_count + 1)
        max_height = self.height() * 0.9  # Leave some space at top and bottom
        
        # Create gradient for bars
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 50, 50))    # Red at top
        gradient.setColorAt(0.5, QColor(255, 255, 50))  # Yellow in middle
        gradient.setColorAt(1, QColor(50, 255, 50))    # Green at bottom
        
        # Draw each bar
        x = bar_spacing
        for i, value in enumerate(self.spectrum_data):
            # Scale value to height
            bar_height = max_height * min(1.0, max(0.05, value))
            
            # Draw bar
            bar_rect = QRect(
                int(x), 
                int(self.height() - bar_height), 
                int(bar_width), 
                int(bar_height)
            )
            
            painter.fillRect(bar_rect, gradient)
            
            # Mirror the bar for retro effect
            mirror_rect = QRect(
                int(x),
                int(0),
                int(bar_width),
                int(bar_height * 0.3)  # Mirror is smaller
            )
            
            mirror_gradient = QLinearGradient(0, 0, 0, bar_height * 0.3)
            mirror_gradient.setColorAt(0, QColor(50, 255, 50, 100))  # Transparent green at top
            mirror_gradient.setColorAt(1, QColor(255, 50, 50, 20))   # Very transparent red at bottom
            
            painter.fillRect(mirror_rect, mirror_gradient)
            
            # Move to next bar position
            x += bar_width + bar_spacing
    
    def resizeEvent(self, event):
        """Handle resize event."""
        super().resizeEvent(event)
        self.update()  # Redraw when resized
