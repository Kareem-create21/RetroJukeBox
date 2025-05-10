<<<<<<< HEAD
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QSlider, QFileDialog, 
                            QListWidget, QListWidgetItem, QMenu, QAction, 
                            QMessageBox, QSplitter, QFrame, QToolButton, 
                            QSystemTrayIcon, QStyle, QComboBox, QLineEdit, 
                            QSpinBox, QTabWidget, QScrollArea, QGroupBox, 
                            QGridLayout, QCheckBox, QDialog, QFormLayout)
from PyQt5.QtCore import Qt, QTimer, QUrl, QSettings
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor, QFont
from PyQt5.QtMultimedia import QMediaPlayer

import os
import sys
from functools import partial

from player import AudioPlayer
from playlist import PlaylistManager
from metadata import MetadataManager
from ui.controls import PlayerControls
from ui.visualizer import AudioVisualizer
from ui.themes import ThemeManager
from utils.config import ConfigManager
from utils.audio import format_time

class RetroPlayerWindow(QMainWindow):
    """Main window for the retro MP3 player application."""
=======
"""
Main window implementation for RetroJukebox
"""

import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QSplitter, QLabel, QPushButton, 
                             QSlider, QFileDialog, QMessageBox, QListWidget,
                             QListWidgetItem, QComboBox, QInputDialog, QAction,
                             QToolBar, QMenu, QDialog, QFrame, QGridLayout,
                             QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize, QByteArray
from PyQt5.QtSvg import QSvgWidget

from player import Player
from file_manager import FileManager
from metadata import MetadataManager
from playlist import PlaylistManager
from visualizer import AudioVisualizer
from themes import ThemeManager
from ui.controls import create_playback_controls

class MainWindow(QMainWindow):
    """
    Main application window
    """
>>>>>>> 7931bac3b70b4ade7d98445fc1a06d706a28aa92
    
    def __init__(self):
        super().__init__()
        
<<<<<<< HEAD
        # Setup audio player
        self.player = AudioPlayer()
        self.playlist_manager = PlaylistManager(self.player)
        self.config_manager = ConfigManager()
        self.theme_manager = ThemeManager()
        
        # Setup player callbacks
        self.player.set_callbacks(
            duration_changed=self.update_duration,
            position_changed=self.update_position,
            state_changed=self.update_player_state,
            track_changed=self.track_changed
        )
        
        # Track data
        self.current_track_metadata = None
        self.current_track_path = ""
        
        # UI setup
        self.init_ui()
        self.setup_tray_icon()
        
        # Load saved settings
        self.load_settings()
        
        # Setup update timer for visualizer
        self.visualizer_timer = QTimer(self)
        self.visualizer_timer.timeout.connect(self.update_visualizer)
        self.visualizer_timer.start(50)  # Update every 50ms
        
        # Setup status bar
        self.statusBar().showMessage("Ready")
    
    def init_ui(self):
        """Initialize the user interface."""
        # Main window setup
        self.setWindowTitle("Retro MP3 Player")
        self.setMinimumSize(800, 600)
        
        # Apply initial theme
        self.theme_manager.apply_theme(self, "dark")
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Create header section (now playing info)
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        
        # Album art placeholder
        self.album_art_label = QLabel()
        self.album_art_label.setFixedSize(100, 100)
        self.album_art_label.setAlignment(Qt.AlignCenter)
        self.album_art_label.setStyleSheet("background-color: #444;")
        
        # Track info section
        track_info_layout = QVBoxLayout()
        self.track_title_label = QLabel("No Track")
        self.track_title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.track_artist_label = QLabel("No Artist")
        self.track_artist_label.setFont(QFont("Arial", 12))
        self.track_album_label = QLabel("No Album")
        
        track_info_layout.addWidget(self.track_title_label)
        track_info_layout.addWidget(self.track_artist_label)
        track_info_layout.addWidget(self.track_album_label)
        track_info_layout.addStretch()
        
        header_layout.addWidget(self.album_art_label)
        header_layout.addLayout(track_info_layout, 1)
        
        # Audio visualizer
        self.visualizer = AudioVisualizer()
        self.visualizer.setFixedHeight(80)
        
        # Create main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Playlist section
        playlist_frame = QFrame()
        playlist_layout = QVBoxLayout(playlist_frame)
        
        # Playlist controls
        playlist_controls_layout = QHBoxLayout()
        
        self.add_file_button = QPushButton("Add File")
        self.add_file_button.clicked.connect(self.open_file_dialog)
        
        self.add_folder_button = QPushButton("Add Folder")
        self.add_folder_button.clicked.connect(self.import_folder)
        
        self.save_playlist_button = QPushButton("Save Playlist")
        self.save_playlist_button.clicked.connect(self.save_playlist)
        
        self.load_playlist_button = QPushButton("Load Playlist")
        self.load_playlist_button.clicked.connect(self.load_playlist)
        
        playlist_controls_layout.addWidget(self.add_file_button)
        playlist_controls_layout.addWidget(self.add_folder_button)
        playlist_controls_layout.addWidget(self.save_playlist_button)
        playlist_controls_layout.addWidget(self.load_playlist_button)
        
        # Playlist filter and search
        filter_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search songs...")
        self.search_box.textChanged.connect(self.filter_playlist)
        
        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(self.search_box, 1)
        
        # Rating filter
        self.rating_combo = QComboBox()
        self.rating_combo.addItems(["All Songs", "★ or higher", "★★ or higher", 
                                    "★★★ or higher", "★★★★ or higher", "★★★★★ only"])
        self.rating_combo.currentIndexChanged.connect(self.filter_by_rating)
        
        filter_layout.addWidget(QLabel("Rating:"))
        filter_layout.addWidget(self.rating_combo)
        
        # Playlist widget
        self.playlist_widget = QListWidget()
        self.playlist_widget.setAlternatingRowColors(True)
        self.playlist_widget.itemDoubleClicked.connect(self.playlist_item_double_clicked)
        self.playlist_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlist_widget.customContextMenuRequested.connect(self.show_playlist_context_menu)
        
        playlist_layout.addLayout(playlist_controls_layout)
        playlist_layout.addLayout(filter_layout)
        playlist_layout.addWidget(self.playlist_widget, 1)  # Give it stretch
        
        # File info and settings section
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)
        
        # Create tabs
        tabs = QTabWidget()
        
        # Track info tab
        track_info_tab = QWidget()
        track_info_layout = QFormLayout(track_info_tab)
        
        self.file_info_label = QLabel("No file loaded")
        self.bitrate_label = QLabel("-")
        self.sample_rate_label = QLabel("-")
        self.duration_label = QLabel("-")
        self.file_size_label = QLabel("-")
        
        # Track rating
        rating_layout = QHBoxLayout()
        self.rating_label = QLabel("Rating:")
        self.rating_stars = []
        
        for i in range(5):
            star_button = QPushButton("★")
            star_button.setFixedSize(20, 20)
            star_button.setCheckable(True)
            star_button.clicked.connect(partial(self.set_rating, i+1))
            rating_layout.addWidget(star_button)
            self.rating_stars.append(star_button)
        
        track_info_layout.addRow("File:", self.file_info_label)
        track_info_layout.addRow("Bitrate:", self.bitrate_label)
        track_info_layout.addRow("Sample Rate:", self.sample_rate_label)
        track_info_layout.addRow("Duration:", self.duration_label)
        track_info_layout.addRow("File Size:", self.file_size_label)
        track_info_layout.addRow(self.rating_label, rating_layout)
        
        # Equalizer tab
        equalizer_tab = QWidget()
        equalizer_layout = QVBoxLayout(equalizer_tab)
        
        # Equalizer presets
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Preset:"))
        
        self.equalizer_preset = QComboBox()
        self.equalizer_preset.addItems(["Default", "Rock", "Pop", "Jazz", "Classic", "Bass Boost"])
        self.equalizer_preset.currentIndexChanged.connect(self.apply_equalizer_preset)
        
        preset_layout.addWidget(self.equalizer_preset, 1)
        equalizer_layout.addLayout(preset_layout)
        
        # Equalizer sliders
        eq_sliders_layout = QGridLayout()
        self.eq_sliders = []
        
        frequency_bands = ["60Hz", "170Hz", "310Hz", "600Hz", "1kHz", "3kHz", "6kHz", "12kHz", "14kHz", "16kHz"]
        
        for i, band in enumerate(frequency_bands):
            label = QLabel(band)
            label.setAlignment(Qt.AlignCenter)
            
            slider = QSlider(Qt.Vertical)
            slider.setRange(-10, 10)
            slider.setValue(0)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.setFixedHeight(100)
            
            eq_sliders_layout.addWidget(label, 0, i)
            eq_sliders_layout.addWidget(slider, 1, i, Qt.AlignCenter)
            
            self.eq_sliders.append(slider)
        
        equalizer_layout.addLayout(eq_sliders_layout)
        
        # Settings tab
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        
        # Theme selection
        theme_group = QGroupBox("Theme")
        theme_layout = QHBoxLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light Mode", "Dark Mode", "Retro Blue", "Retro Green", "Retro Pink"])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        
        theme_layout.addWidget(QLabel("Select Theme:"))
        theme_layout.addWidget(self.theme_combo, 1)
        theme_group.setLayout(theme_layout)
        
        # Playback settings
        playback_group = QGroupBox("Playback")
        playback_layout = QFormLayout()
        
        self.skip_timer_check = QCheckBox("Skip to next song after:")
        self.skip_timer_check.toggled.connect(self.toggle_skip_timer)
        
        self.skip_timer_value = QSpinBox()
        self.skip_timer_value.setRange(10, 300)
        self.skip_timer_value.setValue(30)
        self.skip_timer_value.setSuffix(" seconds")
        self.skip_timer_value.setEnabled(False)
        
        skip_layout = QHBoxLayout()
        skip_layout.addWidget(self.skip_timer_check)
        skip_layout.addWidget(self.skip_timer_value)
        skip_layout.addStretch()
        
        self.fade_check = QCheckBox("Enable fade in/out")
        
        self.minimize_to_tray_check = QCheckBox("Minimize to tray")
        self.minimize_to_tray_check.setChecked(True)
        
        playback_layout.addRow(skip_layout)
        playback_layout.addRow(self.fade_check)
        playback_layout.addRow(self.minimize_to_tray_check)
        playback_group.setLayout(playback_layout)
        
        # Hotkeys
        hotkeys_group = QGroupBox("Hotkeys")
        hotkeys_layout = QFormLayout()
        
        hotkeys_layout.addRow("Play/Pause:", QLabel("Space"))
        hotkeys_layout.addRow("Next Track:", QLabel("Ctrl+Right"))
        hotkeys_layout.addRow("Previous Track:", QLabel("Ctrl+Left"))
        hotkeys_layout.addRow("Volume Up:", QLabel("Ctrl+Up"))
        hotkeys_layout.addRow("Volume Down:", QLabel("Ctrl+Down"))
        hotkeys_layout.addRow("Mute:", QLabel("Ctrl+M"))
        
        hotkeys_group.setLayout(hotkeys_layout)
        
        # Add groups to settings tab
        settings_layout.addWidget(theme_group)
        settings_layout.addWidget(playback_group)
        settings_layout.addWidget(hotkeys_group)
        settings_layout.addStretch()
        
        # Add tabs
        tabs.addTab(track_info_tab, "Track Info")
        tabs.addTab(equalizer_tab, "Equalizer")
        tabs.addTab(settings_tab, "Settings")
        
        info_layout.addWidget(tabs)
        
        # Add frames to splitter
        splitter.addWidget(playlist_frame)
        splitter.addWidget(info_frame)
        
        # Set initial splitter sizes
        splitter.setSizes([int(self.width() * 0.6), int(self.width() * 0.4)])
        
        # Create player controls
        self.controls = PlayerControls(self.player)
        
        # Create progress bar and time labels
        progress_layout = QHBoxLayout()
        
        self.current_time_label = QLabel("00:00")
        self.total_time_label = QLabel("00:00")
        
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.sliderMoved.connect(self.seek_position)
        self.progress_slider.sliderPressed.connect(lambda: self.progress_slider.setProperty("seeking", True))
        self.progress_slider.sliderReleased.connect(lambda: self.progress_slider.setProperty("seeking", False))
        
        progress_layout.addWidget(self.current_time_label)
        progress_layout.addWidget(self.progress_slider, 1)
        progress_layout.addWidget(self.total_time_label)
        
        # Add all widgets to main layout
        main_layout.addWidget(header_frame)
        main_layout.addWidget(self.visualizer)
        main_layout.addLayout(progress_layout)
        main_layout.addWidget(self.controls)
        main_layout.addWidget(splitter, 1)  # Give it stretch
        
        # Set central widget
        self.setCentralWidget(main_widget)
        
        # Timer for skip timer functionality
        self.skip_timer = QTimer(self)
        self.skip_timer.timeout.connect(self.skip_track_timer)
        self.skip_timer_active = False
        self.skip_time_remaining = 0
    
    def setup_tray_icon(self):
        """Set up system tray icon and menu."""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        
        # Create tray icon menu
        tray_menu = QMenu()
        
        play_action = QAction("Play/Pause", self)
        play_action.triggered.connect(self.controls.play_pause_clicked)
        
        next_action = QAction("Next Track", self)
        next_action.triggered.connect(self.controls.next_clicked)
        
        prev_action = QAction("Previous Track", self)
        prev_action.triggered.connect(self.controls.previous_clicked)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        
        tray_menu.addAction(play_action)
        tray_menu.addAction(next_action)
        tray_menu.addAction(prev_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # Show the tray icon
        self.tray_icon.show()
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.minimize_to_tray_check.isChecked() and self.tray_icon.isVisible():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Retro MP3 Player",
                "Application is still running in the system tray.",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            # Save settings before closing
            self.save_settings()
            event.accept()
    
    def save_settings(self):
        """Save application settings."""
        settings = QSettings()
        
        # Save window geometry
        settings.setValue("geometry", self.saveGeometry())
        
        # Save volume
        settings.setValue("volume", self.player.get_volume())
        
        # Save theme
        settings.setValue("theme", self.theme_combo.currentIndex())
        
        # Save last playlist if available
        if self.player.get_track_count() > 0:
            playlist_data = []
            for i in range(self.player.get_track_count()):
                url = self.player.get_media_url(i)
                if url.isLocalFile():
                    playlist_data.append(url.toLocalFile())
            
            settings.setValue("last_playlist", playlist_data)
            settings.setValue("last_track_index", self.player.get_current_track_index())
        
        # Save ratings
        settings.setValue("song_ratings", self.playlist_manager.song_ratings)
        
        # Save other settings
        settings.setValue("minimize_to_tray", self.minimize_to_tray_check.isChecked())
        settings.setValue("fade_enabled", self.fade_check.isChecked())
        settings.setValue("skip_timer_enabled", self.skip_timer_check.isChecked())
        settings.setValue("skip_timer_seconds", self.skip_timer_value.value())
        
        # Save equalizer settings
        eq_values = [slider.value() for slider in self.eq_sliders]
        settings.setValue("equalizer_values", eq_values)
        settings.setValue("equalizer_preset", self.equalizer_preset.currentIndex())
    
    def load_settings(self):
        """Load application settings."""
        settings = QSettings()
        
        # Restore window geometry
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        # Restore volume
        volume = settings.value("volume", 70, type=int)
        self.player.set_volume(volume)
        self.controls.volume_slider.setValue(volume)
        
        # Restore theme
        theme_index = settings.value("theme", 0, type=int)
        self.theme_combo.setCurrentIndex(theme_index)
        self.change_theme(theme_index)
        
        # Restore last playlist
        last_playlist = settings.value("last_playlist", [])
        if last_playlist:
            for file_path in last_playlist:
                if os.path.exists(file_path):
                    self.add_file_to_playlist(file_path)
            
            # Set last track
            last_index = settings.value("last_track_index", 0, type=int)
            if 0 <= last_index < self.player.get_track_count():
                self.player.set_current_track(last_index)
                self.playlist_widget.setCurrentRow(last_index)
                self.update_track_info(last_index)
        
        # Restore ratings
        ratings = settings.value("song_ratings", {})
        if ratings:
            self.playlist_manager.song_ratings = ratings
        
        # Restore other settings
        self.minimize_to_tray_check.setChecked(settings.value("minimize_to_tray", True, type=bool))
        self.fade_check.setChecked(settings.value("fade_enabled", False, type=bool))
        self.skip_timer_check.setChecked(settings.value("skip_timer_enabled", False, type=bool))
        self.skip_timer_value.setValue(settings.value("skip_timer_seconds", 30, type=int))
        self.skip_timer_value.setEnabled(self.skip_timer_check.isChecked())
        
        # Restore equalizer settings
        eq_values = settings.value("equalizer_values", [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for i, value in enumerate(eq_values):
            if i < len(self.eq_sliders):
                self.eq_sliders[i].setValue(int(value))
        
        preset_index = settings.value("equalizer_preset", 0, type=int)
        self.equalizer_preset.setCurrentIndex(preset_index)
    
    def open_file_dialog(self):
        """Open file dialog to select MP3 files."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Open MP3 Files", "", "MP3 Files (*.mp3);;All Files (*)"
        )
        
        if files:
            for file_path in files:
                self.add_file_to_playlist(file_path)
    
    def add_file_to_playlist(self, file_path):
        """Add a file to the playlist."""
        if not os.path.exists(file_path):
            return
        
        # Add to player playlist
        url = QUrl.fromLocalFile(file_path)
        index = self.player.add_to_playlist(url)
        
        # Get metadata for display
        metadata = MetadataManager.get_metadata(file_path)
        
        # Create list item with track info
        item_text = f"{metadata['title']} - {metadata['artist']}"
        
        # Add stars if rated
        rating = self.playlist_manager.get_song_rating(file_path)
        if rating > 0:
            stars = "★" * rating
            item_text = f"{item_text} {stars}"
        
        item = QListWidgetItem(item_text)
        item.setData(Qt.UserRole, file_path)  # Store file path as item data
        
        self.playlist_widget.addItem(item)
        
        # If this is the first track, update display and auto-select it
        if self.playlist_widget.count() == 1:
            self.playlist_widget.setCurrentRow(0)
            self.update_track_info(0)
    
    def import_folder(self):
        """Import all MP3 files from a folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        if folder:
            count = self.playlist_manager.import_folder(folder)
            self.refresh_playlist_widget()
            self.statusBar().showMessage(f"Imported {count} MP3 files from folder")
    
    def refresh_playlist_widget(self):
        """Refresh the playlist widget with current tracks."""
        self.playlist_widget.clear()
        
        for i in range(self.player.get_track_count()):
            url = self.player.get_media_url(i)
            if url.isLocalFile():
                file_path = url.toLocalFile()
                metadata = MetadataManager.get_metadata(file_path)
                
                item_text = f"{metadata['title']} - {metadata['artist']}"
                
                # Add stars if rated
                rating = self.playlist_manager.get_song_rating(file_path)
                if rating > 0:
                    stars = "★" * rating
                    item_text = f"{item_text} {stars}"
                
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, file_path)
                
                self.playlist_widget.addItem(item)
    
    def save_playlist(self):
        """Save current playlist to a file."""
        if self.player.get_track_count() == 0:
            QMessageBox.information(self, "Save Playlist", "No tracks to save.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Playlist", "", "Playlist Files (*.rpl);;All Files (*)"
        )
        
        if file_path:
            # Add extension if not provided
            if not file_path.lower().endswith('.rpl'):
                file_path += '.rpl'
            
            success = self.playlist_manager.save_playlist(file_path)
            
            if success:
                self.statusBar().showMessage(f"Playlist saved: {file_path}")
            else:
                QMessageBox.warning(self, "Save Error", "Failed to save playlist.")
    
    def load_playlist(self):
        """Load a playlist from a file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Playlist", "", "Playlist Files (*.rpl);;All Files (*)"
        )
        
        if file_path:
            success = self.playlist_manager.load_playlist(file_path)
            
            if success:
                self.refresh_playlist_widget()
                self.statusBar().showMessage(f"Playlist loaded: {file_path}")
                
                # Select first track if available
                if self.playlist_widget.count() > 0:
                    self.playlist_widget.setCurrentRow(0)
                    self.update_track_info(0)
            else:
                QMessageBox.warning(self, "Load Error", "Failed to load playlist.")
    
    def playlist_item_double_clicked(self, item):
        """Handle double click on playlist item."""
        index = self.playlist_widget.row(item)
        self.player.set_current_track(index)
        self.player.play()
    
    def show_playlist_context_menu(self, position):
        """Show context menu for playlist items."""
        menu = QMenu()
        
        play_action = menu.addAction("Play")
        remove_action = menu.addAction("Remove")
        
        rate_menu = QMenu("Rate")
        rate_actions = []
        
        for i in range(5):
            rate_actions.append(rate_menu.addAction(f"{'★' * (i+1)}"))
        
        menu.addMenu(rate_menu)
        menu.addSeparator()
        
        move_up_action = menu.addAction("Move Up")
        move_down_action = menu.addAction("Move Down")
        
        # Get selected item
        item = self.playlist_widget.itemAt(position)
        if not item:
            return
        
        # Show the menu and get selected action
        action = menu.exec_(self.playlist_widget.mapToGlobal(position))
        
        # Handle actions
        if action == play_action:
            index = self.playlist_widget.row(item)
            self.player.set_current_track(index)
            self.player.play()
        
        elif action == remove_action:
            index = self.playlist_widget.row(item)
            # TODO: Implement remove from playlist functionality
            # This would require modifying the QMediaPlaylist which is more complex
            # For now, just remove from widget
            self.playlist_widget.takeItem(index)
        
        elif action in rate_actions:
            index = self.playlist_widget.row(item)
            rating = rate_actions.index(action) + 1
            
            file_path = item.data(Qt.UserRole)
            self.playlist_manager.set_song_rating(file_path, rating)
            
            # Update display
            item_text = item.text().split(" ★")[0]  # Remove existing stars
            item.setText(f"{item_text} {'★' * rating}")
            
            # Update current track rating display if this is the current track
            if file_path == self.current_track_path:
                self.update_rating_display(rating)
        
        elif action == move_up_action:
            row = self.playlist_widget.row(item)
            if row > 0:
                # Take the item
                taken_item = self.playlist_widget.takeItem(row)
                # Insert it at the new position
                self.playlist_widget.insertItem(row - 1, taken_item)
                # Select it again
                self.playlist_widget.setCurrentRow(row - 1)
        
        elif action == move_down_action:
            row = self.playlist_widget.row(item)
            if row < self.playlist_widget.count() - 1:
                # Take the item
                taken_item = self.playlist_widget.takeItem(row)
                # Insert it at the new position
                self.playlist_widget.insertItem(row + 1, taken_item)
                # Select it again
                self.playlist_widget.setCurrentRow(row + 1)
    
    def update_duration(self, duration, formatted_duration):
        """Update the duration display."""
        self.progress_slider.setMaximum(duration)
        self.total_time_label.setText(formatted_duration)
        
        # Update track info
        if self.current_track_metadata:
            self.duration_label.setText(formatted_duration)
    
    def update_position(self, position, formatted_position, duration):
        """Update the position display and slider."""
        # Only update slider if not currently seeking
        if not self.progress_slider.property("seeking"):
            self.progress_slider.setValue(position)
        
        self.current_time_label.setText(formatted_position)
        
        # Update skip timer display if active
        if self.skip_timer_active:
            remaining = self.skip_time_remaining
            self.statusBar().showMessage(f"Skipping to next track in {remaining} seconds")
    
    def update_player_state(self, state):
        """Update UI based on player state."""
        # Update controls display
        self.controls.update_controls(state)
        
        # Handle skip timer
        if state == QMediaPlayer.PlayingState:
            if self.skip_timer_check.isChecked() and not self.skip_timer_active:
                self.start_skip_timer()
            
            if not self.visualizer_timer.isActive():
                self.visualizer_timer.start(50)
        else:
            if self.skip_timer_active:
                self.skip_timer.stop()
                self.skip_timer_active = False
            
            if state == QMediaPlayer.StoppedState:
                self.visualizer_timer.stop()
                self.visualizer.clear()
    
    def track_changed(self, index):
        """Handle track changed event."""
        # Update track info
        self.update_track_info(index)
        
        # Update playlist selection
        if index >= 0 and index < self.playlist_widget.count():
            self.playlist_widget.setCurrentRow(index)
        
        # Reset skip timer if active
        if self.skip_timer_active:
            self.skip_timer.stop()
            self.skip_timer_active = False
            
            # Start again if playing and enabled
            if self.player.get_state() == QMediaPlayer.PlayingState and self.skip_timer_check.isChecked():
                self.start_skip_timer()
    
    def update_track_info(self, index):
        """Update track information display."""
        if index < 0 or self.player.get_track_count() == 0:
            return
        
        # Get file path
        url = self.player.get_media_url(index)
        if not url.isLocalFile():
            return
        
        file_path = url.toLocalFile()
        self.current_track_path = file_path
        
        # Get metadata
        metadata = MetadataManager.get_metadata(file_path)
        self.current_track_metadata = metadata
        
        # Update track info display
        self.track_title_label.setText(metadata['title'])
        self.track_artist_label.setText(metadata['artist'])
        self.track_album_label.setText(metadata['album'])
        
        # Update file info
        self.file_info_label.setText(os.path.basename(file_path))
        self.bitrate_label.setText(MetadataManager.format_bitrate(metadata['bitrate']))
        self.sample_rate_label.setText(MetadataManager.format_sample_rate(metadata['sample_rate']))
        self.duration_label.setText(format_time(metadata['duration']))
        self.file_size_label.setText(MetadataManager.format_file_size(metadata['file_size']))
        
        # Update album art
        album_art = MetadataManager.get_album_art(file_path)
        if album_art:
            scaled_art = album_art.scaled(self.album_art_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.album_art_label.setPixmap(scaled_art)
        else:
            self.album_art_label.setText("No\nArt")
        
        # Update rating
        rating = self.playlist_manager.get_song_rating(file_path)
        self.update_rating_display(rating)
    
    def update_rating_display(self, rating):
        """Update the rating display."""
        for i, star in enumerate(self.rating_stars):
            star.setChecked(i < rating)
    
    def set_rating(self, rating):
        """Set the rating for the current track."""
        if not self.current_track_path:
            return
        
        self.playlist_manager.set_song_rating(self.current_track_path, rating)
        self.update_rating_display(rating)
        
        # Update the playlist item text to include stars
        current_index = self.player.get_current_track_index()
        if current_index >= 0 and current_index < self.playlist_widget.count():
            item = self.playlist_widget.item(current_index)
            
            # Remove existing stars
            item_text = item.text().split(" ★")[0]
            
            # Add new stars
            item.setText(f"{item_text} {'★' * rating}")
    
    def filter_playlist(self):
        """Filter playlist by search term."""
        search_text = self.search_box.text().lower()
        
        for i in range(self.playlist_widget.count()):
            item = self.playlist_widget.item(i)
            item_text = item.text().lower()
            
            # Show/hide based on search text
            if search_text and search_text not in item_text:
                item.setHidden(True)
            else:
                item.setHidden(False)
    
    def filter_by_rating(self, index):
        """Filter playlist by rating."""
        if index == 0:  # All songs
            # Show all songs
            for i in range(self.playlist_widget.count()):
                self.playlist_widget.item(i).setHidden(False)
        else:
            min_rating = index  # 1-5
            
            for i in range(self.playlist_widget.count()):
                item = self.playlist_widget.item(i)
                file_path = item.data(Qt.UserRole)
                rating = self.playlist_manager.get_song_rating(file_path)
                
                # Show/hide based on rating
                if rating < min_rating:
                    item.setHidden(True)
                else:
                    item.setHidden(False)
    
    def seek_position(self, position):
        """Seek to position in track."""
        self.player.set_position(position)
    
    def update_visualizer(self):
        """Update the audio visualizer."""
        if self.player.get_state() == QMediaPlayer.PlayingState:
            spectrum_data = self.player.get_spectrum_data()
            self.visualizer.update_spectrum(spectrum_data)
    
    def apply_equalizer_preset(self, preset_index):
        """Apply an equalizer preset."""
        # Presets: values from -10 to 10 for each frequency band
        presets = {
            0: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Default
            1: [4, 3, 2, 0, -1, 1, 3, 4, 4, 3],  # Rock
            2: [2, 1, 0, -1, -2, 0, 1, 2, 3, 3],  # Pop
            3: [2, 1, 0, 0, 1, 3, 2, 1, 2, 2],  # Jazz
            4: [3, 2, 1, 0, 0, 0, -2, -3, -3, -3],  # Classic
            5: [5, 4, 3, 2, 0, 0, 0, 0, 1, 1]   # Bass Boost
        }
        
        if preset_index in presets:
            values = presets[preset_index]
            
            for i, value in enumerate(values):
                if i < len(self.eq_sliders):
                    self.eq_sliders[i].setValue(value)
    
    def change_theme(self, theme_index):
        """Change the application theme."""
        theme_names = ["light", "dark", "retro_blue", "retro_green", "retro_pink"]
        
        if 0 <= theme_index < len(theme_names):
            theme = theme_names[theme_index]
            self.theme_manager.apply_theme(self, theme)
    
    def toggle_skip_timer(self, enabled):
        """Toggle the skip timer functionality."""
        self.skip_timer_value.setEnabled(enabled)
        
        if enabled and self.player.get_state() == QMediaPlayer.PlayingState:
            self.start_skip_timer()
        else:
            self.skip_timer.stop()
            self.skip_timer_active = False
            self.statusBar().showMessage("Ready")
    
    def start_skip_timer(self):
        """Start the skip timer."""
        seconds = self.skip_timer_value.value()
        self.skip_time_remaining = seconds
        self.skip_timer.start(1000)  # 1 second
        self.skip_timer_active = True
        self.statusBar().showMessage(f"Skipping to next track in {seconds} seconds")
    
    def skip_track_timer(self):
        """Handle skip timer timeout."""
        if self.skip_time_remaining <= 1:
            self.skip_timer.stop()
            self.skip_timer_active = False
            self.player.next_track()
            self.statusBar().showMessage("Skipped to next track")
        else:
            self.skip_time_remaining -= 1
            self.statusBar().showMessage(f"Skipping to next track in {self.skip_time_remaining} seconds")

    def play_button_clicked(self):
        """Play button clicked handler."""
        self.controls.play_pause_clicked()
    
    def pause_button_clicked(self):
        """Pause button clicked handler."""
        if self.player.get_state() == QMediaPlayer.PlayingState:
            self.controls.play_pause_clicked()
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Space:
            self.controls.play_pause_clicked()
        elif event.key() == Qt.Key_Right and event.modifiers() & Qt.ControlModifier:
            self.controls.next_clicked()
        elif event.key() == Qt.Key_Left and event.modifiers() & Qt.ControlModifier:
            self.controls.previous_clicked()
        elif event.key() == Qt.Key_Up and event.modifiers() & Qt.ControlModifier:
            current_volume = self.player.get_volume()
            self.player.set_volume(min(100, current_volume + 5))
            self.controls.volume_slider.setValue(self.player.get_volume())
        elif event.key() == Qt.Key_Down and event.modifiers() & Qt.ControlModifier:
            current_volume = self.player.get_volume()
            self.player.set_volume(max(0, current_volume - 5))
            self.controls.volume_slider.setValue(self.player.get_volume())
        elif event.key() == Qt.Key_M and event.modifiers() & Qt.ControlModifier:
            self.controls.mute_clicked()
        else:
            super().keyPressEvent(event)
=======
        # Initialize components
        self.player = Player()
        self.file_manager = FileManager()
        self.metadata_manager = MetadataManager()
        self.playlist_manager = PlaylistManager()
        self.visualizer = AudioVisualizer()
        self.theme_manager = ThemeManager()
        
        # Setup UI
        self.init_ui()
        
        # Connect signals
        self.connect_signals()
        
        # Start visualizer
        self.visualizer.start()
        
        # Apply default theme
        self.theme_manager.apply_theme_to_widget(self)
        
        # Set window properties
        self.setWindowTitle("RetroJukebox")
        self.resize(900, 600)
    
    def init_ui(self):
        """Initialize the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create media player area
        self.create_media_player_area(main_layout)
        
        # Create bottom area with tabs
        self.create_bottom_tabs(main_layout)
        
        # Create menu bar and toolbar
        self.create_menu_bar()
        self.create_toolbar()
        
        # Status bar setup
        self.statusBar().showMessage("Ready")
    
    def create_media_player_area(self, parent_layout):
        """Create the media player area with album art, controls, etc."""
        # Media player container
        media_layout = QHBoxLayout()
        parent_layout.addLayout(media_layout)
        
        # Splitter for album art and track info
        splitter = QSplitter(Qt.Horizontal)
        media_layout.addWidget(splitter)
        
        # Left side - Album art and theme-specific visuals
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Visual theme container (for cassette/vinyl visual)
        self.theme_visual_container = QFrame()
        self.theme_visual_container.setFixedSize(300, 300)
        self.theme_visual_container.setObjectName("themeVisualContainer")
        
        # SVG Widget for theme visual
        self.theme_visual = QSvgWidget()
        self.theme_visual.setFixedSize(300, 300)
        
        # Layout for theme visual
        theme_visual_layout = QHBoxLayout(self.theme_visual_container)
        theme_visual_layout.addWidget(self.theme_visual)
        
        left_layout.addWidget(self.theme_visual_container)
        left_layout.addStretch()
        
        # Right side - Track info, controls, visualizer
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Now playing section
        now_playing_widget = QWidget()
        now_playing_layout = QVBoxLayout(now_playing_widget)
        
        self.track_title_label = QLabel("No Track Playing")
        self.track_title_label.setObjectName("trackTitleLabel")
        self.track_title_label.setAlignment(Qt.AlignCenter)
        self.track_title_label.setWordWrap(True)
        
        self.artist_label = QLabel("Unknown Artist")
        self.artist_label.setObjectName("artistLabel")
        self.artist_label.setAlignment(Qt.AlignCenter)
        
        self.album_label = QLabel("Unknown Album")
        self.album_label.setAlignment(Qt.AlignCenter)
        
        # Add audio quality info label
        self.audio_quality_label = QLabel("")
        self.audio_quality_label.setAlignment(Qt.AlignCenter)
        self.audio_quality_label.setObjectName("audioQualityLabel")
        
        now_playing_layout.addWidget(self.track_title_label)
        now_playing_layout.addWidget(self.artist_label)
        now_playing_layout.addWidget(self.album_label)
        now_playing_layout.addWidget(self.audio_quality_label)
        
        right_layout.addWidget(now_playing_widget)
        
        # Visualizer area
        self.visualizer_label = QLabel()
        self.visualizer_label.setMinimumHeight(120)
        self.visualizer_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.visualizer_label)
        
        # Position slider
        position_widget = QWidget()
        position_layout = QHBoxLayout(position_widget)
        
        self.position_label = QLabel("0:00")
        self.position_slider = QSlider(Qt.Horizontal)
        self.duration_label = QLabel("0:00")
        
        position_layout.addWidget(self.position_label)
        position_layout.addWidget(self.position_slider)
        position_layout.addWidget(self.duration_label)
        
        right_layout.addWidget(position_widget)
        
        # Playback controls
        controls_widget = create_playback_controls()
        right_layout.addWidget(controls_widget)
        
        # Connect control buttons
        controls_widget.playButton.clicked.connect(self.play_current)
        controls_widget.pauseButton.clicked.connect(self.pause_resume)
        controls_widget.stopButton.clicked.connect(self.stop_playback)
        controls_widget.prevButton.clicked.connect(self.play_previous)
        controls_widget.nextButton.clicked.connect(self.play_next)
        controls_widget.volumeSlider.valueChanged.connect(self.change_volume)
        controls_widget.shuffleButton.clicked.connect(self.toggle_shuffle)
        controls_widget.repeatButton.clicked.connect(self.toggle_repeat)
        
        self.playback_controls = controls_widget
        
        # Extra controls
        extra_controls = QWidget()
        extra_layout = QHBoxLayout(extra_controls)
        
        # Theme selector
        theme_label = QLabel("Theme:")
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(self.theme_manager.get_theme_names())
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        
        # Visualization type selector
        visualizer_label = QLabel("Visualizer:")
        self.visualizer_selector = QComboBox()
        self.visualizer_selector.addItems(["bars", "waves", "circles"])
        self.visualizer_selector.currentTextChanged.connect(self.change_visualization)
        
        extra_layout.addWidget(theme_label)
        extra_layout.addWidget(self.theme_selector)
        extra_layout.addWidget(visualizer_label)
        extra_layout.addWidget(self.visualizer_selector)
        
        right_layout.addWidget(extra_controls)
        
        # Add left and right sides to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        
        # Set initial splitter sizes
        splitter.setSizes([300, 600])
    
    def create_bottom_tabs(self, parent_layout):
        """Create the bottom tabs area with library and playlists"""
        # Tab widget
        self.tabs = QTabWidget()
        parent_layout.addWidget(self.tabs)
        
        # Library tab
        self.library_widget = QWidget()
        library_layout = QVBoxLayout(self.library_widget)
        
        # Library controls
        library_controls = QWidget()
        library_controls_layout = QHBoxLayout(library_controls)
        
        self.browse_button = QPushButton("Browse...")
        self.browse_button.setToolTip("Browse for music directory")
        self.browse_button.clicked.connect(self.browse_directory)
        
        # Add search functionality
        from PyQt5.QtWidgets import QLineEdit
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search library...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self.search_library)
        
        library_controls_layout.addWidget(self.browse_button)
        library_controls_layout.addWidget(self.search_input)
        library_controls_layout.addStretch()
        
        # Library list
        self.library_list = QListWidget()
        self.library_list.itemDoubleClicked.connect(self.library_item_double_clicked)
        
        library_layout.addWidget(library_controls)
        library_layout.addWidget(self.library_list)
        
        # Playlist tab
        self.playlist_widget = QWidget()
        playlist_layout = QVBoxLayout(self.playlist_widget)
        
        # Playlist controls
        playlist_controls = QWidget()
        playlist_controls_layout = QHBoxLayout(playlist_controls)
        
        self.playlist_selector = QComboBox()
        self.playlist_selector.currentTextChanged.connect(self.change_playlist)
        
        self.new_playlist_button = QPushButton("New")
        self.new_playlist_button.setToolTip("Create new playlist")
        self.new_playlist_button.clicked.connect(self.create_new_playlist)
        
        self.rename_playlist_button = QPushButton("Rename")
        self.rename_playlist_button.setToolTip("Rename current playlist")
        self.rename_playlist_button.clicked.connect(self.rename_current_playlist)
        
        self.delete_playlist_button = QPushButton("Delete")
        self.delete_playlist_button.setToolTip("Delete current playlist")
        self.delete_playlist_button.clicked.connect(self.delete_current_playlist)
        
        playlist_controls_layout.addWidget(self.playlist_selector)
        playlist_controls_layout.addWidget(self.new_playlist_button)
        playlist_controls_layout.addWidget(self.rename_playlist_button)
        playlist_controls_layout.addWidget(self.delete_playlist_button)
        
        # Add second row of playlist controls with sorting and search
        playlist_controls2 = QWidget()
        playlist_controls_layout2 = QHBoxLayout(playlist_controls2)
        
        # Search in playlist
        self.playlist_search = QLineEdit()
        self.playlist_search.setPlaceholderText("Search in playlist...")
        self.playlist_search.setClearButtonEnabled(True)
        self.playlist_search.textChanged.connect(self.search_playlist)
        
        # Sorting options
        self.sort_by_name_button = QPushButton("Sort by Name")
        self.sort_by_name_button.setToolTip("Sort tracks by filename")
        self.sort_by_name_button.clicked.connect(self.sort_playlist_by_name)
        
        self.sort_by_path_button = QPushButton("Sort by Path")
        self.sort_by_path_button.setToolTip("Sort tracks by file path")
        self.sort_by_path_button.clicked.connect(self.sort_playlist_by_path)
        
        playlist_controls_layout2.addWidget(self.playlist_search)
        playlist_controls_layout2.addWidget(self.sort_by_name_button)
        playlist_controls_layout2.addWidget(self.sort_by_path_button)
        
        # Playlist list
        self.playlist_list = QListWidget()
        self.playlist_list.itemDoubleClicked.connect(self.playlist_item_double_clicked)
        
        playlist_layout.addWidget(playlist_controls)
        playlist_layout.addWidget(playlist_controls2)
        playlist_layout.addWidget(self.playlist_list)
        
        # Add tabs
        self.tabs.addTab(self.library_widget, "Library")
        self.tabs.addTab(self.playlist_widget, "Playlists")
        
        # Update playlist selector with available playlists
        self.update_playlist_selector()
    
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open File...", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        open_dir_action = QAction("Open Directory...", self)
        open_dir_action.triggered.connect(self.browse_directory)
        file_menu.addAction(open_dir_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Playback menu
        playback_menu = menubar.addMenu("Playback")
        
        play_action = QAction("Play", self)
        play_action.triggered.connect(self.play_current)
        playback_menu.addAction(play_action)
        
        pause_action = QAction("Pause/Resume", self)
        pause_action.triggered.connect(self.pause_resume)
        playback_menu.addAction(pause_action)
        
        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self.stop_playback)
        playback_menu.addAction(stop_action)
        
        playback_menu.addSeparator()
        
        next_action = QAction("Next", self)
        next_action.triggered.connect(self.play_next)
        playback_menu.addAction(next_action)
        
        prev_action = QAction("Previous", self)
        prev_action.triggered.connect(self.play_previous)
        playback_menu.addAction(prev_action)
        
        # Playlist menu
        playlist_menu = menubar.addMenu("Playlist")
        
        new_playlist_action = QAction("New Playlist", self)
        new_playlist_action.triggered.connect(self.create_new_playlist)
        playlist_menu.addAction(new_playlist_action)
        
        rename_playlist_action = QAction("Rename Playlist", self)
        rename_playlist_action.triggered.connect(self.rename_current_playlist)
        playlist_menu.addAction(rename_playlist_action)
        
        delete_playlist_action = QAction("Delete Playlist", self)
        delete_playlist_action.triggered.connect(self.delete_current_playlist)
        playlist_menu.addAction(delete_playlist_action)
        
        # Visualization menu
        visualization_menu = menubar.addMenu("Visualization")
        
        # Visualization type submenu
        viz_type_menu = QMenu("Visualization Type", self)
        visualization_menu.addMenu(viz_type_menu)
        
        viz_types = [
            "Bars", "Waves", "Circles", "Spectrum", 
            "Particles", "Equalizer", "Waveform", 
            "3D Bars", "Fireworks", "Oscilloscope"
        ]
        
        viz_type_actions = {}
        for viz_type in viz_types:
            action = QAction(viz_type, self)
            action.setCheckable(True)
            if viz_type.lower().replace(" ", "-") == self.visualizer.viz_type:
                action.setChecked(True)
            viz_type_actions[viz_type] = action
            viz_type_menu.addAction(action)
            action.triggered.connect(lambda checked, vt=viz_type: self.set_visualization_type(vt.lower().replace(" ", "-")))
        
        # Color scheme submenu
        color_scheme_menu = QMenu("Color Scheme", self)
        visualization_menu.addMenu(color_scheme_menu)
        
        color_schemes = list(self.visualizer.color_maps.keys())
        color_scheme_actions = {}
        for scheme in color_schemes:
            action = QAction(scheme.capitalize(), self)
            action.setCheckable(True)
            if scheme == self.visualizer.color_scheme:
                action.setChecked(True)
            color_scheme_actions[scheme] = action
            color_scheme_menu.addAction(action)
            action.triggered.connect(lambda checked, s=scheme: self.set_color_scheme(s))
        
        visualization_menu.addSeparator()
        
        # Background pattern submenu
        bg_pattern_menu = QMenu("Background Pattern", self)
        visualization_menu.addMenu(bg_pattern_menu)
        
        bg_patterns = ["Solid", "Grid", "Dots", "Noise"]
        bg_pattern_actions = {}
        for pattern in bg_patterns:
            action = QAction(pattern, self)
            action.setCheckable(True)
            if pattern.lower() == self.visualizer.bg_pattern:
                action.setChecked(True)
            bg_pattern_actions[pattern] = action
            bg_pattern_menu.addAction(action)
            action.triggered.connect(lambda checked, p=pattern: self.set_background_pattern(p.lower()))
        
        visualization_menu.addSeparator()
        
        # Effects submenu
        effects_menu = QMenu("Effects", self)
        visualization_menu.addMenu(effects_menu)
        
        # Glow effect
        glow_effect_action = QAction("Glow Effect", self)
        glow_effect_action.setCheckable(True)
        glow_effect_action.setChecked(self.visualizer.glow_effect)
        glow_effect_action.triggered.connect(lambda: self.toggle_visualization_effect("glow"))
        effects_menu.addAction(glow_effect_action)
        
        # Mirror mode
        mirror_mode_action = QAction("Mirror Mode", self)
        mirror_mode_action.setCheckable(True)
        mirror_mode_action.setChecked(self.visualizer.mirror_mode)
        mirror_mode_action.triggered.connect(lambda: self.toggle_visualization_effect("mirror"))
        effects_menu.addAction(mirror_mode_action)
        
        # Invert colors
        invert_colors_action = QAction("Invert Colors", self)
        invert_colors_action.setCheckable(True)
        invert_colors_action.setChecked(self.visualizer.invert_colors)
        invert_colors_action.triggered.connect(lambda: self.toggle_visualization_effect("invert"))
        effects_menu.addAction(invert_colors_action)
        
        # Show song info
        show_song_info_action = QAction("Show Song Info", self)
        show_song_info_action.setCheckable(True)
        show_song_info_action.setChecked(self.visualizer.show_song_info)
        show_song_info_action.triggered.connect(lambda: self.toggle_visualization_effect("song_info"))
        effects_menu.addAction(show_song_info_action)
        
        # Show FPS
        show_fps_action = QAction("Show FPS", self)
        show_fps_action.setCheckable(True)
        show_fps_action.setChecked(self.visualizer.show_fps)
        show_fps_action.triggered.connect(lambda: self.toggle_visualization_effect("fps"))
        effects_menu.addAction(show_fps_action)
        
        # Show time
        show_time_action = QAction("Show Time", self)
        show_time_action.setCheckable(True)
        show_time_action.setChecked(self.visualizer.show_time)
        show_time_action.triggered.connect(lambda: self.toggle_visualization_effect("time"))
        effects_menu.addAction(show_time_action)
        
        visualization_menu.addSeparator()
        
        # Cycle visualization
        cycle_viz_action = QAction("Cycle Visualization (Space)", self)
        cycle_viz_action.triggered.connect(self.cycle_visualization)
        visualization_menu.addAction(cycle_viz_action)
        
        # Cycle color scheme
        cycle_color_action = QAction("Cycle Color Scheme (C)", self)
        cycle_color_action.triggered.connect(self.cycle_color_scheme)
        visualization_menu.addAction(cycle_color_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create the application toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Add toolbar actions
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        toolbar.addSeparator()
        
        play_action = QAction("Play", self)
        play_action.triggered.connect(self.play_current)
        toolbar.addAction(play_action)
        
        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self.pause_resume)
        toolbar.addAction(pause_action)
        
        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self.stop_playback)
        toolbar.addAction(stop_action)
        
        toolbar.addSeparator()
        
        prev_action = QAction("Previous", self)
        prev_action.triggered.connect(self.play_previous)
        toolbar.addAction(prev_action)
        
        next_action = QAction("Next", self)
        next_action.triggered.connect(self.play_next)
        toolbar.addAction(next_action)
    
    def connect_signals(self):
        """Connect all signals to slots"""
        # Player signals
        self.player.track_started.connect(self.on_track_started)
        self.player.track_ended.connect(self.on_track_ended)
        self.player.track_position_changed.connect(self.on_track_position_changed)
        self.player.track_error.connect(self.on_track_error)
        
        # File manager signals
        self.file_manager.scan_finished.connect(self.on_scan_finished)
        self.file_manager.scan_progress.connect(self.on_scan_progress)
        self.file_manager.error.connect(self.on_file_manager_error)
        
        # Metadata manager signals
        self.metadata_manager.error.connect(self.on_metadata_error)
        
        # Playlist manager signals
        self.playlist_manager.playlist_added.connect(self.on_playlist_added)
        self.playlist_manager.playlist_removed.connect(self.on_playlist_removed)
        self.playlist_manager.playlist_updated.connect(self.on_playlist_updated)
        self.playlist_manager.error.connect(self.on_playlist_error)
        
        # Visualizer signals
        self.visualizer.visualization_updated.connect(self.on_visualization_updated)
        
        # Theme manager signals
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # Position slider signals
        self.position_slider.sliderPressed.connect(self.on_position_slider_pressed)
        self.position_slider.sliderReleased.connect(self.on_position_slider_released)
        self.position_slider.valueChanged.connect(self.on_position_slider_value_changed)
    
    def browse_directory(self):
        """Open a dialog to browse for a music directory"""
        directory = QFileDialog.getExistingDirectory(self, "Select Music Directory")
        if directory:
            self.statusBar().showMessage(f"Scanning directory: {directory}")
            self.file_manager.scan_directory(directory)
    
    def open_file(self):
        """Open a dialog to select a music file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Music File", "", "MP3 Files (*.mp3)"
        )
        
        if file_path:
            self.play_file(file_path)
    
    def play_file(self, file_path):
        """Play a specific file"""
        self.player.play(file_path)
    
    def play_current(self):
        """Play the currently selected track"""
        # Try to play from playlist first
        if self.tabs.currentIndex() == 1 and self.playlist_list.currentItem():
            self.playlist_item_double_clicked(self.playlist_list.currentItem())
        # Otherwise try library
        elif self.tabs.currentIndex() == 0 and self.library_list.currentItem():
            self.library_item_double_clicked(self.library_list.currentItem())
        # Otherwise if already have a track, resume it
        elif self.player.current_track and self.player.is_paused:
            self.player.resume()
    
    def pause_resume(self):
        """Toggle between pause and resume"""
        if not self.player.is_playing:
            return
            
        if self.player.is_paused:
            self.player.resume()
            self.playback_controls.pauseButton.setText("Pause")
        else:
            self.player.pause()
            self.playback_controls.pauseButton.setText("Resume")
    
    def stop_playback(self):
        """Stop playback"""
        self.player.stop()
        self.position_slider.setValue(0)
        self.position_label.setText("0:00")
        self.duration_label.setText("0:00")
        self.track_title_label.setText("No Track Playing")
        self.artist_label.setText("Unknown Artist")
        self.album_label.setText("Unknown Album")
        self.playback_controls.pauseButton.setText("Pause")
    
    def search_library(self, search_text):
        """
        Search the library for matching tracks
        
        Args:
            search_text (str): Text to search for
        """
        if not search_text:
            # If search is cleared, show all files
            for i in range(self.library_list.count()):
                self.library_list.item(i).setHidden(False)
            return
            
        # Otherwise filter the list
        for i in range(self.library_list.count()):
            item = self.library_list.item(i)
            if search_text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
    
    def play_next(self):
        """Play the next track in playlist"""
        current_playlist = self.playlist_manager.get_current_playlist()
        if not current_playlist:
            return
            
        # Find current track in playlist
        current_track = self.player.current_track
        if not current_track:
            # If nothing playing, play the first track
            if current_playlist.get_track_count() > 0:
                self.play_file(current_playlist.get_track_at(0))
            return
        
        # Find index of current track
        tracks = current_playlist.get_tracks()
        try:
            current_index = tracks.index(current_track)
        except ValueError:
            # Current track not in playlist, play first track
            if current_playlist.get_track_count() > 0:
                self.play_file(current_playlist.get_track_at(0))
            return
        
        # Play next track or loop to beginning
        if self.player.shuffle:
            # Play random track
            import random
            next_index = random.randint(0, current_playlist.get_track_count() - 1)
            while next_index == current_index and current_playlist.get_track_count() > 1:
                next_index = random.randint(0, current_playlist.get_track_count() - 1)
            self.play_file(current_playlist.get_track_at(next_index))
        else:
            # Play next track in order
            next_index = (current_index + 1) % current_playlist.get_track_count()
            self.play_file(current_playlist.get_track_at(next_index))
    
    def search_playlist(self, search_text):
        """
        Search the current playlist for matching tracks
        
        Args:
            search_text (str): Text to search for
        """
        if not search_text:
            # If search is cleared, show all files
            for i in range(self.playlist_list.count()):
                self.playlist_list.item(i).setHidden(False)
            return
            
        # Otherwise filter the list
        for i in range(self.playlist_list.count()):
            item = self.playlist_list.item(i)
            if search_text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
    
    def sort_playlist_by_name(self):
        """Sort current playlist by filename"""
        current_playlist = self.playlist_manager.get_current_playlist()
        if current_playlist:
            current_playlist.sort_by_filename()
            self.update_playlist_content()
            self.statusBar().showMessage("Playlist sorted by filename", 3000)
    
    def sort_playlist_by_path(self):
        """Sort current playlist by filepath"""
        current_playlist = self.playlist_manager.get_current_playlist()
        if current_playlist:
            current_playlist.sort_by_filepath()
            self.update_playlist_content()
            self.statusBar().showMessage("Playlist sorted by filepath", 3000)
    
    def play_previous(self):
        """Play the previous track in playlist"""
        current_playlist = self.playlist_manager.get_current_playlist()
        if not current_playlist:
            return
            
        # Find current track in playlist
        current_track = self.player.current_track
        if not current_track:
            # If nothing playing, play the last track
            if current_playlist.get_track_count() > 0:
                self.play_file(current_playlist.get_track_at(current_playlist.get_track_count() - 1))
            return
        
        # Find index of current track
        tracks = current_playlist.get_tracks()
        try:
            current_index = tracks.index(current_track)
        except ValueError:
            # Current track not in playlist, play last track
            if current_playlist.get_track_count() > 0:
                self.play_file(current_playlist.get_track_at(current_playlist.get_track_count() - 1))
            return
        
        # Play previous track or loop to end
        if self.player.shuffle:
            # Play random track
            import random
            prev_index = random.randint(0, current_playlist.get_track_count() - 1)
            while prev_index == current_index and current_playlist.get_track_count() > 1:
                prev_index = random.randint(0, current_playlist.get_track_count() - 1)
            self.play_file(current_playlist.get_track_at(prev_index))
        else:
            # Play previous track in order
            prev_index = (current_index - 1) % current_playlist.get_track_count()
            self.play_file(current_playlist.get_track_at(prev_index))
    
    def change_volume(self, value):
        """Change player volume"""
        volume = value / 100.0
        self.player.set_volume(volume)
    
    def toggle_shuffle(self, enabled):
        """Toggle shuffle mode"""
        self.player.set_shuffle(enabled)
    
    def toggle_repeat(self, enabled):
        """Toggle repeat mode"""
        self.player.set_repeat(enabled)
    
    def change_theme(self, theme_name):
        """Change the application theme"""
        if self.theme_manager.set_theme(theme_name):
            self.theme_manager.apply_theme_to_widget(self)
            self.update_theme_visual()
    
    def update_theme_visual(self):
        """Update the theme-specific visual (cassette or vinyl)"""
        current_theme = self.theme_manager.get_current_theme()
        if current_theme:
            # Get SVG data for the current theme
            if self.theme_manager.current_theme == "Cassette Mode":
                svg_data = current_theme.get_cassette_svg()
            elif self.theme_manager.current_theme == "Vinyl View":
                svg_data = current_theme.get_vinyl_svg()
            else:
                # Default to cassette if unknown theme
                svg_data = self.theme_manager.get_theme("Cassette Mode").get_cassette_svg()
            
            # Load SVG data into the SVG widget
            self.theme_visual.load(QByteArray(svg_data.encode()))
    
    def change_visualization(self, viz_type):
        """Change the visualization type"""
        self.visualizer.set_visualization_type(viz_type)
    
    def create_new_playlist(self):
        """Create a new playlist"""
        name, ok = QInputDialog.getText(self, "New Playlist", "Enter playlist name:")
        if ok and name:
            self.playlist_manager.create_playlist(name)
    
    def rename_current_playlist(self):
        """Rename the current playlist"""
        current_name = self.playlist_selector.currentText()
        new_name, ok = QInputDialog.getText(
            self, "Rename Playlist", "Enter new name:", text=current_name
        )
        if ok and new_name and new_name != current_name:
            self.playlist_manager.rename_playlist(current_name, new_name)
    
    def delete_current_playlist(self):
        """Delete the current playlist"""
        current_name = self.playlist_selector.currentText()
        reply = QMessageBox.question(
            self, "Delete Playlist",
            f"Are you sure you want to delete the playlist '{current_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.playlist_manager.delete_playlist(current_name)
    
    def change_playlist(self, playlist_name):
        """Change the current active playlist"""
        if playlist_name:
            self.playlist_manager.set_current_playlist(playlist_name)
            self.update_playlist_content()
    
    def update_playlist_selector(self):
        """Update the playlist selector with available playlists"""
        self.playlist_selector.clear()
        self.playlist_selector.addItems(self.playlist_manager.get_playlist_names())
        
        # Set current playlist
        current_playlist = self.playlist_manager.current_playlist
        if current_playlist:
            index = self.playlist_selector.findText(current_playlist)
            if index >= 0:
                self.playlist_selector.setCurrentIndex(index)
    
    def update_playlist_content(self):
        """Update the playlist content view"""
        self.playlist_list.clear()
        
        current_playlist = self.playlist_manager.get_current_playlist()
        if not current_playlist:
            return
        
        # Add all tracks to the list
        for track_path in current_playlist.get_tracks():
            # Get metadata for the track
            metadata = self.metadata_manager.get_metadata(track_path)
            
            # Create display text
            if metadata:
                display_text = f"{metadata['title']} - {metadata['artist']}"
            else:
                display_text = os.path.basename(track_path)
            
            # Create list item
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, track_path)
            self.playlist_list.addItem(item)
    
    def library_item_double_clicked(self, item):
        """Handle double click on library item"""
        file_path = item.data(Qt.UserRole)
        if file_path:
            # Also add to current playlist if not already there
            current_playlist = self.playlist_manager.get_current_playlist()
            if current_playlist and file_path not in current_playlist.get_tracks():
                self.playlist_manager.add_track_to_playlist(
                    self.playlist_manager.current_playlist, file_path
                )
            
            # Play the file
            self.play_file(file_path)
    
    def playlist_item_double_clicked(self, item):
        """Handle double click on playlist item"""
        file_path = item.data(Qt.UserRole)
        if file_path:
            self.play_file(file_path)
    
    def show_about_dialog(self):
        """Show the about dialog"""
        QMessageBox.about(
            self, "About RetroJukebox",
            "RetroJukebox\n\n"
            "A desktop music player with retro-styled UI themes that plays local audio files "
            "and features advanced visualizations.\n\n"
            "Features:\n"
            "- Play local MP3, FLAC, WAV, and OGG files\n"
            "- Display album art from audio metadata\n"
            "- 10 stunning visualization modes (Bars, Waves, Circles, Spectrum, etc.)\n"
            "- 10 color themes with customizable effects\n"
            "- Background patterns and special effects\n"
            "- Retro UI themes (Cassette Mode and Vinyl View)\n"
            "- Create and manage playlists\n"
            "- Beat detection and responsive visualizations\n"
            "- Support for systems with limited resources\n\n"
            "Version: 2.0"
        )
    
    # Slots for signals
    
    def on_track_started(self, track_path):
        """Handle track started playing"""
        # Update UI
        metadata = self.metadata_manager.get_metadata(track_path)
        
        if metadata:
            self.track_title_label.setText(metadata['title'])
            self.artist_label.setText(metadata['artist'])
            self.album_label.setText(metadata['album'])
            
            # Format duration
            duration = metadata.get('duration', 0)
            duration_str = self.format_time(duration)
            self.duration_label.setText(duration_str)
            
            # Display audio quality information
            audio_quality = []
            
            # Add bitrate if available
            if 'bitrate' in metadata and metadata['bitrate']:
                kbps = int(metadata['bitrate'] / 1000)
                audio_quality.append(f"{kbps} kbps")
            
            # Add sample rate if available
            if 'sample_rate' in metadata and metadata['sample_rate']:
                sample_rate = int(metadata['sample_rate'] / 1000)
                audio_quality.append(f"{sample_rate} kHz")
            
            # Add audio mode if available (stereo/mono)
            if 'mode' in metadata and metadata['mode']:
                audio_quality.append(metadata['mode'])
                
            # Display the quality info
            if audio_quality:
                self.audio_quality_label.setText(" | ".join(audio_quality))
            else:
                self.audio_quality_label.setText("")
                
            # Update album art display
            album_art = self.metadata_manager.get_album_art(track_path)
            if album_art:
                self.album_art_label.setPixmap(album_art.scaled(
                    self.album_art_label.width(), 
                    self.album_art_label.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))
            
            # Set slider maximum
            self.position_slider.setMaximum(duration)
        else:
            # Use filename if metadata not available
            filename = os.path.basename(track_path)
            name, _ = os.path.splitext(filename)
            
            self.track_title_label.setText(name)
            self.artist_label.setText("Unknown Artist")
            self.album_label.setText("Unknown Album")
            self.duration_label.setText("0:00")
            
            # Set slider to default maximum
            self.position_slider.setMaximum(100)
        
        # Reset position slider
        self.position_slider.setValue(0)
        self.position_label.setText("0:00")
        
        # Update button state
        self.playback_controls.pauseButton.setText("Pause")
        
        # Update status bar
        self.statusBar().showMessage(f"Playing: {metadata['title'] if metadata else os.path.basename(track_path)}")
    
    def on_track_ended(self):
        """Handle track finished playing"""
        # If repeat is enabled, play the same track again
        if self.player.repeat and self.player.current_track:
            self.play_file(self.player.current_track)
        else:
            # Otherwise play the next track
            self.play_next()
    
    def on_track_position_changed(self, position, duration):
        """Handle track position update"""
        # Only update if not dragging slider
        if not self.position_slider.isSliderDown():
            self.position_slider.setValue(position)
        
        # Update position label
        self.position_label.setText(self.format_time(position))
        
        # Update duration label if it changed
        if duration > 0:
            self.duration_label.setText(self.format_time(duration))
            self.position_slider.setMaximum(duration)
    
    def on_track_error(self, error_message):
        """Handle track playback error"""
        QMessageBox.warning(self, "Playback Error", error_message)
        self.statusBar().showMessage(f"Error: {error_message}")
    
    def on_scan_finished(self, file_list):
        """Handle file scanning finished"""
        # Clear library list
        self.library_list.clear()
        
        # Add all files to the list
        for file_path in file_list:
            # Get metadata for the file
            metadata = self.metadata_manager.get_metadata(file_path)
            
            # Create display text
            if metadata:
                display_text = f"{metadata['title']} - {metadata['artist']}"
            else:
                display_text = os.path.basename(file_path)
            
            # Create list item
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, file_path)
            self.library_list.addItem(item)
        
        # Update status bar
        self.statusBar().showMessage(f"Scan complete: {len(file_list)} files found")
    
    def on_scan_progress(self, current, total):
        """Handle file scanning progress update"""
        self.statusBar().showMessage(f"Scanning: {current} of {total} files...")
    
    def on_file_manager_error(self, error_message):
        """Handle file manager error"""
        QMessageBox.warning(self, "File Error", error_message)
        self.statusBar().showMessage(f"Error: {error_message}")
    
    def on_metadata_error(self, error_message):
        """Handle metadata extraction error"""
        # Just log the error, don't show a dialog for every file
        print(f"Metadata error: {error_message}")
    
    def on_playlist_added(self, playlist_name):
        """Handle playlist added"""
        self.update_playlist_selector()
        self.statusBar().showMessage(f"Playlist '{playlist_name}' created")
    
    def on_playlist_removed(self, playlist_name):
        """Handle playlist removed"""
        self.update_playlist_selector()
        self.statusBar().showMessage(f"Playlist '{playlist_name}' deleted")
    
    def on_playlist_updated(self, playlist_name):
        """Handle playlist updated"""
        # Only update UI if this is the current playlist
        if playlist_name == self.playlist_manager.current_playlist:
            self.update_playlist_content()
        
        self.statusBar().showMessage(f"Playlist '{playlist_name}' updated")
    
    def on_playlist_error(self, error_message):
        """Handle playlist error"""
        QMessageBox.warning(self, "Playlist Error", error_message)
        self.statusBar().showMessage(f"Error: {error_message}")
    
    def on_visualization_updated(self, pixmap):
        """Handle visualization update"""
        self.visualizer_label.setPixmap(pixmap)
    
    def on_theme_changed(self, theme_name):
        """Handle theme changed"""
        self.statusBar().showMessage(f"Theme changed to '{theme_name}'")
        self.update_theme_visual()
    
    def on_position_slider_pressed(self):
        """Handle position slider being pressed (start dragging)"""
        # Nothing to do here, just stop updating the slider from player
        pass
    
    def on_position_slider_released(self):
        """Handle position slider being released (end dragging)"""
        # Seek to the selected position
        position = self.position_slider.value()
        self.player.set_position(position)
    
    def on_position_slider_value_changed(self, value):
        """Handle position slider value changed while dragging"""
        # Update position label while dragging
        self.position_label.setText(self.format_time(value))
    
    def format_time(self, seconds):
        """Format time in seconds to mm:ss format"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Clean up resources
        self.player.cleanup()
        self.visualizer.stop()
        
        # Accept the event
        event.accept()
        
    # New visualization methods
    def set_visualization_type(self, viz_type):
        """Set the visualization type"""
        self.visualizer.set_visualization_type(viz_type)
        self.statusBar().showMessage(f"Visualization changed to {viz_type}")
        
    def set_color_scheme(self, scheme):
        """Set the color scheme"""
        self.visualizer.set_color_scheme(scheme)
        self.statusBar().showMessage(f"Color scheme changed to {scheme}")
        
    def set_background_pattern(self, pattern):
        """Set the background pattern"""
        self.visualizer.set_background_pattern(pattern)
        self.statusBar().showMessage(f"Background pattern changed to {pattern}")
        
    def toggle_visualization_effect(self, effect_name):
        """Toggle a visualization effect"""
        self.visualizer.toggle_effect(effect_name)
        status = "enabled" if getattr(self.visualizer, f"{effect_name}_effect", False) else "disabled"
        if effect_name == "mirror":
            status = "enabled" if self.visualizer.mirror_mode else "disabled"
        elif effect_name == "invert":
            status = "enabled" if self.visualizer.invert_colors else "disabled"
        elif effect_name == "song_info":
            status = "enabled" if self.visualizer.show_song_info else "disabled"
        elif effect_name == "fps":
            status = "enabled" if self.visualizer.show_fps else "disabled"
        elif effect_name == "time":
            status = "enabled" if self.visualizer.show_time else "disabled"
        
        self.statusBar().showMessage(f"{effect_name.replace('_', ' ').title()} {status}")
        
    def cycle_visualization(self):
        """Cycle through visualization types"""
        new_viz = self.visualizer.cycle_visualization_type()
        self.statusBar().showMessage(f"Visualization changed to {new_viz}")
        
    def cycle_color_scheme(self):
        """Cycle through color schemes"""
        new_scheme = self.visualizer.cycle_color_scheme()
        self.statusBar().showMessage(f"Color scheme changed to {new_scheme}")
        
    def update_song_info_display(self):
        """Update song information in the visualizer"""
        if hasattr(self, 'current_track') and self.current_track:
            metadata = self.metadata_manager.get_metadata(self.current_track)
            self.visualizer.set_song_info(
                metadata.get('title', os.path.basename(self.current_track)),
                metadata.get('artist', 'Unknown Artist'),
                metadata.get('album', 'Unknown Album')
            )
>>>>>>> 7931bac3b70b4ade7d98445fc1a06d706a28aa92
