import os
import json
from PyQt5.QtCore import QUrl, Qt

class PlaylistManager:
    """Manage playlists including saving and loading."""
    
    def __init__(self, player):
        """Initialize the playlist manager with a player instance."""
        self.player = player
        self.current_playlist_name = "Default"
        self.song_ratings = {}  # Store song ratings: {file_path: rating}
        
    def save_playlist(self, filepath, playlist_name=None):
        """Save the current playlist to a file."""
        playlist_data = {
            "name": playlist_name or self.current_playlist_name,
            "tracks": [],
            "ratings": self.song_ratings
        }
        
        # Get all tracks in the playlist
        for i in range(self.player.get_track_count()):
            url = self.player.get_media_url(i)
            if url.isLocalFile():
                file_path = url.toLocalFile()
                playlist_data["tracks"].append(file_path)
            else:
                # For non-local files, store the URL as string
                playlist_data["tracks"].append(url.toString())
        
        try:
            with open(filepath, 'w') as f:
                json.dump(playlist_data, f, indent=2)
            self.current_playlist_name = playlist_name or self.current_playlist_name
            return True
        except Exception as e:
            print(f"Error saving playlist: {e}")
            return False
    
    def load_playlist(self, filepath):
        """Load a playlist from a file."""
        try:
            with open(filepath, 'r') as f:
                playlist_data = json.load(f)
            
            # Clear current playlist
            self.player.clear_playlist()
            
            # Add tracks to playlist
            for track in playlist_data.get("tracks", []):
                if os.path.exists(track):
                    # Local file
                    url = QUrl.fromLocalFile(track)
                else:
                    # Try as URL
                    url = QUrl(track)
                
                self.player.add_to_playlist(url)
            
            # Load ratings if available
            if "ratings" in playlist_data:
                self.song_ratings = playlist_data["ratings"]
            
            # Set playlist name
            self.current_playlist_name = playlist_data.get("name", "Loaded Playlist")
            
            return True
        except Exception as e:
            print(f"Error loading playlist: {e}")
            return False
    
    def import_folder(self, folder_path):
        """Import all MP3 files from a folder."""
        if not os.path.isdir(folder_path):
            return 0
        
        count = 0
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.mp3'):
                    file_path = os.path.join(root, file)
                    url = QUrl.fromLocalFile(file_path)
                    self.player.add_to_playlist(url)
                    count += 1
        
        return count
    
    def set_song_rating(self, file_path, rating):
        """Set a rating (1-5) for a song."""
        if 1 <= rating <= 5:
            self.song_ratings[file_path] = rating
            return True
        return False
    
    def get_song_rating(self, file_path):
        """Get the rating for a song."""
        return self.song_ratings.get(file_path, 0)
    
    def filter_by_rating(self, min_rating=1):
        """Create a new playlist with songs above the specified rating."""
        filtered_tracks = []
        
        for file_path, rating in self.song_ratings.items():
            if rating >= min_rating and os.path.exists(file_path):
                filtered_tracks.append(file_path)
        
        # Clear current playlist
        self.player.clear_playlist()
        
        # Add filtered tracks
        for track in filtered_tracks:
            url = QUrl.fromLocalFile(track)
            self.player.add_to_playlist(url)
        
        return len(filtered_tracks)
