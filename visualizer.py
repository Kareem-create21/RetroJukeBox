"""
Audio visualizer module
Enhanced with multiple visualization modes and effects
"""
from PyQt5.QtCore import QObject, QTimer, pyqtSignal, QRect, QPoint, Qt, QSize
from PyQt5.QtGui import (QPixmap, QPainter, QLinearGradient, QColor, QPen, QBrush, 
                        QRadialGradient, QPainterPath, QFont, QFontMetrics, QTransform,
                        QPolygon)
import pygame
import numpy as np
import math
import random
import time

class AudioVisualizer(QObject):
    """
    Class to create audio visualizations with enhanced effects
    """
    visualization_updated = pyqtSignal(QPixmap)
    
    def __init__(self, update_interval=50):
        """
        Initialize the visualizer
        
        Args:
            update_interval (int): Interval in ms between visualization updates
        """
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_visualization)
        self.update_interval = update_interval
        self.is_running = False
        
        # Set default dimensions and visualization type
        self.width = 500
        self.height = 300
        self.viz_type = "bars"  # Default visualization type
        self.color_scheme = "default"  # Default color scheme
        
        # State variables
        self.last_values = np.zeros(32)  # Increased resolution
        self.target_values = np.zeros(32)  # Increased resolution
        self.particle_positions = []
        self.particle_velocities = []
        self.spectrum_data = np.zeros((10, 32))  # For spectrum history
        self.beat_detected = False
        self.beat_time = 0
        self.beat_intensity = 0
        self.frame_counter = 0
        self.noise_offset = 0
        self.analyzer_mode = "standard"  # standard, detailed, spectrum
        
        # Particles for particle mode
        self.particles = []
        for _ in range(100):
            self.particles.append({
                'x': random.uniform(0, 1),
                'y': random.uniform(0, 1),
                'size': random.uniform(2, 8),
                'speed': random.uniform(0.001, 0.005),
                'angle': random.uniform(0, 2*math.pi),
                'color': random.uniform(0, 1)
            })
        
        # Additional visualization modes
        self.viz_modes = [
            "bars", "waves", "circles", "spectrum", 
            "particles", "equalizer", "waveform", 
            "3d-bars", "fireworks", "oscilloscope"
        ]
        
        # Enhanced color maps for different themes
        self.color_maps = {
            "default": [QColor(30, 144, 255), QColor(65, 105, 225)],    # Blue gradient
            "vintage": [QColor(139, 69, 19), QColor(160, 82, 45)],      # Brown gradient 
            "neon": [QColor(255, 0, 255), QColor(0, 255, 255)],         # Neon pink to cyan
            "retro": [QColor(255, 215, 0), QColor(255, 69, 0)],         # Gold to orange-red
            "monochrome": [QColor(240, 240, 240), QColor(50, 50, 50)],  # White to dark gray
            "sunset": [QColor(255, 165, 0), QColor(255, 0, 0)],         # Orange to red
            "forest": [QColor(34, 139, 34), QColor(0, 100, 0)],         # Green shades
            "ocean": [QColor(0, 191, 255), QColor(0, 0, 128)],          # Light blue to dark blue
            "candy": [QColor(255, 105, 180), QColor(147, 112, 219)],    # Pink to purple
            "fire": [QColor(255, 69, 0), QColor(255, 0, 0)]             # Orange-red to red
        }
        
        # Background patterns
        self.bg_pattern = "solid"  # solid, grid, dots, noise
        self.show_fps = False
        self.show_time = False
        self.frame_times = []
        self.last_frame_time = time.time()
        
        # Effect settings
        self.glow_effect = False
        self.motion_blur = False
        self.mirror_mode = False
        self.invert_colors = False
        self.show_song_info = False
        self.song_info = {"title": "", "artist": "", "album": ""}
    
    def start(self):
        """Start the visualization updates"""
        self.is_running = True
        self.timer.start(self.update_interval)
    
    def stop(self):
        """Stop the visualization updates"""
        self.is_running = False
        self.timer.stop()
    
    def set_size(self, width, height):
        """Set the size of the visualization"""
        self.width = width
        self.height = height
    
    def set_visualization_type(self, viz_type):
        """Set the visualization type"""
        if viz_type in self.viz_modes:
            self.viz_type = viz_type
    
    def set_color_scheme(self, scheme):
        """Set the color scheme"""
        if scheme in self.color_maps:
            self.color_scheme = scheme
    
    def set_song_info(self, title, artist, album):
        """Set current song information for display"""
        self.song_info = {"title": title, "artist": artist, "album": album}
    
    def toggle_effect(self, effect_name):
        """Toggle a visualization effect on/off"""
        if effect_name == "glow":
            self.glow_effect = not self.glow_effect
        elif effect_name == "motion_blur":
            self.motion_blur = not self.motion_blur
        elif effect_name == "mirror":
            self.mirror_mode = not self.mirror_mode
        elif effect_name == "invert":
            self.invert_colors = not self.invert_colors
        elif effect_name == "song_info":
            self.show_song_info = not self.show_song_info
        elif effect_name == "fps":
            self.show_fps = not self.show_fps
        elif effect_name == "time":
            self.show_time = not self.show_time
    
    def set_background_pattern(self, pattern):
        """Set background pattern"""
        self.bg_pattern = pattern
    
    def set_analyzer_mode(self, mode):
        """Set frequency analyzer mode"""
        self.analyzer_mode = mode
    
    def cycle_visualization_type(self):
        """Cycle to the next visualization type"""
        current_index = self.viz_modes.index(self.viz_type)
        next_index = (current_index + 1) % len(self.viz_modes)
        self.viz_type = self.viz_modes[next_index]
        return self.viz_type
    
    def cycle_color_scheme(self):
        """Cycle to the next color scheme"""
        schemes = list(self.color_maps.keys())
        current_index = schemes.index(self.color_scheme)
        next_index = (current_index + 1) % len(schemes)
        self.color_scheme = schemes[next_index]
        return self.color_scheme
    
    def _get_audio_data(self):
        """
        Get audio data from pygame mixer
        
        Returns:
            numpy.ndarray: Array of audio levels
        """
        # Check if pygame mixer is initialized and playing music
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            # We'll add some randomness but keep coherence with previous frame
            # Make sure dimensions match - using 32 elements now
            if len(self.target_values) != 32:
                self.target_values = np.zeros(32)
                self.last_values = np.zeros(32)
                
            self.target_values = np.random.rand(32) * 0.3 + 0.7 * self.target_values
            
            # Smooth transition
            self.last_values = 0.7 * self.last_values + 0.3 * self.target_values
            
            # Beat detection (simple implementation)
            current_avg = np.mean(self.target_values)
            if current_avg > 0.6 and current_avg > 1.5 * np.mean(self.last_values):
                self.beat_detected = True
                self.beat_time = time.time()
                self.beat_intensity = current_avg
            else:
                # Reset beat detection after a short time
                if time.time() - self.beat_time > 0.3:
                    self.beat_detected = False
            
            return self.last_values
        else:
            # If not playing, return zeros
            if len(self.last_values) != 32:
                self.last_values = np.zeros(32)
                
            self.last_values = self.last_values * 0.9  # Slowly fade out
            return self.last_values
    
    def _update_visualization(self):
        """Update the visualization and emit the updated pixmap"""
        # Calculate FPS
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)
        
        # Get audio data
        audio_data = self._get_audio_data()
        
        # Create new pixmap
        pixmap = QPixmap(self.width, self.height)
        
        # Apply background pattern
        if self.bg_pattern == "solid":
            bg_color = QColor(20, 20, 20)  # Dark background
            if self.invert_colors:
                bg_color = QColor(240, 240, 240)  # Light background when inverted
            pixmap.fill(bg_color)
        else:
            self._draw_patterned_background(pixmap)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get colors for the current color scheme
        colors = self.color_maps.get(self.color_scheme, self.color_maps["default"])
        
        # Invert colors if needed
        if self.invert_colors:
            colors = [QColor(255-c.red(), 255-c.green(), 255-c.blue()) for c in colors]
        
        # Choose visualization method based on type
        if self.viz_type == "bars":
            self._draw_bars(painter, audio_data, colors)
        elif self.viz_type == "waves":
            self._draw_waves(painter, audio_data, colors)
        elif self.viz_type == "circles":
            self._draw_circles(painter, audio_data, colors)
        elif self.viz_type == "spectrum":
            self._draw_spectrum(painter, audio_data, colors)
        elif self.viz_type == "particles":
            self._draw_particles(painter, audio_data, colors)
        elif self.viz_type == "equalizer":
            self._draw_equalizer(painter, audio_data, colors)
        elif self.viz_type == "waveform":
            self._draw_waveform(painter, audio_data, colors)
        elif self.viz_type == "3d-bars":
            self._draw_3d_bars(painter, audio_data, colors)
        elif self.viz_type == "fireworks":
            self._draw_fireworks(painter, audio_data, colors)
        elif self.viz_type == "oscilloscope":
            self._draw_oscilloscope(painter, audio_data, colors)
        
        # Add glow effect if enabled
        if self.glow_effect and self.beat_detected:
            self._apply_glow(painter, colors[0])
        
        # Draw song information if enabled
        if self.show_song_info:
            self._draw_song_info(painter, colors)
        
        # Show FPS if enabled
        if self.show_fps:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times) if self.frame_times else 0
            fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(10, 20, f"FPS: {fps:.1f}")
        
        # Show time if enabled
        if self.show_time:
            current_time_str = time.strftime("%H:%M:%S", time.localtime())
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(self.width - 80, 20, current_time_str)
        
        painter.end()
        
        # Mirror mode
        if self.mirror_mode:
            mirrored = QPixmap(self.width, self.height)
            mp = QPainter(mirrored)
            mp.drawPixmap(0, 0, pixmap)
            mp.drawPixmap(0, 0, pixmap.transformed(QTransform().scale(-1, 1).translate(-self.width, 0)))
            mp.end()
            pixmap = mirrored
        
        # Emit the updated pixmap
        self.visualization_updated.emit(pixmap)
        
        # Update frame counter
        self.frame_counter += 1
    
    def _draw_patterned_background(self, pixmap):
        """Draw a patterned background"""
        painter = QPainter(pixmap)
        painter.fillRect(0, 0, self.width, self.height, QColor(20, 20, 20))
        
        if self.bg_pattern == "grid":
            painter.setPen(QPen(QColor(40, 40, 40), 1))
            
            # Draw grid
            for x in range(0, self.width, 20):
                painter.drawLine(x, 0, x, self.height)
            
            for y in range(0, self.height, 20):
                painter.drawLine(0, y, self.width, y)
        
        elif self.bg_pattern == "dots":
            painter.setPen(QPen(QColor(40, 40, 40), 1))
            painter.setBrush(QBrush(QColor(40, 40, 40)))
            
            # Draw dots
            for x in range(10, self.width, 20):
                for y in range(10, self.height, 20):
                    painter.drawEllipse(QPoint(x, y), 2, 2)
        
        elif self.bg_pattern == "noise":
            # Perlin-like noise pattern
            self.noise_offset += 0.01
            for x in range(0, self.width, 4):
                for y in range(0, self.height, 4):
                    noise_val = (math.sin(x * 0.05 + self.noise_offset) + 
                                math.cos(y * 0.05 + self.noise_offset)) * 0.5 + 0.5
                    val = int(20 + noise_val * 30)
                    painter.fillRect(x, y, 4, 4, QColor(val, val, val))
        
        painter.end()
    
    def _apply_glow(self, painter, color):
        """Apply a glow effect"""
        glow_intensity = min(1.0, (time.time() - self.beat_time) * 5)
        glow_size = int(min(self.width, self.height) * 0.1 * (1 - glow_intensity))
        
        if glow_size > 0:
            # Draw radial gradient from center
            gradient = QRadialGradient(self.width/2, self.height/2, glow_size)
            gradient.setColorAt(0, QColor(color.red(), color.green(), color.blue(), 150))
            gradient.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(
                QPoint(int(self.width/2), int(self.height/2)), 
                glow_size * 2, 
                glow_size * 2
            )
    
    def _draw_song_info(self, painter, colors):
        """Draw the current song information"""
        if not any(self.song_info.values()):
            return
            
        # Create a semi-transparent background
        painter.fillRect(
            10, self.height - 70, self.width - 20, 60, 
            QColor(0, 0, 0, 180)
        )
        
        # Set font and color
        painter.setPen(colors[0])
        title_font = QFont("Arial", 12, QFont.Bold)
        info_font = QFont("Arial", 10)
        
        # Draw song title
        painter.setFont(title_font)
        painter.drawText(
            20, self.height - 50, 
            self.song_info["title"]
        )
        
        # Draw artist and album
        painter.setFont(info_font)
        painter.drawText(
            20, self.height - 30,
            f"{self.song_info['artist']} - {self.song_info['album']}"
        )
    
    def _draw_bars(self, painter, audio_data, colors):
        """Draw bar visualization"""
        bar_width = self.width / (len(audio_data) * 2)
        gradient = self._create_gradient(colors)
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(0, 0, 0, 0)))  # Transparent pen (no outline)
        
        for i, value in enumerate(audio_data):
            # Scale the value to the height
            bar_height = value * self.height * 0.8
            x = i * bar_width * 2 + bar_width / 2
            y = self.height - bar_height
            
            # Draw the bar
            painter.drawRect(QRect(int(x), int(y), int(bar_width), int(bar_height)))
            
            # Draw reflection
            reflection_gradient = QLinearGradient(0, self.height, 0, self.height + 50)
            reflection_gradient.setColorAt(0, QColor(colors[0].red(), colors[0].green(), colors[0].blue(), 120))
            reflection_gradient.setColorAt(1, QColor(colors[0].red(), colors[0].green(), colors[0].blue(), 0))
            painter.setBrush(QBrush(reflection_gradient))
            painter.drawRect(QRect(int(x), int(self.height), int(bar_width), int(bar_height * 0.2)))
        
    def _draw_waves(self, painter, audio_data, colors):
        """Draw wave visualization"""
        # Create a path for the wave
        path = QPainterPath()
        
        # Move to the first point
        path.moveTo(0, self.height / 2)
        
        # Create points for the wave
        points_count = 100
        for i in range(points_count):
            x = i * self.width / (points_count - 1)
            
            # Use different audio_data points to influence the wave
            idx = int(i * len(audio_data) / points_count)
            value = audio_data[idx] if idx < len(audio_data) else 0
            
            y = self.height / 2 + math.sin(i * 0.2) * value * self.height / 2
            path.lineTo(x, y)
        
        # Close the path to create a filled shape
        path.lineTo(self.width, self.height)
        path.lineTo(0, self.height)
        path.closeSubpath()
        
        # Fill with gradient
        gradient = self._create_gradient(colors, vertical=False)
        painter.fillPath(path, QBrush(gradient))
        
        # Draw the outline
        outline_pen = QPen(colors[0], 2)
        painter.setPen(outline_pen)
        painter.drawPath(path)
    
    def _draw_circles(self, painter, audio_data, colors):
        """Draw circle visualization"""
        # Center of the visualization
        center_x = self.width / 2
        center_y = self.height / 2
        
        # Create a radial gradient for the circles
        gradient = QRadialGradient(center_x, center_y, self.width / 3)
        gradient.setColorAt(0, colors[0])
        gradient.setColorAt(1, colors[1])
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(colors[0], 1))
        
        # Calculate the main circle size based on the average audio level
        avg_level = np.mean(audio_data)
        main_radius = avg_level * self.width / 3 + self.width / 10
        
        # Draw the main circle
        painter.drawEllipse(QPoint(int(center_x), int(center_y)), int(main_radius), int(main_radius))
        
        # Draw smaller circles based on individual audio levels
        for i, value in enumerate(audio_data[:16]):  # Use first 16 values for circles
            angle = 2 * math.pi * i / 16
            radius = main_radius * 0.6
            
            # Calculate position based on angle and a distance from center
            distance = main_radius * 1.2
            x = center_x + math.cos(angle) * distance
            y = center_y + math.sin(angle) * distance
            
            # Draw a circle with size based on the audio value
            circle_radius = value * self.width / 20 + 5
            
            # Get a color from the gradient
            color = self._interpolate_color(colors[0], colors[1], i / 16)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color.lighter(120), 1))
            
            painter.drawEllipse(QPoint(int(x), int(y)), int(circle_radius), int(circle_radius))
    
    def _draw_spectrum(self, painter, audio_data, colors):
        """Draw a spectrum analyzer visualization"""
        # Add current audio data to spectrum history
        # Roll the history array
        self.spectrum_data = np.roll(self.spectrum_data, 1, axis=0)
        self.spectrum_data[0] = audio_data
        
        # Draw the spectrum
        bar_width = self.width / len(audio_data)
        bar_height = self.height / len(self.spectrum_data)
        
        for y in range(len(self.spectrum_data)):
            for x in range(len(audio_data)):
                value = self.spectrum_data[y][x]
                
                # Calculate color intensity based on value
                intensity = int(value * 255)
                if y == 0:  # Current data line
                    color = colors[0]
                else:
                    # Fade out older lines
                    alpha = 255 - (y * (255 / len(self.spectrum_data)))
                    color = QColor(colors[1].red(), colors[1].green(), colors[1].blue(), alpha)
                
                painter.fillRect(
                    int(x * bar_width), 
                    int(self.height - (y + 1) * bar_height), 
                    int(bar_width - 1), 
                    int(bar_height - 1), 
                    color
                )
    
    def _draw_particles(self, painter, audio_data, colors):
        """Draw particle visualization"""
        avg_level = np.mean(audio_data)
        
        # Update particles
        for p in self.particles:
            # Move particles
            p['x'] += math.cos(p['angle']) * p['speed'] * (1 + avg_level * 5)
            p['y'] += math.sin(p['angle']) * p['speed'] * (1 + avg_level * 5)
            
            # Wrap around edges
            if p['x'] < 0: p['x'] = 1
            if p['x'] > 1: p['x'] = 0
            if p['y'] < 0: p['y'] = 1
            if p['y'] > 1: p['y'] = 0
            
            # Draw particle
            color = self._interpolate_color(colors[0], colors[1], p['color'])
            
            # Make size pulsate with audio
            size = p['size'] * (1 + avg_level)
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(
                QPoint(int(p['x'] * self.width), int(p['y'] * self.height)),
                int(size),
                int(size)
            )
        
        # If a beat is detected, change some particle directions
        if self.beat_detected:
            for i in range(20):
                p = random.choice(self.particles)
                p['angle'] = random.uniform(0, 2*math.pi)
    
    def _draw_equalizer(self, painter, audio_data, colors):
        """Draw an equalizer-style visualization"""
        bands = 16
        band_width = self.width / bands
        
        # Group the audio data into bands
        band_data = []
        for i in range(bands):
            start = int(i * len(audio_data) / bands)
            end = int((i + 1) * len(audio_data) / bands)
            band_data.append(np.mean(audio_data[start:end]))
        
        # Draw frequency bands
        for i, value in enumerate(band_data):
            # Scale value to height
            bar_height = value * self.height * 0.8
            x = i * band_width
            y = self.height - bar_height
            
            # Draw band
            gradient = QLinearGradient(0, self.height, 0, 0)
            gradient.setColorAt(0, colors[0])
            gradient.setColorAt(1, colors[1])
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            
            painter.drawRect(
                int(x), int(y),
                int(band_width - 2), int(bar_height)
            )
            
            # Draw frequency label
            freq = int((i + 1) * 1000 / bands) * bands
            if freq >= 1000:
                freq_text = f"{freq/1000:.1f}k"
            else:
                freq_text = f"{freq}"
                
            painter.setPen(QColor(200, 200, 200))
            painter.setFont(QFont("Arial", 8))
            painter.drawText(
                int(x + band_width/2 - 10), self.height - 5,
                freq_text
            )
    
    def _draw_waveform(self, painter, audio_data, colors):
        """Draw a waveform visualization"""
        # Generate a waveform based on audio data
        center_y = self.height / 2
        point_spacing = self.width / len(audio_data)
        
        # Create upper and lower paths
        upper_path = QPainterPath()
        lower_path = QPainterPath()
        
        upper_path.moveTo(0, center_y)
        lower_path.moveTo(0, center_y)
        
        for i, value in enumerate(audio_data):
            x = i * point_spacing
            upper_y = center_y - value * center_y * 0.8
            lower_y = center_y + value * center_y * 0.8
            
            upper_path.lineTo(x, upper_y)
            lower_path.lineTo(x, lower_y)
        
        upper_path.lineTo(self.width, center_y)
        lower_path.lineTo(self.width, center_y)
        
        # Fill paths
        painter.setPen(Qt.NoPen)
        
        # Upper gradient
        upper_gradient = QLinearGradient(0, 0, 0, center_y)
        upper_gradient.setColorAt(0, QColor(colors[0].red(), colors[0].green(), colors[0].blue(), 150))
        upper_gradient.setColorAt(1, QColor(colors[0].red(), colors[0].green(), colors[0].blue(), 50))
        
        # Lower gradient
        lower_gradient = QLinearGradient(0, center_y, 0, self.height)
        lower_gradient.setColorAt(0, QColor(colors[1].red(), colors[1].green(), colors[1].blue(), 50))
        lower_gradient.setColorAt(1, QColor(colors[1].red(), colors[1].green(), colors[1].blue(), 150))
        
        painter.setBrush(QBrush(upper_gradient))
        painter.drawPath(upper_path)
        
        painter.setBrush(QBrush(lower_gradient))
        painter.drawPath(lower_path)
        
        # Draw center line
        painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
        painter.drawLine(0, int(center_y), self.width, int(center_y))
    
    def _draw_3d_bars(self, painter, audio_data, colors):
        """Draw 3D-style bar visualization"""
        num_bars = min(16, len(audio_data))
        bar_width = self.width / (num_bars * 1.5)
        depth = bar_width * 0.3  # Perspective depth
        
        # Sort bars by position to handle overlapping correctly (back to front)
        for i in range(num_bars):
            # Calculate bar properties
            value = audio_data[i]
            bar_height = value * self.height * 0.7
            
            # Base x position (center of visualization)
            center_offset = (num_bars * bar_width) / 2
            x = self.width/2 - center_offset + i * bar_width * 1.5
            y = self.height - bar_height
            
            # Draw 3D bar (right side)
            side_color = colors[1].darker(120)
            painter.setBrush(QBrush(side_color))
            painter.setPen(Qt.NoPen)
            
            side_points = [
                QPoint(int(x + bar_width), int(y)),
                QPoint(int(x + bar_width + depth), int(y + depth)),
                QPoint(int(x + bar_width + depth), int(self.height + depth)),
                QPoint(int(x + bar_width), int(self.height))
            ]
            
            painter.drawPolygon(QPolygon(side_points))
            
            # Draw 3D bar (top side)
            top_color = colors[0].lighter(120)
            painter.setBrush(QBrush(top_color))
            
            top_points = [
                QPoint(int(x), int(y)),
                QPoint(int(x + depth), int(y + depth)),
                QPoint(int(x + bar_width + depth), int(y + depth)),
                QPoint(int(x + bar_width), int(y))
            ]
            
            painter.drawPolygon(QPolygon(top_points))
            
            # Draw front face of bar
            front_gradient = QLinearGradient(0, 0, 0, self.height)
            front_gradient.setColorAt(0, colors[0])
            front_gradient.setColorAt(1, colors[1])
            
            painter.setBrush(QBrush(front_gradient))
            painter.drawRect(int(x), int(y), int(bar_width), int(bar_height))
    
    def _draw_fireworks(self, painter, audio_data, colors):
        """Draw fireworks-style visualization"""
        # Create fireworks on beat
        if self.beat_detected and random.random() < 0.8:
            for _ in range(3):
                # Add new particles to simulate fireworks
                explosion_x = random.uniform(0.2, 0.8) * self.width
                explosion_y = random.uniform(0.2, 0.8) * self.height
                explosion_color = random.random()
                
                for _ in range(20):
                    angle = random.uniform(0, 2*math.pi)
                    self.particles.append({
                        'x': explosion_x / self.width,
                        'y': explosion_y / self.height,
                        'size': random.uniform(2, 6),
                        'speed': random.uniform(0.005, 0.015),
                        'angle': angle,
                        'color': explosion_color,
                        'life': 1.0  # Full life
                    })
        
        # Update and draw particles
        remaining_particles = []
        for p in self.particles:
            # Age particles
            if 'life' in p:
                p['life'] -= 0.01
                if p['life'] <= 0:
                    continue
                
                # Move particle
                p['x'] += math.cos(p['angle']) * p['speed']
                p['y'] += math.sin(p['angle']) * p['speed']
                p['speed'] *= 0.98  # Slow down
                
                # Draw particle with fading alpha
                color = self._interpolate_color(colors[0], colors[1], p['color'])
                alpha_color = QColor(color.red(), color.green(), color.blue(), 
                                    int(255 * p['life']))
                
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(alpha_color))
                
                size = p['size'] * p['life']
                painter.drawEllipse(
                    QPoint(int(p['x'] * self.width), int(p['y'] * self.height)),
                    int(size), int(size)
                )
                
                remaining_particles.append(p)
            else:
                # Keep regular particles
                remaining_particles.append(p)
        
        # Replace particles array with remaining particles
        self.particles = remaining_particles
        
        # Draw basic circle visualization behind fireworks
        avg_level = np.mean(audio_data)
        circle_size = avg_level * self.width / 4
        
        painter.setBrush(Qt.NoBrush)
        for i in range(5):
            size_factor = 1.0 + i * 0.4
            alpha = 255 - i * 40
            
            painter.setPen(QPen(
                QColor(colors[0].red(), colors[0].green(), colors[0].blue(), alpha),
                2
            ))
            
            painter.drawEllipse(
                QPoint(int(self.width/2), int(self.height/2)),
                int(circle_size * size_factor),
                int(circle_size * size_factor)
            )
    
    def _draw_oscilloscope(self, painter, audio_data, colors):
        """Draw oscilloscope-style visualization"""
        # Generate a sine wave modulated by audio data
        center_y = self.height / 2
        painter.setPen(QPen(colors[0], 2))
        
        path = QPainterPath()
        path.moveTo(0, center_y)
        
        num_points = 200
        for i in range(num_points):
            x = i * self.width / (num_points - 1)
            
            # Sample audio data
            idx1 = int(i * len(audio_data) / num_points)
            idx2 = int((i+1) * len(audio_data) / num_points) % len(audio_data)
            
            value1 = audio_data[idx1]
            value2 = audio_data[idx2]
            value = (value1 + value2) / 2
            
            # Modulate a sine wave with the audio data
            wave_value = math.sin(i * 0.1 + self.frame_counter * 0.05) * value
            y = center_y + wave_value * center_y * 0.8
            
            path.lineTo(x, y)
        
        # Draw main oscilloscope line
        painter.drawPath(path)
        
        # Draw grid
        painter.setPen(QPen(QColor(100, 100, 100, 100), 1))
        
        # Horizontal lines
        for i in range(5):
            y = i * self.height / 4
            painter.drawLine(0, int(y), self.width, int(y))
        
        # Vertical lines
        for i in range(11):
            x = i * self.width / 10
            painter.drawLine(int(x), 0, int(x), self.height)
        
        # Add measurement text
        painter.setPen(QColor(200, 200, 200))
        painter.setFont(QFont("Arial", 8))
        
        # Level indicators
        for i in range(5):
            y = i * self.height / 4
            level = (2 - i/2) * 100  # +100, +50, 0, -50, -100
            painter.drawText(5, int(y) + 15, f"{level:+.0f}%")
            
        # Time indicators
        time_base = 5  # ms per division
        for i in range(11):
            x = i * self.width / 10
            time_ms = i * time_base
            painter.drawText(int(x) - 10, self.height - 5, f"{time_ms}")
        
        painter.drawText(self.width - 70, 20, f"{time_base} ms/div")
        
        # Add a trigger line
        trigger_y = center_y + 0.3 * center_y
        painter.setPen(QPen(QColor(255, 165, 0), 1, Qt.DashLine))
        painter.drawLine(0, int(trigger_y), self.width, int(trigger_y))
        painter.drawText(5, int(trigger_y) - 5, "TRIG")
    
    def _create_gradient(self, colors, vertical=True):
        """Create a linear gradient from colors"""
        if vertical:
            gradient = QLinearGradient(0, 0, 0, self.height)
        else:
            gradient = QLinearGradient(0, 0, self.width, 0)
            
        gradient.setColorAt(0, colors[0])
        gradient.setColorAt(1, colors[1])
        return gradient
    
    def _interpolate_color(self, color1, color2, ratio):
        """Interpolate between two colors"""
        r = color1.red() + (color2.red() - color1.red()) * ratio
        g = color1.green() + (color2.green() - color1.green()) * ratio
        b = color1.blue() + (color2.blue() - color1.blue()) * ratio
        return QColor(int(r), int(g), int(b))