"""
Metadata module for extracting and handling audio file metadata
"""

import os
import io
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3
from mutagen.id3._frames import APIC
from mutagen import File as MutagenFile

class MetadataManager(QObject):
    """
    Class to handle extraction and management of audio file metadata
    Supports MP3, FLAC, WAV, and OGG formats
    """
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
    
    def get_metadata(self, file_path):
        """
        Extract metadata from various audio formats (MP3, FLAC, WAV, OGG)
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            dict: Metadata including title, artist, album, etc.
        """
        try:
            if not os.path.exists(file_path):
                self.error.emit(f"File not found: {file_path}")
                return self._create_default_metadata(file_path)
            
            # Load appropriate audio handler based on file extension
            file_ext = os.path.splitext(file_path.lower())[1]
            audio = None
            
            if file_ext == '.mp3':
                audio = MP3(file_path)
            elif file_ext == '.flac':
                audio = FLAC(file_path)
            elif file_ext == '.wav':
                audio = WAVE(file_path)
            elif file_ext == '.ogg':
                audio = OggVorbis(file_path)
            else:
                # Try generic handler as fallback
                audio = MutagenFile(file_path)
            
            if audio is None:
                return self._create_default_metadata(file_path)
            
            # Default metadata with filename as fallback
            metadata = self._create_default_metadata(file_path)
            
            # Extract ID3 tags if available
            if hasattr(audio, 'tags') and audio.tags:
                tags = audio.tags
                
                # ID3 tags use different formats depending on version
                # Try to extract common tags
                if "TIT2" in tags:  # Title
                    metadata['title'] = str(tags["TIT2"])
                
                if "TPE1" in tags:  # Artist
                    metadata['artist'] = str(tags["TPE1"])
                
                if "TALB" in tags:  # Album
                    metadata['album'] = str(tags["TALB"])
                
                if "TDRC" in tags:  # Year
                    metadata['year'] = str(tags["TDRC"])
                
                if "TRCK" in tags:  # Track number
                    metadata['track'] = str(tags["TRCK"])
                
                if "TCON" in tags:  # Genre
                    metadata['genre'] = str(tags["TCON"])
            
            # Add duration
            if hasattr(audio, 'info') and hasattr(audio.info, 'length'):
                metadata['duration'] = int(audio.info.length)
            
            # Add audio quality information if available
            if hasattr(audio, 'info'):
                # Handle different audio format attributes safely
                try:
                    if hasattr(audio.info, 'bitrate'):
                        metadata['bitrate'] = audio.info.bitrate // 1000  # kbps
                    
                    # MP3 specific info
                    if isinstance(audio, MP3):
                        metadata['sample_rate'] = audio.info.sample_rate  # Hz
                        metadata['channels'] = 2 if audio.info.mode != 3 else 1
                        metadata['layer'] = audio.info.layer
                        metadata['version'] = audio.info.version
                    
                    # Generic attributes for other formats
                    else:
                        if hasattr(audio.info, 'sample_rate'):
                            metadata['sample_rate'] = audio.info.sample_rate
                        if hasattr(audio.info, 'channels'):
                            metadata['channels'] = audio.info.channels
                except Exception:
                    # Ignore errors in audio quality extraction
                    pass
            
            # Add file size
            try:
                metadata['file_size'] = os.path.getsize(file_path) // 1024  # KB
            except:
                pass
                
            return metadata
            
        except Exception as e:
            self.error.emit(f"Error extracting metadata: {str(e)}")
            return self._create_default_metadata(file_path)
    
    def get_album_art(self, file_path):
        """
        Extract album art from audio files (MP3, FLAC, OGG)
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            QPixmap: Album art as a QPixmap, or None if not found
        """
        try:
            if not os.path.exists(file_path):
                self.error.emit(f"File not found: {file_path}")
                return None
            
            file_ext = os.path.splitext(file_path.lower())[1]
            img_data = None
            
            # Extract album art based on file format
            if file_ext == '.mp3':
                # MP3 files - look for APIC frames in ID3 tags
                try:
                    audio = ID3(file_path)
                    for tag in audio.values():
                        if isinstance(tag, APIC):
                            img_data = tag.data
                            break
                except Exception:
                    pass
                    
            elif file_ext == '.flac':
                # FLAC files - look for PICTURE blocks
                try:
                    audio = FLAC(file_path)
                    if audio.pictures:
                        img_data = audio.pictures[0].data
                except Exception:
                    pass
                    
            elif file_ext == '.ogg':
                # OGG files - look for METADATA_BLOCK_PICTURE
                try:
                    audio = OggVorbis(file_path)
                    if 'METADATA_BLOCK_PICTURE' in audio:
                        import base64
                        picture_data = base64.b64decode(audio['METADATA_BLOCK_PICTURE'][0])
                        img_data = picture_data
                except Exception:
                    pass
            
            # Convert image data to QPixmap if found
            if img_data:
                qimg = QImage()
                qimg.loadFromData(img_data)
                return QPixmap.fromImage(qimg)
            
            return None
            
        except Exception as e:
            # Not all audio files have embedded art, so this is not always an error
            return None
    
    def _create_default_metadata(self, file_path):
        """
        Create default metadata from filename
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            dict: Basic metadata with filename
        """
        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)
        
        # Try to parse artist - title pattern
        title = name
        artist = "Unknown Artist"
        
        if " - " in name:
            parts = name.split(" - ", 1)
            artist = parts[0].strip()
            title = parts[1].strip()
        
        return {
            'title': title,
            'artist': artist,
            'album': "Unknown Album",
            'year': "",
            'track': "",
            'genre': "",
            'duration': 0,
            'file_path': file_path
        }
