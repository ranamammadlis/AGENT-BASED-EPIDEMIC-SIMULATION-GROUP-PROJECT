"""
Build Script for SIR Epidemic Simulator
Creates a standalone executable file
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully!")

def build_executable():
    """Build the executable using PyInstaller"""
    print("\nBuilding executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window (GUI app)
        "--name=SIR_Epidemic_Simulator",  # Name of the executable
        "--icon=NONE",  # You can add an icon file here if you have one
        "--add-data=requirements.txt:.",  # Include requirements.txt
        "sir_epidemic_simulator.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*70)
        print("BUILD SUCCESSFUL!")
        print("="*70)
        print(f"\nYour executable is located at:")
        print(f"  {os.path.join(os.getcwd(), 'dist', 'SIR_Epidemic_Simulator.exe')}")
        print("\nYou can now distribute this file to run the simulator on any Windows computer")
        print("without needing Python installed!")
        print("="*70)
        
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        sys.exit(1)

def main():
    """Main build process"""
    print("="*70)
    print("SIR EPIDEMIC SIMULATOR - BUILD PROCESS")
    print("="*70)
    print("\nThis script will:")
    print("1. Install all required dependencies")
    print("2. Create a standalone executable file")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    # Install dependencies
    install_dependencies()
    
    # Build executable
    build_executable()

if __name__ == "__main__":
    main()
