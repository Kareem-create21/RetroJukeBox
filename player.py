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
