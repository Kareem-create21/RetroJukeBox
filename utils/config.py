import os
import json
import configparser
from PyQt5.QtCore import QSettings, QDir

class ConfigManager:
    """
    Manage application configuration settings.
    Handles reading and writing settings to disk.
    """
    
    def __init__(self):
        """Initialize the configuration manager."""
        self.settings = QSettings()
        self.config_dir = os.path.join(QDir.homePath(), ".retromp3player")
        self.config_file = os.path.join(self.config_dir, "config.ini")
        self.playlists_dir = os.path.join(self.config_dir, "playlists")
        
        # Create config directory if it doesn't exist
        self._ensure_directories_exist()
        
        # Default settings
        self.default_settings = {
            "General": {
                "theme": "dark",
                "minimize_to_tray": "True",
                "last_volume": "70",
            },
            "Playback": {
                "skip_timer_enabled": "False",
                "skip_timer_seconds": "30",
                "fade_enabled": "False",
                "playback_speed": "1.0",
            },
            "Equalizer": {
                "preset": "Default",
                "bands": "0,0,0,0,0,0,0,0,0,0",
            }
        }
        
        # Load settings
        self.config = self._load_config()
    
    def _ensure_directories_exist(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.playlists_dir, exist_ok=True)
    
    def _load_config(self):
        """Load configuration from file."""
        config = configparser.ConfigParser()
        
        # Load defaults
        for section, options in self.default_settings.items():
            config[section] = {}
            for key, value in options.items():
                config[section][key] = value
        
        # Try to load from file
        if os.path.exists(self.config_file):
            try:
                config.read(self.config_file)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return config
    
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, section, key, fallback=None):
        """Get a configuration value."""
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def get_int(self, section, key, fallback=0):
        """Get an integer configuration value."""
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def get_float(self, section, key, fallback=0.0):
        """Get a float configuration value."""
        try:
            return self.config.getfloat(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def get_bool(self, section, key, fallback=False):
        """Get a boolean configuration value."""
        try:
            return self.config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def set(self, section, key, value):
        """Set a configuration value."""
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = str(value)
    
    def get_last_playlist(self):
        """Get the last used playlist."""
        return self.settings.value("last_playlist", [])
    
    def set_last_playlist(self, playlist_files):
        """Save the last used playlist."""
        self.settings.setValue("last_playlist", playlist_files)
    
    def get_last_track_index(self):
        """Get the last played track index."""
        return self.settings.value("last_track_index", 0, type=int)
    
    def set_last_track_index(self, index):
        """Save the last played track index."""
        self.settings.setValue("last_track_index", index)
    
    def get_song_ratings(self):
        """Get song ratings dictionary."""
        return self.settings.value("song_ratings", {})
    
    def set_song_ratings(self, ratings):
        """Save song ratings dictionary."""
        self.settings.setValue("song_ratings", ratings)
    
    def save_playlist(self, name, tracks, ratings=None):
        """Save a playlist to a file."""
        if not name:
            return False
        
        # Create playlist data
        playlist_data = {
            "name": name,
            "tracks": tracks,
            "ratings": ratings or {}
        }
        
        # Save to file
        filename = os.path.join(self.playlists_dir, f"{name}.rpl")
        try:
            with open(filename, 'w') as f:
                json.dump(playlist_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving playlist: {e}")
            return False
    
    def load_playlist(self, name):
        """Load a playlist from a file."""
        if not name:
            return None
        
        filename = os.path.join(self.playlists_dir, f"{name}.rpl")
        
        if not os.path.exists(filename):
            # Try with .rpl extension added
            if not filename.endswith('.rpl'):
                filename = f"{filename}.rpl"
            
            if not os.path.exists(filename):
                return None
        
        try:
            with open(filename, 'r') as f:
                playlist_data = json.dump(f)
            return playlist_data
        except Exception as e:
            print(f"Error loading playlist: {e}")
            return None
    
    def list_playlists(self):
        """List all saved playlists."""
        playlists = []
        for filename in os.listdir(self.playlists_dir):
            if filename.endswith('.rpl'):
                playlists.append(os.path.splitext(filename)[0])
        return playlists
