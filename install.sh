#!/bin/bash

echo "==================================="
echo "Retro MP3 Player Installer"
echo "==================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    echo "Please install Python 3.9 or higher from https://www.python.org/downloads/"
    echo "or use your system's package manager."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"
echo

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed."
    echo "Please install pip for Python 3."
    echo "On Ubuntu/Debian: sudo apt-get install python3-pip"
    echo "On Fedora: sudo dnf install python3-pip"
    echo "On macOS: pip3 is included with Python 3 from python.org"
    exit 1
fi

# Install dependencies
echo "Installing required packages..."
pip3 install PyQt5 mutagen

# Check if PyQt5 installation succeeded
if ! python3 -c "import PyQt5" &> /dev/null; then
    echo "Warning: PyQt5 installation might have issues."
    echo "If you're on Linux, you might need additional system packages."
    echo "For Ubuntu/Debian: sudo apt-get install python3-pyqt5 libgl1-mesa-glx"
    echo "For Fedora: sudo dnf install python3-qt5 mesa-libGL"
    echo
fi

# Check specifically for libGL.so.1
if [[ "$(uname)" == "Linux" ]]; then
    echo "Checking for required OpenGL libraries..."
    if ! ldconfig -p | grep -q libGL.so.1; then
        echo "ERROR: libGL.so.1 not found. This is required for PyQt5 applications."
        echo "Installing the following packages should fix this issue:"
        echo "For Ubuntu/Debian: sudo apt-get install libgl1-mesa-glx"
        echo "For Fedora: sudo dnf install mesa-libGL"
        echo "For Arch Linux: sudo pacman -S mesa"
        echo
        echo "Please install the appropriate package for your distribution first,"
        echo "then run this installer again."
        exit 1
    else
        echo "OpenGL libraries found! Installation should work correctly."
    fi
fi

# Create run script
echo "#!/bin/bash" > run.sh
echo "python3 main.py" >> run.sh
chmod +x run.sh

echo
echo "==================================="
echo "Installation complete!"
echo
echo "To run the Retro MP3 Player, use one of the following options:"
echo "1. Execute ./run.sh"
echo "2. Run: python3 main.py"
echo "==================================="
echo

# On Linux, provide additional information about libGL
if [[ "$(uname)" == "Linux" ]]; then
    echo "Note for Linux users:"
    echo "If you encounter 'libGL.so.1: cannot open shared object file',"
    echo "please install the required package:"
    echo "- For Ubuntu/Debian: sudo apt-get install libgl1-mesa-glx"
    echo "- For Fedora: sudo dnf install mesa-libGL"
    echo "- For Arch Linux: sudo pacman -S mesa"
    echo
fi