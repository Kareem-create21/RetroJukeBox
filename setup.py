#!/usr/bin/env python3

import subprocess
import sys
import os
import platform
from pathlib import Path

HEADER = "\033[95m"
BLUE = "\033[94m"
GREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"

def print_header(text):
    print(f"{HEADER}{BOLD}{text}{ENDC}")

def print_success(text):
    print(f"{GREEN}{text}{ENDC}")

def print_warning(text):
    print(f"{WARNING}{text}{ENDC}")

def print_error(text):
    print(f"{FAIL}{text}{ENDC}")

def print_info(text):
    print(f"{BLUE}{text}{ENDC}")

def check_python_version():
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print_warning(f"Python {version.major}.{version.minor} detected.")
        print_warning("Retro MP3 Player works best with Python 3.9 or higher.")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected.")
    return True

def check_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def install_packages():
    print_info("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "mutagen"])
        print_success("Successfully installed packages.")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install packages.")
        return False

def create_run_script():
    system = platform.system()
    if system == "Windows":
        with open("run.bat", "w") as f:
            f.write("@echo off\n")
            f.write(f'"{sys.executable}" main.py\n')
        print_info("Created run.bat for Windows")
    else:
        with open("run.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f'"{sys.executable}" main.py\n')
        os.chmod("run.sh", 0o755)
        print_info("Created run.sh for Unix systems")

def handle_linux_specific():
    try:
        # Check if libGL is available
        result = subprocess.check_output(["ldconfig", "-p"]).decode('utf-8')
        if "libGL.so.1" not in result:
            print_error("libGL.so.1 not found. This library is required for PyQt5 applications.")
            print_warning("You need to install the OpenGL libraries for your Linux distribution:")
            print("  - For Ubuntu/Debian: sudo apt-get install libgl1-mesa-glx")
            print("  - For Fedora: sudo dnf install mesa-libGL")
            print("  - For Arch Linux: sudo pacman -S mesa")
            print()
            print_warning("Please install the appropriate package and run this setup again.")
            return False
        else:
            print_success("OpenGL libraries found! Installation should work correctly.")
            return True
    except:
        print_warning("Unable to check for libGL.so.1. If you encounter OpenGL errors when running the application, try installing the required packages:")
        print("  - For Ubuntu/Debian: sudo apt-get install libgl1-mesa-glx")
        print("  - For Fedora: sudo dnf install mesa-libGL")
        print("  - For Arch Linux: sudo pacman -S mesa")
        print()
        return True

def main():
    print_header("====================================")
    print_header("  Retro MP3 Player Setup")
    print_header("====================================")
    print()
    
    # Check Python version
    if not check_python_version():
        choice = input("Continue anyway? [y/N]: ").lower()
        if choice != 'y':
            print_info("Setup cancelled.")
            return
    
    # Check pip
    if not check_pip():
        print_error("pip is not available. Please install pip to continue.")
        return
    
    # Install packages
    if not install_packages():
        print_warning("There were errors installing packages. You may need to install them manually.")
        print("Run: pip install PyQt5 mutagen")
    
    # Platform-specific instructions
    system = platform.system()
    if system == "Linux":
        linux_check_passed = handle_linux_specific()
        if not linux_check_passed:
            print_warning("Setup halted due to missing required libraries.")
            return
    
    # Create run script
    create_run_script()
    
    print()
    print_header("====================================")
    print_success("Installation complete!")
    print()
    print_info("To run the Retro MP3 Player:")
    if system == "Windows":
        print("  - Double-click run.bat")
        print("  - Or run: python main.py")
    else:
        print("  - Run: ./run.sh")
        print("  - Or run: python main.py")
    print_header("====================================")

if __name__ == "__main__":
    main()