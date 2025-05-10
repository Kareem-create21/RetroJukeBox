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
    
    def __init__(self):
        super().__init__()
        
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
