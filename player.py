<<<<<<< HEAD
from PyQt5.QtCore import QUrl, QTime, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
import os
from utils.audio import format_time, calculate_spectrum
import random

class AudioPlayer:
    """Audio player class that handles the audio playback functionality."""
    
    def __init__(self):
        """Initialize the audio player."""
        self.media_player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.media_player.setPlaylist(self.playlist)
        
        # Set initial volume (0-100)
        self.media_player.setVolume(70)
        
        # Playback settings
        self.is_shuffled = False
        self.repeat_mode = 0  # 0: No repeat, 1: Repeat track, 2: Repeat playlist
        self.previous_volume = 70
        self.playback_rate = 1.0
        
        # Connect signals
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.stateChanged.connect(self.state_changed)
        self.playlist.currentIndexChanged.connect(self.playlist_position_changed)
        
        # Callbacks to be set by UI
        self.duration_changed_callback = None
        self.position_changed_callback = None
        self.state_changed_callback = None
        self.track_changed_callback = None
        
    def set_callbacks(self, duration_changed=None, position_changed=None, 
                      state_changed=None, track_changed=None):
        """Set the callback functions for player events."""
        self.duration_changed_callback = duration_changed
        self.position_changed_callback = position_changed
        self.state_changed_callback = state_changed
        self.track_changed_callback = track_changed
        
    def duration_changed(self, duration):
        """Handle duration changed event."""
        if self.duration_changed_callback:
            formatted_duration = format_time(duration)
            self.duration_changed_callback(duration, formatted_duration)
    
    def position_changed(self, position):
        """Handle position changed event."""
        if self.position_changed_callback:
            formatted_position = format_time(position)
            duration = self.media_player.duration()
            self.position_changed_callback(position, formatted_position, duration)
    
    def state_changed(self, state):
        """Handle state changed event."""
        if self.state_changed_callback:
            self.state_changed_callback(state)
    
    def playlist_position_changed(self, position):
        """Handle playlist position changed event."""
        if self.track_changed_callback and position >= 0:
            self.track_changed_callback(position)
    
    def add_to_playlist(self, url):
        """Add a file to the playlist."""
        self.playlist.addMedia(QMediaContent(url))
        return self.playlist.mediaCount() - 1
    
    def add_files_to_playlist(self, urls):
        """Add multiple files to the playlist."""
        for url in urls:
            self.add_to_playlist(url)
        return self.playlist.mediaCount()
    
    def clear_playlist(self):
        """Clear the playlist."""
        self.playlist.clear()
    
    def play(self):
        """Start playback."""
        self.media_player.play()
    
    def pause(self):
        """Pause playback."""
        self.media_player.pause()
    
    def stop(self):
        """Stop playback."""
        self.media_player.stop()
    
    def next_track(self):
        """Play the next track in the playlist."""
        self.playlist.next()
    
    def previous_track(self):
        """Play the previous track in the playlist."""
        self.playlist.previous()
    
    def set_position(self, position):
        """Set the playback position."""
        self.media_player.setPosition(position)
    
    def set_volume(self, volume):
        """Set the volume (0-100)."""
        self.media_player.setVolume(volume)
    
    def get_volume(self):
        """Get the current volume."""
        return self.media_player.volume()
    
    def toggle_mute(self):
        """Toggle mute state."""
        if self.media_player.volume() > 0:
            self.previous_volume = self.media_player.volume()
            self.media_player.setVolume(0)
        else:
            self.media_player.setVolume(self.previous_volume)
        return self.media_player.volume() == 0
    
    def set_playback_rate(self, rate):
        """Set playback speed (0.5-2.0)."""
        self.playback_rate = rate
        self.media_player.setPlaybackRate(rate)
    
    def toggle_shuffle(self):
        """Toggle shuffle mode."""
        self.is_shuffled = not self.is_shuffled
        if self.is_shuffled:
            self.playlist.setPlaybackMode(QMediaPlaylist.Random)
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        return self.is_shuffled
    
    def toggle_repeat(self):
        """Toggle repeat mode (0: None, 1: Track, 2: Playlist)."""
        self.repeat_mode = (self.repeat_mode + 1) % 3
        
        if self.repeat_mode == 0:  # No repeat
            if self.is_shuffled:
                self.playlist.setPlaybackMode(QMediaPlaylist.Random)
            else:
                self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        elif self.repeat_mode == 1:  # Repeat track
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        elif self.repeat_mode == 2:  # Repeat playlist
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            
        return self.repeat_mode
    
    def get_current_track_index(self):
        """Get the index of the current track."""
        return self.playlist.currentIndex()
    
    def set_current_track(self, index):
        """Set the current track by index."""
        return self.playlist.setCurrentIndex(index)
    
    def get_track_count(self):
        """Get the number of tracks in the playlist."""
        return self.playlist.mediaCount()
    
    def get_current_media(self):
        """Get the current media."""
        return self.playlist.currentMedia()
    
    def get_media_url(self, index):
        """Get the URL of a media by index."""
        return self.playlist.media(index).canonicalUrl()
    
    def get_state(self):
        """Get the current state of the player."""
        return self.media_player.state()
    
    def get_spectrum_data(self):
        """Get audio spectrum data for visualization."""
        # This is a simplified implementation
        # In a real app, you'd use QAudioProbe or similar
        if self.media_player.state() == QMediaPlayer.PlayingState:
            return calculate_spectrum(10)  # Return 10 values for visualization
        return [0] * 10  # Return empty data when not playing
=======
"""
Player module for handling audio playback functionality
Supports MP3, FLAC, WAV, and OGG audio formats
"""

import os
import time
import threading
import pygame
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class Player(QObject):
    """
    Audio player class that handles playing, pausing, and skipping tracks
    """
    track_started = pyqtSignal(str)
    track_ended = pyqtSignal()
    track_position_changed = pyqtSignal(int, int)  # current_position, total_duration
    track_error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        # Initialize pygame mixer with fallback for environments without audio
        self.audio_available = True
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Warning: No audio device available, running in silent mode")
            self.audio_available = False
        
        self.current_track = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.5
        self.shuffle = False
        self.repeat = False
        
        # Set up position tracking timer
        self.position_timer = QTimer()
        self.position_timer.setInterval(100)  # Update every 100ms
        self.position_timer.timeout.connect(self._update_position)
        
        # Set up end of track detection thread
        self.track_monitor = None
        self.monitor_running = False
    
    def _monitor_track_end(self):
        """Background thread to monitor when a track ends"""
        self.monitor_running = True
        while self.monitor_running:
            if self.is_playing and not pygame.mixer.music.get_busy() and not self.is_paused:
                # Signal that track has ended but don't stop the thread
                # This allows the UI to handle track completion and autoplay next track
                self.track_ended.emit()
                self.is_playing = False
                self.position_timer.stop()
                # Don't break from the loop - wait for next track to play
            time.sleep(0.1)
    
    def _update_position(self):
        """Update current track position and emit signal"""
        if self.is_playing and not self.is_paused and self.current_track:
            try:
                if self.audio_available:
                    # Real audio playback mode
                    current_pos = pygame.mixer.music.get_pos() // 1000  # Convert ms to seconds
                    if current_pos >= 0:  # Sometimes returns -1 on errors
                        sound = pygame.mixer.Sound(self.current_track)
                        total_length = sound.get_length()
                        self.track_position_changed.emit(current_pos, int(total_length))
                else:
                    # Silent mode - simulate progress
                    # Get current time in milliseconds since playback started
                    if not hasattr(self, 'silent_mode_start_time'):
                        self.silent_mode_start_time = time.time()
                        self.silent_mode_position = 0
                    
                    current_time = time.time()
                    elapsed = current_time - self.silent_mode_start_time
                    
                    # Simulate a 3-minute track
                    total_length = 180  # 3 minutes in seconds
                    position = min(int(elapsed), total_length)
                    
                    self.silent_mode_position = position
                    self.track_position_changed.emit(position, total_length)
                    
                    # Signal track ended if we reach the end
                    if position >= total_length:
                        self.track_ended.emit()
                        self.silent_mode_start_time = current_time  # Reset for next track
            except Exception as e:
                print(f"Error updating position: {e}")
    
    def play(self, track_path):
        """
        Play a track from the given path
        
        Args:
            track_path (str): Path to the audio file
        """
        try:
            if not os.path.exists(track_path):
                self.track_error.emit(f"File not found: {track_path}")
                return
                
            # Stop any existing playback
            if self.is_playing:
                self.stop()
            
            # Store current track and update states
            self.current_track = track_path
            self.is_playing = True
            self.is_paused = False
            
            # If audio is available, play the track
            if self.audio_available:
                # Load and play new track
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()
                
                # Start position timer
                self.position_timer.start()
                
                # Start end-of-track monitor
                if self.track_monitor is None or not self.track_monitor.is_alive():
                    self.track_monitor = threading.Thread(target=self._monitor_track_end)
                    self.track_monitor.daemon = True
                    self.track_monitor.start()
            else:
                # Simulate playback in silent mode - emit position changed signals
                self.position_timer.start()
                
                # For silent mode, we'll need an alternative way to detect track end
                # Let's use a timer to simulate a track that's 3 minutes long
                QTimer.singleShot(180000, self.track_ended.emit)  # 3 minutes
            
            # Emit signal that track started
            self.track_started.emit(track_path)
            
        except Exception as e:
            self.track_error.emit(f"Error playing track: {str(e)}")
    
    def pause(self):
        """Pause the currently playing track"""
        if self.is_playing and not self.is_paused:
            if self.audio_available:
                pygame.mixer.music.pause()
            self.is_paused = True
            self.position_timer.stop()
    
    def resume(self):
        """Resume playback of a paused track"""
        if self.is_playing and self.is_paused:
            if self.audio_available:
                pygame.mixer.music.unpause()
            self.is_paused = False
            self.position_timer.start()
    
    def stop(self):
        """Stop playback completely"""
        if self.audio_available:
            pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_track = None
        self.position_timer.stop()
        
        # Stop the track monitor thread
        self.monitor_running = False
        if self.track_monitor and self.track_monitor.is_alive():
            self.track_monitor.join(1.0)  # Wait for thread to finish with timeout
        self.track_monitor = None
    
    def set_volume(self, volume):
        """Set player volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def set_position(self, position_seconds):
        """Seek to a position in the current track"""
        if self.is_playing and self.current_track:
            try:
                # pygame.mixer doesn't support seeking, so we need to reload and skip
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.current_track)
                pygame.mixer.music.play(start=position_seconds)
                pygame.mixer.music.set_volume(self.volume)
                
                # Restore pause state if needed
                if self.is_paused:
                    pygame.mixer.music.pause()
                else:
                    self.position_timer.start()
            except Exception as e:
                self.track_error.emit(f"Error seeking: {str(e)}")
    
    def set_shuffle(self, enabled):
        """Enable or disable shuffle mode"""
        self.shuffle = enabled
    
    def set_repeat(self, enabled):
        """Enable or disable repeat mode"""
        self.repeat = enabled
    
    def cleanup(self):
        """Cleanup resources when application is closing"""
        self.stop()
        pygame.mixer.quit()
>>>>>>> 7931bac3b70b4ade7d98445fc1a06d706a28aa92
