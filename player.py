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
