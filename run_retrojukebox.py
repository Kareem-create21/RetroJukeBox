#!/usr/bin/env python3
"""
RetroJukebox Quick Runner
A script to quickly run RetroJukebox without installing
"""

import os
import sys
import subprocess
import platform

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ["PyQt5", "pygame", "mutagen", "numpy"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Some required packages are missing:")
        print(", ".join(missing_packages))
        
        install = input("Do you want to install them now? (y/n): ")
        if install.lower() == 'y':
            for package in missing_packages:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("All dependencies installed.")
        else:
            print("Cannot run RetroJukebox without required dependencies.")
            sys.exit(1)

def set_platform_env():
    """Set platform-specific environment variables"""
    system = platform.system()
    
    if system == "Windows":
        os.environ["QT_QPA_PLATFORM"] = "windows"
    elif system == "Linux":
        os.environ["QT_QPA_PLATFORM"] = "xcb"
    # macOS typically doesn't need a specific platform setting

def run_application():
    """Run the main RetroJukebox application"""
    print("Starting RetroJukebox...")
    
    # Get the path to the main.py file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(current_dir, "main.py")
    
    if not os.path.exists(main_script):
        print(f"Error: Could not find {main_script}")
        sys.exit(1)
    
    try:
        # Run the main script directly
        subprocess.call([sys.executable, main_script])
    except Exception as e:
        print(f"Error running RetroJukebox: {e}")
        sys.exit(1)

def main():
    print("RetroJukebox Quick Runner")
    print("========================")
    
    check_dependencies()
    set_platform_env()
    run_application()

if __name__ == "__main__":
    main()