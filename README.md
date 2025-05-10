# RetroJukebox Installation Guide

RetroJukebox is a desktop music player with retro-styled UI themes. This document explains how to install RetroJukebox on your computer.

## Requirements

- Python 3.7 or higher
- Internet connection (for downloading dependencies)
- A supported operating system: Windows, macOS, or Linux

## Installation Methods

### Method 1: Using the Installer Script (Recommended)

The easiest way to install RetroJukebox is to use the included installer script.

1. Make sure you have Python installed on your system.
2. Download the RetroJukebox package from the release page or clone the repository.
3. Open a terminal or command prompt.
4. Navigate to the RetroJukebox directory.
5. Run the installer script:

```
python installer.py
```

The installer will:
- Check if your system meets the requirements
- Install all necessary dependencies
- Copy the application files to your home directory
- Create shortcuts on your desktop and in your applications menu
- Configure platform-specific settings

### Method 2: Manual Installation

If you prefer to install RetroJukebox manually, follow these steps:

1. Make sure you have Python 3.7 or higher installed.
2. Install the required dependencies:

```
pip install PyQt5 pygame mutagen numpy
```

3. Download the RetroJukebox package.
4. Extract the package to your desired location.
5. Run the application:

```
cd path/to/RetroJukebox
python main.py
```

## Platform-Specific Notes

### Windows

On Windows, the installer creates:
- A desktop shortcut
- A start menu entry
- A batch file for running the application with the correct environment variables

If you experience issues with the Qt platform, try running the `win_launcher.bat` file created in the installation directory.

### Linux

On Linux, the installer creates:
- A desktop shortcut
- An entry in your applications menu
- A shell script for running the application with the correct environment variables

If you experience issues with display, try running the `linux_launcher.sh` script created in the installation directory.

### macOS

On macOS, the installer creates:
- A symlink in your Applications folder
- A shell script for running the application

## Troubleshooting

If you encounter any issues during installation:

1. Check that you have the correct Python version installed:
```
python --version
```

2. Make sure you have pip installed and updated:
```
pip --version
python -m pip install --upgrade pip
```

3. Try manually installing the dependencies:
```
pip install --user PyQt5 pygame mutagen numpy
```

4. If you experience issues with audio playback, make sure your system has a working audio device.

5. For other issues, please report them in the Issues section of the project repository.

## Uninstalling

To uninstall RetroJukebox:

1. Delete the RetroJukebox folder from your home directory.
2. Remove any shortcuts created during installation.
3. Optionally, uninstall the Python dependencies if you don't use them for other projects.

## License

RetroJukebox is distributed under the MIT License. See the LICENSE file for more information.