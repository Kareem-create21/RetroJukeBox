import random
import math
from PyQt5.QtCore import QTime

def format_time(milliseconds):
    """
    Format milliseconds as mm:ss or hh:mm:ss depending on length.
    
    Args:
        milliseconds (int): Time in milliseconds
        
    Returns:
        str: Formatted time string
    """
    if milliseconds <= 0:
        return "00:00"
    
    # Convert to QTime for easy formatting
    total_seconds = int(milliseconds / 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    # Format based on length
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def calculate_spectrum(num_bands, seed=None):
    """
    Calculate a simulated audio spectrum for visualization.
    In a real application, this would use actual audio data.
    
    Args:
        num_bands (int): Number of frequency bands
        seed (int, optional): Random seed for consistent results
        
    Returns:
        list: List of spectrum values between 0 and 1
    """
    if seed is not None:
        random.seed(seed)
    
    # Generate random spectrum with some pattern to look like music
    spectrum = []
    
    # Create a pattern that resembles audio spectrum (higher in the middle frequencies)
    for i in range(num_bands):
        # Create a curve peaking in the middle
        pos = i / (num_bands - 1)  # 0 to 1
        
        # Base value with curve that peaks in the middle
        base_curve = 0.5 + 0.5 * math.sin(pos * math.pi)
        
        # Add some randomness
        random_factor = 0.3 * random.random()
        
        # Combine base curve with randomness
        value = base_curve + random_factor
        
        # Ensure value is between 0 and 1
        value = max(0, min(1, value))
        
        spectrum.append(value)
    
    return spectrum

def get_time_remaining(position, duration):
    """
    Calculate remaining time in milliseconds.
    
    Args:
        position (int): Current position in milliseconds
        duration (int): Total duration in milliseconds
        
    Returns:
        int: Remaining time in milliseconds
    """
    if duration <= 0:
        return 0
    
    return max(0, duration - position)

def format_time_remaining(position, duration):
    """
    Format the remaining time as a string.
    
    Args:
        position (int): Current position in milliseconds
        duration (int): Total duration in milliseconds
        
    Returns:
        str: Formatted remaining time with a minus sign
    """
    remaining = get_time_remaining(position, duration)
    
    # Use the minus sign to indicate remaining time
    return f"-{format_time(remaining)}"

def apply_fade(volume, max_volume, duration, position, fade_in_duration=2000, fade_out_duration=2000):
    """
    Calculate volume adjustment for fade in/out effects.
    
    Args:
        volume (int): Current volume level (0-100)
        max_volume (int): Maximum volume level
        duration (int): Total track duration in milliseconds
        position (int): Current position in milliseconds
        fade_in_duration (int): Fade in duration in milliseconds
        fade_out_duration (int): Fade out duration in milliseconds
        
    Returns:
        int: Adjusted volume level (0-100)
    """
    # Don't fade if duration is too short
    if duration < (fade_in_duration + fade_out_duration):
        return volume
    
    # Calculate fade in effect
    if position < fade_in_duration:
        fade_factor = position / fade_in_duration
        return int(volume * fade_factor)
    
    # Calculate fade out effect
    if position > (duration - fade_out_duration):
        remaining = duration - position
        fade_factor = remaining / fade_out_duration
        return int(volume * fade_factor)
    
    # Normal volume in the middle
    return volume

def format_bitrate(bitrate):
    """
    Format bitrate in kbps.
    
    Args:
        bitrate (int): Bitrate in bits per second
        
    Returns:
        str: Formatted bitrate
    """
    if bitrate <= 0:
        return "Unknown"
    
    # Convert to kbps
    kbps = bitrate / 1000
    return f"{int(kbps)} kbps"

def format_sample_rate(sample_rate):
    """
    Format sample rate in kHz.
    
    Args:
        sample_rate (int): Sample rate in Hz
        
    Returns:
        str: Formatted sample rate
    """
    if sample_rate <= 0:
        return "Unknown"
    
    # Convert to kHz
    khz = sample_rate / 1000
    return f"{khz:.1f} kHz"

def format_file_size(size_bytes):
    """
    Format file size with appropriate units.
    
    Args:
        size_bytes (int): File size in bytes
        
    Returns:
        str: Formatted file size
    """
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < (1024 * 1024):
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < (1024 * 1024 * 1024):
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
