from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QSlider, 
                           QLabel, QToolButton, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer
import os

class PlayerControls(QWidget):
    """Widget containing the media player controls."""
    
    def __init__(self, player):
        super().__init__()
        
        self.player = player
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        # Create layout
        controls_layout = QHBoxLayout(self)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create control buttons
        self.play_pause_button = QToolButton()
        self.play_pause_button.setIconSize(QSize(48, 48))
        self.play_pause_button.setToolTip("Play/Pause")
        self.play_pause_button.clicked.connect(self.play_pause_clicked)
        
        self.stop_button = QToolButton()
        self.stop_button.setIconSize(QSize(32, 32))
        self.stop_button.setToolTip("Stop")
        self.stop_button.clicked.connect(self.stop_clicked)
        
        self.previous_button = QToolButton()
        self.previous_button.setIconSize(QSize(32, 32))
        self.previous_button.setToolTip("Previous")
        self.previous_button.clicked.connect(self.previous_clicked)
        
        self.next_button = QToolButton()
        self.next_button.setIconSize(QSize(32, 32))
        self.next_button.setToolTip("Next")
        self.next_button.clicked.connect(self.next_clicked)
        
        # Create shuffle and repeat buttons
        self.shuffle_button = QToolButton()
        self.shuffle_button.setIconSize(QSize(24, 24))
        self.shuffle_button.setToolTip("Shuffle")
        self.shuffle_button.setCheckable(True)
        self.shuffle_button.clicked.connect(self.shuffle_clicked)
        
        self.repeat_button = QToolButton()
        self.repeat_button.setIconSize(QSize(24, 24))
        self.repeat_button.setToolTip("Repeat")
        self.repeat_button.setCheckable(True)
        self.repeat_button.clicked.connect(self.repeat_clicked)
        
        # Volume controls
        self.mute_button = QToolButton()
        self.mute_button.setIconSize(QSize(24, 24))
        self.mute_button.setToolTip("Mute")
        self.mute_button.setCheckable(True)
        self.mute_button.clicked.connect(self.mute_clicked)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)  # Default volume
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.setToolTip("Volume")
        self.volume_slider.valueChanged.connect(self.volume_changed)
        
        # Speed control
        self.speed_label = QLabel("Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(50, 200)  # 0.5x to 2.0x
        self.speed_slider.setValue(100)  # Default 1.0x
        self.speed_slider.setFixedWidth(80)
        self.speed_slider.setToolTip("Playback Speed")
        self.speed_slider.valueChanged.connect(self.speed_changed)
        
        self.speed_value_label = QLabel("1.0x")
        self.speed_value_label.setFixedWidth(30)
        
        # Set button icons
        self.update_icons()
        
        # Add widgets to layout
        controls_layout.addWidget(self.shuffle_button)
        controls_layout.addWidget(self.previous_button)
        controls_layout.addWidget(self.play_pause_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.next_button)
        controls_layout.addWidget(self.repeat_button)
        controls_layout.addStretch(1)
        controls_layout.addWidget(self.mute_button)
        controls_layout.addWidget(self.volume_slider)
        controls_layout.addStretch(1)
        controls_layout.addWidget(self.speed_label)
        controls_layout.addWidget(self.speed_slider)
        controls_layout.addWidget(self.speed_value_label)
        
        # Set initial play button state
        self.update_controls(QMediaPlayer.StoppedState)
    
    def update_icons(self):
        """Update button icons from the assets directory."""
        # Create simple text-based icons as a fallback
        self.play_pause_button.setText("▶")
        self.stop_button.setText("■")
        self.previous_button.setText("◀◀")
        self.next_button.setText("▶▶")
        self.shuffle_button.setText("🔀")
        self.repeat_button.setText("🔁")
        self.mute_button.setText("🔊")
    
    def update_controls(self, state):
        """Update control buttons based on player state."""
        if state == QMediaPlayer.PlayingState:
            self.play_pause_button.setText("❚❚")  # Pause icon
            self.play_pause_button.setToolTip("Pause")
        else:
            self.play_pause_button.setText("▶")  # Play icon
            self.play_pause_button.setToolTip("Play")
    
    def play_pause_clicked(self):
        """Handle play/pause button click."""
        if self.player.get_state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
    
    def stop_clicked(self):
        """Handle stop button click."""
        self.player.stop()
    
    def previous_clicked(self):
        """Handle previous button click."""
        self.player.previous_track()
    
    def next_clicked(self):
        """Handle next button click."""
        self.player.next_track()
    
    def shuffle_clicked(self, checked):
        """Handle shuffle button click."""
        is_shuffled = self.player.toggle_shuffle()
        self.shuffle_button.setChecked(is_shuffled)
    
    def repeat_clicked(self, checked):
        """Handle repeat button click."""
        repeat_mode = self.player.toggle_repeat()
        self.repeat_button.setChecked(repeat_mode > 0)
    
    def mute_clicked(self, checked=None):
        """Handle mute button click."""
        is_muted = self.player.toggle_mute()
        self.mute_button.setChecked(is_muted)
        if is_muted:
            self.mute_button.setText("🔇")  # Muted icon
        else:
            self.mute_button.setText("🔊")  # Volume icon
    
    def volume_changed(self, value):
        """Handle volume slider change."""
        self.player.set_volume(value)
        # If volume is 0, update mute button
        self.mute_button.setChecked(value == 0)
        if value == 0:
            self.mute_button.setText("🔇")  # Muted icon
        else:
            self.mute_button.setText("🔊")  # Volume icon
    
    def speed_changed(self, value):
        """Handle speed slider change."""
        speed = value / 100.0
        self.player.set_playback_rate(speed)
        self.speed_value_label.setText(f"{speed:.1f}x")
