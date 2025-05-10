#!/usr/bin/env python3
"""
RetroJukebox Executable Builder
A script to build a standalone executable of RetroJukebox
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_colored(message, color):
    """Print colored messages in the terminal"""
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'blue': '\033[94m',
        'bold': '\033[1m',
        'end': '\033[0m'
    }
    print(f"{colors.get(color, '')}{message}{colors['end']}")

def check_requirements():
    """Check if PyInstaller is installed"""
    print_colored("Checking requirements...", 'blue')
    
    try:
        import PyInstaller
        print_colored("PyInstaller is already installed.", 'green')
        return True
    except ImportError:
        print_colored("PyInstaller is not installed. Installing now...", 'yellow')
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print_colored("PyInstaller installed successfully.", 'green')
            return True
        except subprocess.CalledProcessError as e:
            print_colored(f"Failed to install PyInstaller: {e}", 'red')
            return False

def build_executable():
    """Build the executable using PyInstaller"""
    print_colored("Building executable...", 'blue')
    
    script_dir = Path(__file__).resolve().parent
    main_script = script_dir / "main.py"
    
    if not main_script.exists():
        print_colored(f"Main script not found at {main_script}", 'red')
        return False
    
    build_dir = script_dir / "build"
    dist_dir = script_dir / "dist"
    
    # Clean previous builds
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # Determine icon path
    icon_path = script_dir / "generated-icon.png"
    icon_param = []
    
    if icon_path.exists():
        if platform.system() == "Windows":
            # For Windows, we need a .ico file
            try:
                from PIL import Image
                ico_path = script_dir / "retrojukebox.ico"
                Image.open(icon_path).save(ico_path)
                icon_param = ["--icon", str(ico_path)]
            except ImportError:
                print_colored("Pillow not installed. Skipping icon conversion.", 'yellow')
        else:
            icon_param = ["--icon", str(icon_path)]
    
    # List of files to include
    datas = [
        ("ui", "ui"),
    ]
    
    # Create --add-data arguments in the correct format for the current platform
    data_args = []
    separator = ";" if platform.system() == "Windows" else ":"
    for src, dst in datas:
        data_args.extend(["--add-data", f"{src}{separator}{dst}"])
    
    # Define PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=RetroJukebox",
        "--windowed",
        "--onefile",
        *icon_param,
        *data_args,
        str(main_script)
    ]
    
    # Run PyInstaller
    try:
        subprocess.check_call(cmd)
        print_colored("Executable built successfully.", 'green')
        
        # Determine the executable path
        if platform.system() == "Windows":
            exe_path = dist_dir / "RetroJukebox.exe"
        else:
            exe_path = dist_dir / "RetroJukebox"
        
        print_colored(f"Executable is available at: {exe_path}", 'blue')
        return True
    
    except subprocess.CalledProcessError as e:
        print_colored(f"Failed to build executable: {e}", 'red')
        return False

def create_distribution_package():
    """Create a zip file containing the executable and necessary files"""
    print_colored("Creating distribution package...", 'blue')
    
    script_dir = Path(__file__).resolve().parent
    dist_dir = script_dir / "dist"
    
    if not dist_dir.exists():
        print_colored("Dist directory not found. Build failed?", 'red')
        return False
    
    # Create a distribution folder
    dist_package_dir = script_dir / "RetroJukebox-dist"
    if dist_package_dir.exists():
        shutil.rmtree(dist_package_dir)
    
    dist_package_dir.mkdir()
    
    # Copy the executable
    if platform.system() == "Windows":
        src_exe = dist_dir / "RetroJukebox.exe"
        dst_exe = dist_package_dir / "RetroJukebox.exe"
    else:
        src_exe = dist_dir / "RetroJukebox"
        dst_exe = dist_package_dir / "RetroJukebox"
    
    if not src_exe.exists():
        print_colored(f"Executable not found at {src_exe}", 'red')
        return False
    
    shutil.copy2(src_exe, dst_exe)
    
    # Copy README and LICENSE files if they exist
    for file in ["README.md", "LICENSE", "INSTALL.md"]:
        src_file = script_dir / file
        if src_file.exists():
            shutil.copy2(src_file, dist_package_dir / file)
    
    # Create a zip file
    import zipfile
    zip_path = script_dir / "RetroJukebox-dist.zip"
    
    if zip_path.exists():
        os.remove(zip_path)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dist_package_dir):
            for file in files:
                file_path = Path(root) / file
                zipf.write(file_path, file_path.relative_to(dist_package_dir))
    
    print_colored(f"Distribution package created at: {zip_path}", 'green')
    return True

def main():
    """Main function"""
    print_colored("RetroJukebox Executable Builder", 'bold')
    print_colored("==============================", 'bold')
    
    if not check_requirements():
        sys.exit(1)
    
    if not build_executable():
        sys.exit(1)
    
    create_distribution_package()
    
    print_colored("\nBuild process completed.", 'bold')
    print_colored("You can distribute the RetroJukebox-dist.zip file to users.", 'bold')

if __name__ == "__main__":
    main()