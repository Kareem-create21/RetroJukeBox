#!/usr/bin/env python3
"""
RetroJukebox Installer
A script to install RetroJukebox music player and its dependencies
"""

import os
import sys
import platform
import subprocess
import shutil
import zipfile
import time
from pathlib import Path
import urllib.request

# Set up colors for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """Print an attractive header for the installer"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}======================================{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}       RetroJukebox Installer       {Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}======================================{Colors.END}\n")
    
def print_step(step, message):
    """Print a numbered step with message"""
    print(f"{Colors.BOLD}{Colors.GREEN}[{step}] {message}{Colors.END}")
    
def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.YELLOW}WARNING: {message}{Colors.END}")
    
def print_error(message):
    """Print an error message"""
    print(f"{Colors.RED}ERROR: {message}{Colors.END}")
    
def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}{message}{Colors.END}")

def check_python_version():
    """Check if Python version is compatible"""
    required_version = (3, 7)
    current_version = sys.version_info
    
    if current_version < required_version:
        print_error(f"Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"You have Python {current_version[0]}.{current_version[1]}.{current_version[2]}")
        return False
    return True

def install_dependencies(custom_selection=False):
    """Install required Python packages"""
    requirements = {
        "PyQt5": "UI framework for the application",
        "pygame": "Audio playback and visualization",
        "mutagen": "Audio metadata extraction (MP3, FLAC, WAV, OGG)",
        "numpy": "Numerical processing for audio visualization"
    }
    
    selected_packages = []
    
    if custom_selection:
        print("\nSelect dependencies to install:")
        for package, description in requirements.items():
            while True:
                response = input(f"Install {package} ({description})? (y/n): ").strip().lower()
                if response in ['y', 'n']:
                    if response == 'y':
                        selected_packages.append(package)
                    break
                else:
                    print(f"{Colors.YELLOW}Please enter 'y' or 'n'.{Colors.END}")
    else:
        # Install all dependencies
        selected_packages = list(requirements.keys())
    
    if not selected_packages:
        print_warning("No dependencies selected for installation.")
        return True
    
    try:
        for package in selected_packages:
            print(f"    Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
        
        print_success("All selected dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False

def create_installation_directory():
    """Create installation directory in user's home folder"""
    
    home_dir = Path.home()
    install_dir = home_dir / "RetroJukebox"
    
    try:
        if not install_dir.exists():
            install_dir.mkdir(parents=True)
            print_success(f"Created installation directory at {install_dir}")
        else:
            print_warning(f"Installation directory already exists at {install_dir}")
            
            # Ask user if they want to overwrite existing installation
            response = input("Do you want to overwrite the existing installation? (y/n): ").strip().lower()
            if response != 'y':
                print("Installation aborted.")
                return None
                
            # Backup existing installation before overwriting
            backup_dir = home_dir / "RetroJukebox_backup"
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
                
            shutil.copytree(install_dir, backup_dir)
            print_success(f"Existing installation backed up to {backup_dir}")
            
        return install_dir
    
    except Exception as e:
        print_error(f"Failed to create installation directory: {e}")
        return None

def copy_files(install_dir):
    """Copy application files to installation directory"""
    print_step(4, "Copying application files...")
    
    script_dir = Path(__file__).resolve().parent
    
    # These are the files and directories that need to be copied
    required_items = [
        "main.py", "player.py", "file_manager.py", "metadata.py", 
        "playlist.py", "visualizer.py", "themes.py", "loading_screen.py", "ui"
    ]
    
    try:
        for item in required_items:
            src_path = script_dir / item
            dest_path = install_dir / item
            
            if src_path.is_file():
                shutil.copy2(src_path, dest_path)
                print(f"    Copied {item}")
            elif src_path.is_dir():
                # Remove the directory if it exists to avoid permission issues
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                    
                shutil.copytree(src_path, dest_path)
                print(f"    Copied directory {item}")
            else:
                print_warning(f"Required item {item} not found")
        
        print_success("All application files copied successfully.")
        return True
    
    except Exception as e:
        print_error(f"Failed to copy application files: {e}")
        return False

def create_shortcuts(install_dir):
    """Create desktop and start menu shortcuts"""
    print_step(5, "Creating shortcuts...")
    
    system = platform.system()
    
    try:
        if system == "Windows":
            create_windows_shortcuts(install_dir)
        elif system == "Linux":
            create_linux_shortcuts(install_dir)
        elif system == "Darwin":  # macOS
            create_macos_shortcuts(install_dir)
        else:
            print_warning(f"Unsupported platform: {system}. Skipping shortcut creation.")
            return False
            
        print_success("Shortcuts created successfully.")
        return True
    
    except Exception as e:
        print_error(f"Failed to create shortcuts: {e}")
        return False

def create_windows_shortcuts(install_dir):
    """Create Windows shortcuts"""
    try:
        # Try to use the win32com library if available
        import win32com.client
        
        shell = win32com.client.Dispatch("WScript.Shell")
        
        # Desktop shortcut
        desktop = Path(shell.SpecialFolders("Desktop"))
        shortcut_path = desktop / "RetroJukebox.lnk"
        
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = sys.executable
        shortcut.Arguments = str(install_dir / "main.py")
        shortcut.WorkingDirectory = str(install_dir)
        shortcut.IconLocation = str(install_dir / "generated-icon.png")
        shortcut.save()
        
        # Start menu shortcut
        start_menu = Path(shell.SpecialFolders("StartMenu")) / "Programs" / "RetroJukebox"
        if not start_menu.exists():
            start_menu.mkdir(parents=True, exist_ok=True)
            
        shortcut_path = start_menu / "RetroJukebox.lnk"
        
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = sys.executable
        shortcut.Arguments = str(install_dir / "main.py")
        shortcut.WorkingDirectory = str(install_dir)
        shortcut.IconLocation = str(install_dir / "generated-icon.png")
        shortcut.save()
        
    except ImportError:
        # Fall back to using a batch file
        print_warning("Could not create Windows shortcuts. Creating batch file instead.")
        
        batch_path = install_dir / "RetroJukebox.bat"
        with open(batch_path, 'w') as f:
            f.write(f'@echo off\n"{sys.executable}" "{install_dir / "main.py"}"\n')
            
        print_success(f"Created batch file at {batch_path}")

def create_linux_shortcuts(install_dir):
    """Create Linux shortcuts"""
    # Desktop shortcut
    desktop_dir = Path.home() / "Desktop"
    if not desktop_dir.exists():
        desktop_dir.mkdir(parents=True, exist_ok=True)
        
    desktop_file_path = desktop_dir / "retrojukebox.desktop"
    
    # Also create in applications directory for the start menu
    applications_dir = Path.home() / ".local" / "share" / "applications"
    if not applications_dir.exists():
        applications_dir.mkdir(parents=True, exist_ok=True)
        
    app_file_path = applications_dir / "retrojukebox.desktop"
    
    desktop_entry = (
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=RetroJukebox\n"
        "Comment=Retro-styled music player\n"
        f"Exec={sys.executable} {install_dir / 'main.py'}\n"
        f"Path={install_dir}\n"
        f"Icon={install_dir / 'generated-icon.png'}\n"
        "Terminal=false\n"
        "Categories=Audio;Music;Player;AudioVideo;\n"
    )
    
    with open(desktop_file_path, 'w') as f:
        f.write(desktop_entry)
        
    with open(app_file_path, 'w') as f:
        f.write(desktop_entry)
        
    # Make the .desktop files executable
    os.chmod(desktop_file_path, 0o755)
    os.chmod(app_file_path, 0o755)

def create_macos_shortcuts(install_dir):
    """Create macOS shortcuts"""
    # Create an AppleScript file that launches the application
    applications_dir = Path.home() / "Applications"
    if not applications_dir.exists():
        applications_dir.mkdir(parents=True, exist_ok=True)
        
    app_script_path = install_dir / "RetroJukebox.scpt"
    
    applescript = (
        'tell application "Terminal"\n'
        f'    do script "cd {install_dir} && {sys.executable} main.py"\n'
        '    activate\n'
        'end tell\n'
    )
    
    with open(app_script_path, 'w') as f:
        f.write(applescript)
        
    # Create a symbolic link in the Applications folder
    app_link_path = applications_dir / "RetroJukebox"
    
    if app_link_path.exists():
        os.remove(app_link_path)
        
    os.symlink(app_script_path, app_link_path)

def configure_platform_specific_settings(install_dir):
    """Configure platform-specific settings"""
    print_step(6, "Configuring platform-specific settings...")
    
    system = platform.system()
    
    try:
        if system == "Windows":
            # Create a batch file that sets QT_QPA_PLATFORM=windows
            env_setup_path = install_dir / "win_launcher.bat"
            with open(env_setup_path, 'w') as f:
                f.write('@echo off\n')
                f.write('set QT_QPA_PLATFORM=windows\n')
                f.write(f'"{sys.executable}" "{install_dir / "main.py"}"\n')
                
            print_success(f"Created Windows environment setup at {env_setup_path}")
            
        elif system == "Linux":
            # Some Linux systems need XCB
            env_setup_path = install_dir / "linux_launcher.sh"
            with open(env_setup_path, 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('export QT_QPA_PLATFORM=xcb\n')
                f.write(f'"{sys.executable}" "{install_dir / "main.py"}"\n')
                
            os.chmod(env_setup_path, 0o755)
            print_success(f"Created Linux environment setup at {env_setup_path}")
            
        elif system == "Darwin":  # macOS
            # macOS might need specific settings too
            env_setup_path = install_dir / "mac_launcher.sh"
            with open(env_setup_path, 'w') as f:
                f.write('#!/bin/bash\n')
                f.write(f'"{sys.executable}" "{install_dir / "main.py"}"\n')
                
            os.chmod(env_setup_path, 0o755)
            print_success(f"Created macOS environment setup at {env_setup_path}")
            
        else:
            print_warning(f"Unsupported platform: {system}. Skipping platform-specific configuration.")
            return False
            
        return True
    
    except Exception as e:
        print_error(f"Failed to configure platform-specific settings: {e}")
        return False

def get_installation_choice():
    """Ask user for installation options"""
    print("\n" + "-" * 50)
    print(f"{Colors.BOLD}Installation Options:{Colors.END}")
    print("1. Full installation - " + Colors.GREEN + "Recommended" + Colors.END)
    print("   • Install Python packages (PyQt5, pygame, mutagen for audio format support)")
    print("   • Copy all application files including new loading screen")
    print("   • Create desktop shortcuts")
    print("   • Configure platform-specific settings")
    print("2. Install dependencies only")
    print("   • Only install required Python packages")
    print("   • No file copying or shortcuts created")
    print("3. Install application files only")
    print("   • Copy application files including new loading screen")
    print("   • Create shortcuts")
    print("   • Assumes dependencies are already installed")
    print("4. Custom installation")
    print("   • Select specific components to install")
    print("-" * 50)
    
    while True:
        try:
            choice = int(input("\nSelect an option (1-4): "))
            if 1 <= choice <= 4:
                return choice
            else:
                print(f"{Colors.YELLOW}Please enter a number between 1 and 4.{Colors.END}")
        except ValueError:
            print(f"{Colors.YELLOW}Please enter a valid number.{Colors.END}")

def custom_installation():
    """Let user choose specific components to install"""
    options = {
        "dependencies": "Install dependencies (PyQt5, pygame, mutagen for MP3/FLAC/WAV/OGG support, numpy)",
        "files": "Copy application files (including new loading screen with retro boot animation)",
        "shortcuts": "Create desktop/start menu shortcuts (for easy access)",
        "platform_settings": "Configure platform-specific settings (file associations, permissions)"
    }
    
    selections = {}
    
    print("\n" + "-" * 50)
    print(f"{Colors.BOLD}Custom Installation - Select Components:{Colors.END}")
    
    for key, description in options.items():
        while True:
            response = input(f"Install {description}? (y/n): ").strip().lower()
            if response in ['y', 'n']:
                selections[key] = (response == 'y')
                break
            else:
                print(f"{Colors.YELLOW}Please enter 'y' or 'n'.{Colors.END}")
    
    return selections

def main():
    """Main installer function"""
    print_header()
    
    print_step(1, "Checking system compatibility...")
    if not check_python_version():
        sys.exit(1)
    
    # Initialize variables to avoid "possibly unbound" errors
    install_dir = None
    selections = {
        "dependencies": False,
        "files": False,
        "shortcuts": False,
        "platform_settings": False
    }
    
    # Get installation option
    option = get_installation_choice()
    
    # Set default selections based on option
    if option == 1:  # Full installation
        selections = {
            "dependencies": True,
            "files": True,
            "shortcuts": True,
            "platform_settings": True
        }
    elif option == 2:  # Dependencies only
        selections = {
            "dependencies": True,
            "files": False,
            "shortcuts": False,
            "platform_settings": False
        }
    elif option == 3:  # Application files only
        selections = {
            "dependencies": False,
            "files": True,
            "shortcuts": True,
            "platform_settings": True
        }
    elif option == 4:  # Custom installation
        selections = custom_installation()
    
    # Track the step number
    step_num = 2
    
    # Install dependencies if selected
    if selections["dependencies"]:
        print_step(step_num, "Installing dependencies...")
        # If custom installation, let user select specific dependencies
        if option == 4:  # Custom installation
            if not install_dependencies(custom_selection=True):
                sys.exit(1)
        else:
            if not install_dependencies(custom_selection=False):
                sys.exit(1)
        step_num += 1
    
    # Install files if selected
    if selections["files"]:
        print_step(step_num, "Creating installation directory...")
        install_dir = create_installation_directory()
        if not install_dir:
            sys.exit(1)
        step_num += 1
        
        print_step(step_num, "Copying application files...")
        if not copy_files(install_dir):
            sys.exit(1)
        step_num += 1
        
        # Create shortcuts if selected
        if selections["shortcuts"]:
            print_step(step_num, "Creating shortcuts...")
            create_shortcuts(install_dir)
            step_num += 1
        
        # Configure platform settings if selected
        if selections["platform_settings"]:
            print_step(step_num, "Configuring platform-specific settings...")
            configure_platform_specific_settings(install_dir)
            step_num += 1
    
    # Final message
    print("\n" + "-" * 50)
    print(f"{Colors.BOLD}{Colors.GREEN}RetroJukebox installation completed!{Colors.END}")
    
    if selections["files"]:
        # Install dir will be defined if files are installed
        print(f"Installation location: {install_dir}")
        print(f"To run the application, use the desktop shortcut or navigate to")
        print(f"the installation directory and run: python main.py")
        print(f"\n{Colors.YELLOW}New Features:{Colors.END}")
        print(f"• Retro boot animation loading screen (for systems with good resources)")
        print(f"• Simple loading screen fallback (for systems with limited resources)")
        print(f"• Support for multiple audio formats: MP3, FLAC, WAV, OGG")
        print(f"• Run with --simple flag for the simplified loading screen: python main.py --simple")
    elif selections["dependencies"]:
        print("Dependencies have been installed. You can now run RetroJukebox directly from its source directory.")
        print(f"\n{Colors.YELLOW}Note:{Colors.END} This installation includes support for MP3, FLAC, WAV, and OGG audio formats.")
    else:
        print("Custom installation completed with selected components.")
    
    print("-" * 50 + "\n")

if __name__ == "__main__":
    main()