# Retro MP3 Player

A nostalgic retro-style MP3 player built with PyQt5 featuring playback controls, playlist management, and customizable themes.

![Retro MP3 Player](generated-icon.png)

## Features

- **MP3 File Import**: Open MP3 files or entire folders to add to your playlist
- **Playback Controls**: Play, pause, stop, next/previous track
- **Volume Control**: Adjust volume with slider and mute toggle
- **Track Progress Bar**: Shows current playback position with seek functionality
- **Playlist Management**: Create, load, and save playlists
- **Shuffle & Repeat**: Randomize playback or loop tracks/playlists
- **Track Information Display**: See title, artist, album, and other metadata
- **Album Art Display**: View album covers when available
- **Song Duration & Time Left**: Track elapsed and remaining time
- **Equalizer Presets**: Apply genre-specific audio profiles
- **File Metadata Display**: View bitrate, sample rate, and file size
- **Multiple Themes**: Switch between light, dark, and retro themes
- **Background Playback**: Continue listening while using other applications
- **Audio Speed Control**: Adjust playback speed from 0.5x to 2.0x
- **Song Search**: Find tracks in your playlist by title or artist
- **Song Ratings**: Rate your music and filter by rating
- **Custom Hotkeys**: Keyboard shortcuts for common actions
- **Skip Timer**: Automatically move to the next song after a set time
- **Import Songs from Folder**: Bulk import all MP3 files from a directory
- **Audio Visualizer**: Visual representation of the playing audio
- **Fade In/Out Effects**: Smooth transitions between tracks
- **Command Line Controls**: Control the player via command line
- **Save and Load Settings**: Remember your preferences between sessions

## Installation

### Prerequisites

- Python 3.9 or higher
- PyQt5
- Mutagen (for metadata handling)

### Linux-specific Requirements

If you're running on Linux, you'll need the OpenGL libraries:

```
# Ubuntu/Debian
sudo apt-get install libgl1-mesa-glx

# Fedora
sudo dnf install mesa-libGL

# Arch Linux
sudo pacman -S mesa
```

These libraries are required for PyQt5 applications. Without them, you'll see the error:
`libGL.so.1: cannot open shared object file: No such file or directory`

### Option 1: Using the Installer (Recommended)

1. Download the installer package `retro-mp3-player-installer-20250510.zip`
2. Extract the ZIP file
3. Run the installer script:
   - **Windows**: Double-click `install.bat`
   - **macOS/Linux**: Open terminal and run `bash install.sh`
   
Alternatively, you can use the Python-based installer:
```
python setup.py
```

### Option 2: Manual Installation

1. Install required packages:
   ```
   pip install PyQt5 mutagen
   ```
2. Clone or download this repository
3. Navigate to the project directory
4. Run the application:
   ```
   python main.py
   ```

## Usage

### Nostalgic Boot Screen

The player features a retro-style splash screen on startup that shows loading progress with a green terminal aesthetic. You can:

- Skip the boot screen with the `--no-splash` command line option
- Choose between different retro themes with the `--theme` option:
  - `--theme green` - Classic terminal (default)
  - `--theme blue` - 80s computing blue
  - `--theme pink` - Vaporwave aesthetic

### Basic Controls

- **Play/Pause**: Space bar or middle button
- **Next Track**: Ctrl+Right or right arrow button  
- **Previous Track**: Ctrl+Left or left arrow button
- **Volume Up/Down**: Ctrl+Up/Down or volume slider
- **Mute**: Ctrl+M or speaker button
- **Add Files**: Click "Add File" or drag and drop MP3 files
- **Add Folder**: Click "Add Folder" to import all MP3s from a directory

### Command Line Usage

The player supports basic command line controls:

```
python main.py play
python main.py pause
python main.py next
python main.py previous
python main.py --file path/to/song.mp3
```

## Themes

The player includes several themes to match your style:

- Light Mode
- Dark Mode
- Retro Blue (80s style)
- Retro Green (Terminal style)
- Retro Pink (Vaporwave style)

Change themes through the Settings tab.

## Creating Playlists

1. Add songs using "Add File" or "Add Folder"
2. Arrange songs by dragging them in the playlist
3. Click "Save Playlist" and choose a name
4. Load playlists later using "Load Playlist"

## License

This project is distributed under the MIT License. See `LICENSE` file for more information.

## Acknowledgments

- Icons from Feather Icons (https://feathericons.com/)
- Built with PyQt5 and Mutagen

## Author

Created for retro music enthusiasts everywhere
