#!/usr/bin/env python3
"""
Build script for creating Email Validator executable
"""

import subprocess
import sys
import os
from pathlib import Path


def build_exe():
    """Build the executable using PyInstaller"""
    print("Building Email Validator executable...")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single file executable
        "--windowed",                   # Hide console for GUI mode
        "--name=EmailValidator",        # Executable name
        "--icon=NONE",                  # No icon for now
        "--add-data", "requirements.txt:.",  # Include requirements
        "--hidden-import", "dns.resolver",   # Ensure DNS module is included
        "--hidden-import", "tkinter",        # Ensure tkinter is included
        "main.py"
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, cwd=Path.cwd(), capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Executable built successfully!")
            print("  Location: dist/EmailValidator.exe" if sys.platform == "win32" else "dist/EmailValidator")
            
            # Print file size
            exe_path = Path("dist/EmailValidator.exe" if sys.platform == "win32" else "dist/EmailValidator")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"  Size: {size_mb:.1f} MB")
        else:
            print("✗ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except FileNotFoundError:
        print("✗ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"✗ Build error: {e}")
        return False
    
    return True


def main():
    """Main build function"""
    print("Email Validator - Build Script")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("✗ main.py not found. Run this script from the project directory.")
        sys.exit(1)
    
    # Build executable
    if build_exe():
        print("\n🎉 Build completed successfully!")
        print("\nUsage:")
        print("  ./dist/EmailValidator                    # GUI mode")
        print("  ./dist/EmailValidator -e user@test.com   # Command line mode")
        print("  ./dist/EmailValidator -f emails.txt      # Bulk validation")
    else:
        print("\n❌ Build failed. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()