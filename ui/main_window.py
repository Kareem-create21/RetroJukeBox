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
    
    def __init__(self):
        super().__init__()
        
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
