from mutagen import File
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
import os
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QImage, QPixmap

class MetadataManager:
    """Manage track metadata extraction and display."""
    
    @staticmethod
    def get_metadata(file_path):
        """Extract metadata from an MP3 file."""
        if not os.path.exists(file_path):
            return None
        
        try:
            audio = File(file_path)
            if audio is None:
                return None
            
            # Basic metadata dictionary
            metadata = {
                'title': 'Unknown Title',
                'artist': 'Unknown Artist',
                'album': 'Unknown Album',
                'genre': 'Unknown Genre',
                'year': '',
                'track_number': '',
                'duration': 0,
                'bitrate': 0,
                'sample_rate': 0,
                'channels': 0,
                'file_size': os.path.getsize(file_path),
                'has_album_art': False
            }
            
            # Get audio properties
            if hasattr(audio, 'info'):
                metadata['duration'] = int(audio.info.length * 1000)  # Convert to ms
                if hasattr(audio.info, 'bitrate'):
                    metadata['bitrate'] = audio.info.bitrate
                if hasattr(audio.info, 'sample_rate'):
                    metadata['sample_rate'] = audio.info.sample_rate
                if hasattr(audio.info, 'channels'):
                    metadata['channels'] = audio.info.channels
            
            # Get ID3 tags
            if hasattr(audio, 'tags') and audio.tags:
                tags = audio.tags
                
                # ID3v2 tags
                if hasattr(tags, 'getall'):
                    # Try to get the title
                    if 'TIT2' in tags:
                        metadata['title'] = str(tags['TIT2'])
                    
                    # Try to get the artist
                    if 'TPE1' in tags:
                        metadata['artist'] = str(tags['TPE1'])
                    
                    # Try to get the album
                    if 'TALB' in tags:
                        metadata['album'] = str(tags['TALB'])
                    
                    # Try to get the genre
                    if 'TCON' in tags:
                        metadata['genre'] = str(tags['TCON'])
                    
                    # Try to get the year
                    if 'TDRC' in tags:
                        metadata['year'] = str(tags['TDRC'])
                    elif 'TYER' in tags:
                        metadata['year'] = str(tags['TYER'])
                    
                    # Try to get the track number
                    if 'TRCK' in tags:
                        metadata['track_number'] = str(tags['TRCK'])
                    
                    # Check for album art
                    metadata['has_album_art'] = 'APIC:' in tags or 'APIC' in tags
                
                # More generic tag reading for other formats
                elif hasattr(tags, 'get'):
                    metadata['title'] = str(tags.get('title', ['Unknown Title'])[0])
                    metadata['artist'] = str(tags.get('artist', ['Unknown Artist'])[0])
                    metadata['album'] = str(tags.get('album', ['Unknown Album'])[0])
                    metadata['genre'] = str(tags.get('genre', ['Unknown Genre'])[0])
                    metadata['year'] = str(tags.get('date', [''])[0])
                    
                    # Check for album art
                    metadata['has_album_art'] = bool(tags.get('pictures', False))
            
            # If title is still unknown, use filename
            if metadata['title'] == 'Unknown Title':
                metadata['title'] = os.path.splitext(os.path.basename(file_path))[0]
            
            return metadata
        
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            # Return basic info with filename as title
            return {
                'title': os.path.splitext(os.path.basename(file_path))[0],
                'artist': 'Unknown Artist',
                'album': 'Unknown Album',
                'genre': 'Unknown Genre',
                'year': '',
                'track_number': '',
                'duration': 0,
                'bitrate': 0,
                'sample_rate': 0,
                'channels': 0,
                'file_size': os.path.getsize(file_path),
                'has_album_art': False
            }
    
    @staticmethod
    def get_album_art(file_path, default_size=(200, 200)):
        """Extract album art from an MP3 file."""
        if not os.path.exists(file_path):
            return None
        
        try:
            audio = File(file_path)
            if audio is None:
                return None
            
            # ID3 tags (MP3)
            if hasattr(audio, 'tags') and audio.tags:
                tags = audio.tags
                
                # ID3v2 APIC tag
                if hasattr(tags, 'getall'):
                    apic_frames = tags.getall('APIC') if hasattr(tags, 'getall') else []
                    
                    if apic_frames:
                        artwork = apic_frames[0]
                        img = QImage()
                        img.loadFromData(QByteArray(artwork.data))
                        if not img.isNull():
                            return QPixmap.fromImage(img)
                
                # More generic tag reading for other formats
                elif hasattr(tags, 'get') and 'pictures' in tags:
                    pictures = tags.get('pictures', [])
                    if pictures:
                        artwork_data = pictures[0].data
                        img = QImage()
                        img.loadFromData(QByteArray(artwork_data))
                        if not img.isNull():
                            return QPixmap.fromImage(img)
            
            return None
        
        except Exception as e:
            print(f"Error extracting album art: {e}")
            return None
    
    @staticmethod
    def format_bitrate(bitrate):
        """Format bitrate for display."""
        if bitrate > 0:
            return f"{int(bitrate / 1000)} kbps"
        return "Unknown"
    
    @staticmethod
    def format_sample_rate(sample_rate):
        """Format sample rate for display."""
        if sample_rate > 0:
            return f"{sample_rate / 1000:.1f} kHz"
        return "Unknown"
    
    @staticmethod
    def format_file_size(size_bytes):
        """Format file size for display."""
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
