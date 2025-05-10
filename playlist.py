"""
Playlist management module
"""

import os
import json
from PyQt5.QtCore import QObject, pyqtSignal

class Playlist(QObject):
    """
    Class to represent a single playlist with tracks
    """
    
    def __init__(self, name="New Playlist"):
        super().__init__()
        self.name = name
        self.tracks = []  # List of file paths
    
    def add_track(self, track_path):
        """Add a track to the playlist"""
        if track_path not in self.tracks:
            self.tracks.append(track_path)
    
    def remove_track(self, index):
        """Remove a track by index"""
        if 0 <= index < len(self.tracks):
            del self.tracks[index]
    
    def move_track_up(self, index):
        """Move a track up in the playlist"""
        if 0 < index < len(self.tracks):
            self.tracks[index], self.tracks[index-1] = self.tracks[index-1], self.tracks[index]
    
    def move_track_down(self, index):
        """Move a track down in the playlist"""
        if 0 <= index < len(self.tracks) - 1:
            self.tracks[index], self.tracks[index+1] = self.tracks[index+1], self.tracks[index]
    
    def clear(self):
        """Clear all tracks from the playlist"""
        self.tracks = []
    
    def get_tracks(self):
        """Get all tracks in the playlist"""
        return self.tracks
    
    def get_track_count(self):
        """Get the number of tracks in the playlist"""
        return len(self.tracks)
    
    def get_track_at(self, index):
        """Get track at specific index"""
        if 0 <= index < len(self.tracks):
            return self.tracks[index]
        return None
        
    def sort_by_filename(self):
        """Sort tracks by filename"""
        self.tracks.sort(key=lambda x: os.path.basename(x).lower())
        
    def sort_by_filepath(self):
        """Sort tracks by full filepath"""
        self.tracks.sort()
        
    def search_tracks(self, search_term):
        """
        Search tracks by filename
        
        Args:
            search_term (str): Search term to look for in filenames
            
        Returns:
            list: Tracks that match the search term
        """
        search_term = search_term.lower()
        return [track for track in self.tracks 
                if search_term in os.path.basename(track).lower()]

class PlaylistManager(QObject):
    """
    Class to manage multiple playlists
    """
    playlist_added = pyqtSignal(str)
    playlist_removed = pyqtSignal(str)
    playlist_updated = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.playlists = {}  # Dictionary of name -> Playlist
        self.current_playlist = None
        
        # Add a default playlist
        self._add_default_playlist()
    
    def _add_default_playlist(self):
        """Create the default playlist"""
        default_playlist = Playlist("Default")
        self.playlists["Default"] = default_playlist
        self.current_playlist = "Default"
    
    def create_playlist(self, name):
        """
        Create a new playlist
        
        Args:
            name (str): Name of the playlist
        """
        if name in self.playlists:
            self.error.emit(f"Playlist '{name}' already exists")
            return False
        
        self.playlists[name] = Playlist(name)
        self.playlist_added.emit(name)
        return True
    
    def delete_playlist(self, name):
        """
        Delete a playlist
        
        Args:
            name (str): Name of the playlist to delete
        """
        if name not in self.playlists:
            self.error.emit(f"Playlist '{name}' does not exist")
            return False
        
        # Don't delete the last playlist
        if len(self.playlists) <= 1:
            self.error.emit("Cannot delete the last playlist")
            return False
        
        # Update current playlist if needed
        if self.current_playlist == name:
            # Find a new current playlist
            for playlist_name in self.playlists:
                if playlist_name != name:
                    self.current_playlist = playlist_name
                    break
        
        # Delete the playlist
        del self.playlists[name]
        self.playlist_removed.emit(name)
        return True
    
    def rename_playlist(self, old_name, new_name):
        """
        Rename a playlist
        
        Args:
            old_name (str): Current name of the playlist
            new_name (str): New name for the playlist
        """
        if old_name not in self.playlists:
            self.error.emit(f"Playlist '{old_name}' does not exist")
            return False
        
        if new_name in self.playlists:
            self.error.emit(f"Playlist '{new_name}' already exists")
            return False
        
        # Create a new playlist with the new name
        self.playlists[new_name] = self.playlists[old_name]
        self.playlists[new_name].name = new_name
        
        # Update current playlist if needed
        if self.current_playlist == old_name:
            self.current_playlist = new_name
        
        # Delete the old playlist
        del self.playlists[old_name]
        
        self.playlist_removed.emit(old_name)
        self.playlist_added.emit(new_name)
        return True
    
    def get_playlist(self, name):
        """
        Get a playlist by name
        
        Args:
            name (str): Name of the playlist
            
        Returns:
            Playlist: The requested playlist, or None if not found
        """
        return self.playlists.get(name)
    
    def get_current_playlist(self):
        """
        Get the current playlist
        
        Returns:
            Playlist: The current playlist
        """
        return self.playlists.get(self.current_playlist)
    
    def set_current_playlist(self, name):
        """
        Set the current playlist
        
        Args:
            name (str): Name of the playlist to set as current
        """
        if name in self.playlists:
            self.current_playlist = name
            return True
        
        self.error.emit(f"Playlist '{name}' does not exist")
        return False
    
    def get_playlist_names(self):
        """
        Get the names of all playlists
        
        Returns:
            list: List of playlist names
        """
        return list(self.playlists.keys())
    
    def add_track_to_playlist(self, playlist_name, track_path):
        """
        Add a track to a playlist
        
        Args:
            playlist_name (str): Name of the playlist
            track_path (str): Path to the track file
        """
        if playlist_name not in self.playlists:
            self.error.emit(f"Playlist '{playlist_name}' does not exist")
            return False
        
        self.playlists[playlist_name].add_track(track_path)
        self.playlist_updated.emit(playlist_name)
        return True
    
    def add_tracks_to_playlist(self, playlist_name, track_paths):
        """
        Add multiple tracks to a playlist
        
        Args:
            playlist_name (str): Name of the playlist
            track_paths (list): List of paths to track files
        """
        if playlist_name not in self.playlists:
            self.error.emit(f"Playlist '{playlist_name}' does not exist")
            return False
        
        for track_path in track_paths:
            self.playlists[playlist_name].add_track(track_path)
        
        self.playlist_updated.emit(playlist_name)
        return True
    
    def save_playlists(self, directory):
        """
        Save all playlists to JSON files in the given directory
        
        Args:
            directory (str): Directory to save playlists in
        """
        try:
            os.makedirs(directory, exist_ok=True)
            
            # Save each playlist
            for name, playlist in self.playlists.items():
                file_path = os.path.join(directory, f"{name}.json")
                
                # Create playlist data
                playlist_data = {
                    'name': playlist.name,
                    'tracks': playlist.tracks
                }
                
                # Write to file
                with open(file_path, 'w') as f:
                    json.dump(playlist_data, f, indent=4)
            
            return True
        
        except Exception as e:
            self.error.emit(f"Error saving playlists: {str(e)}")
            return False
    
    def load_playlists(self, directory):
        """
        Load playlists from JSON files in the given directory
        
        Args:
            directory (str): Directory to load playlists from
        """
        try:
            if not os.path.exists(directory):
                self.error.emit(f"Directory not found: {directory}")
                return False
            
            # Clear existing playlists
            self.playlists = {}
            
            # Find playlist files
            playlist_files = [f for f in os.listdir(directory) if f.endswith('.json')]
            
            if not playlist_files:
                # No playlists found, create default
                self._add_default_playlist()
                return True
            
            # Load each playlist
            for file_name in playlist_files:
                file_path = os.path.join(directory, file_name)
                
                try:
                    with open(file_path, 'r') as f:
                        playlist_data = json.load(f)
                    
                    # Create playlist
                    name = playlist_data.get('name', os.path.splitext(file_name)[0])
                    playlist = Playlist(name)
                    
                    # Add tracks
                    for track in playlist_data.get('tracks', []):
                        playlist.add_track(track)
                    
                    # Add to playlists
                    self.playlists[name] = playlist
                    
                    # Signal playlist added
                    self.playlist_added.emit(name)
                
                except Exception as e:
                    self.error.emit(f"Error loading playlist {file_name}: {str(e)}")
            
            # If no playlists were loaded, create default
            if not self.playlists:
                self._add_default_playlist()
            else:
                # Set current playlist to first one
                self.current_playlist = next(iter(self.playlists))
            
            return True
        
        except Exception as e:
            self.error.emit(f"Error loading playlists: {str(e)}")
            self._add_default_playlist()
            return False
