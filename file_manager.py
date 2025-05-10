"""
File Manager module for managing local music files
"""

import os
from PyQt5.QtCore import QObject, pyqtSignal

class FileManager(QObject):
    """
    Class to handle browsing and managing local music files
    """
    scan_finished = pyqtSignal(list)
    scan_progress = pyqtSignal(int, int)  # progress, total
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        # Extended format support
        self.supported_formats = ['.mp3', '.flac', '.wav', '.ogg']
        self.music_files = []
        self.current_directory = None
    
    def scan_directory(self, directory_path):
        """
        Scan a directory for music files
        
        Args:
            directory_path (str): Path to the directory to scan
        """
        self.music_files = []
        self.current_directory = directory_path
        
        try:
            if not os.path.exists(directory_path):
                self.error.emit(f"Directory not found: {directory_path}")
                return
                
            # Walk through directory and find supported music files
            total_files = 0
            found_files = 0
            
            # First pass to count files
            for root, _, files in os.walk(directory_path):
                for file in files:
                    if any(file.lower().endswith(fmt) for fmt in self.supported_formats):
                        total_files += 1
            
            # Second pass to collect files
            for root, _, files in os.walk(directory_path):
                for file in files:
                    if any(file.lower().endswith(fmt) for fmt in self.supported_formats):
                        full_path = os.path.join(root, file)
                        self.music_files.append(full_path)
                        found_files += 1
                        self.scan_progress.emit(found_files, total_files)
            
            # Sort files by name
            self.music_files.sort()
            
            # Emit scan finished signal
            self.scan_finished.emit(self.music_files)
        
        except Exception as e:
            self.error.emit(f"Error scanning directory: {str(e)}")
    
    def get_files(self):
        """
        Get the list of found music files
        
        Returns:
            list: List of file paths
        """
        return self.music_files
    
    def get_file_details(self, file_path):
        """
        Get basic details about a file
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            dict: File details including name, size, etc.
        """
        try:
            if not os.path.exists(file_path):
                return None
                
            stat_info = os.stat(file_path)
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'size': stat_info.st_size,
                'modified': stat_info.st_mtime
            }
        except Exception as e:
            self.error.emit(f"Error getting file details: {str(e)}")
            return None
