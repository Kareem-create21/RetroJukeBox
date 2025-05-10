"""
Playback controls module
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                           QSlider, QLabel, QCheckBox)
from PyQt5.QtCore import Qt

class PlaybackControls(QWidget):
    """Widget containing playback controls"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create layout
        main_layout = QVBoxLayout(self)
        
        # Main controls row
        controls_layout = QHBoxLayout()
        
        # Create buttons
        self.prevButton = QPushButton("⏮")
        self.prevButton.setObjectName("prevButton")
        self.prevButton.setToolTip("Previous Track")
        
        self.playButton = QPushButton("▶")
        self.playButton.setObjectName("playButton")
        self.playButton.setToolTip("Play")
        
        self.pauseButton = QPushButton("⏸")
        self.pauseButton.setObjectName("pauseButton")
        self.pauseButton.setToolTip("Pause/Resume")
        
        self.stopButton = QPushButton("⏹")
        self.stopButton.setObjectName("stopButton")
        self.stopButton.setToolTip("Stop")
        
        self.nextButton = QPushButton("⏭")
        self.nextButton.setObjectName("nextButton")
        self.nextButton.setToolTip("Next Track")
        
        # Add buttons to layout
        controls_layout.addStretch()
        controls_layout.addWidget(self.prevButton)
        controls_layout.addWidget(self.playButton)
        controls_layout.addWidget(self.pauseButton)
        controls_layout.addWidget(self.stopButton)
        controls_layout.addWidget(self.nextButton)
        controls_layout.addStretch()
        
        # Volume and options row
        volume_layout = QHBoxLayout()
        
        # Volume control
        volume_label = QLabel("Volume:")
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.setToolTip("Volume")
        
        # Shuffle and repeat checkboxes
        self.shuffleButton = QCheckBox("Shuffle")
        self.shuffleButton.setToolTip("Toggle Shuffle Mode")
        
        self.repeatButton = QCheckBox("Repeat")
        self.repeatButton.setToolTip("Toggle Repeat Mode")
        
        # Add volume controls to layout
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volumeSlider)
        volume_layout.addWidget(self.shuffleButton)
        volume_layout.addWidget(self.repeatButton)
        
        # Add layouts to main layout
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(volume_layout)

def create_playback_controls():
    """
    Factory function to create playback controls
    
    Returns:
        PlaybackControls: A widget with playback controls
    """
    return PlaybackControls()
