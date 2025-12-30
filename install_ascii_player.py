#!/usr/bin/env python3
"""
ASCII Video Player - Installation Script
Creates a standalone application you can run from anywhere
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Main application code
PLAYER_CODE = '''#!/usr/bin/env python3
"""
Terminal ASCII Video Player
Plays videos in the terminal using ASCII characters
"""

import cv2
import numpy as np
import sys
import time
import os
import argparse

ASCII_CHARS = '@%#*+=-:. '

class ASCIIVideoPlayer:
    def __init__(self, video_path, width=120, detailed=False):
        self.video_path = video_path
        self.width = width
        self.detailed = detailed
        
        if detailed:
            self.ascii_chars = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\\\|()1{}[]?-_+~<>i!lI;:,"^`\\'. '
        else:
            self.ascii_chars = ASCII_CHARS
        
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.original_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.original_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.height = int(self.width * self.original_height / self.original_width * 0.55)
        
    def frame_to_ascii(self, frame):
        frame = cv2.resize(frame, (self.width, self.height))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        ascii_frame = ''
        for row in gray:
            for pixel in row:
                char_index = int(pixel / 255 * (len(self.ascii_chars) - 1))
                ascii_frame += self.ascii_chars[char_index]
            ascii_frame += '\\n'
        
        return ascii_frame
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def play(self, start_frame=0):
        try:
            if start_frame > 0:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
            frame_delay = 1.0 / self.fps if self.fps > 0 else 0.033
            frame_num = start_frame
            
            print(f"\\nPlaying: {os.path.basename(self.video_path)}")
            print(f"Resolution: {self.original_width}x{self.original_height} -> {self.width}x{self.height} (ASCII)")
            print(f"FPS: {self.fps:.2f} | Frames: {self.frame_count}")
            print(f"\\nPress Ctrl+C to stop\\n")
            time.sleep(2)
            
            self.clear_screen()
            
            while True:
                start_time = time.time()
                
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                ascii_frame = self.frame_to_ascii(frame)
                
                print(f"\\033[H", end='')
                print(ascii_frame, end='')
                print(f"\\nFrame: {frame_num}/{self.frame_count} | {frame_num/self.frame_count*100:.1f}%", end='')
                
                frame_num += 1
                
                elapsed = time.time() - start_time
                sleep_time = frame_delay - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            print("\\n\\n[DONE] Video playback complete!")
            
        except KeyboardInterrupt:
            print("\\n\\n[STOP] Playback stopped by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        self.cap.release()


def main():
    parser = argparse.ArgumentParser(
        description='Play videos in terminal as ASCII art',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ascii-player video.mp4
  ascii-player video.mp4 -w 150
  ascii-player video.mp4 --detailed
  ascii-player video.mp4 -w 100 -s 30
        """
    )
    
    parser.add_argument('video', help='Path to video file')
    parser.add_argument('-w', '--width', type=int, default=120,
                        help='Width in characters (default: 120)')
    parser.add_argument('-d', '--detailed', action='store_true',
                        help='Use detailed ASCII character set')
    parser.add_argument('-s', '--start', type=int, default=0,
                        help='Start from frame number (default: 0)')
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.video):
        print(f"Error: File not found: {args.video}")
        sys.exit(1)
    
    try:
        player = ASCIIVideoPlayer(args.video, width=args.width, detailed=args.detailed)
        player.play(start_frame=args.start)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
'''

def print_header():
    print("=" * 60)
    print("  ASCII VIDEO PLAYER - INSTALLER")
    print("=" * 60)
    print()

def check_python():
    """Check Python version"""
    print("[*] Checking Python version...")
    if sys.version_info < (3, 6):
        print("[X] Python 3.6 or higher is required")
        sys.exit(1)
    print(f"[OK] Python {sys.version.split()[0]} detected")
    print()

def install_dependencies():
    """Install required packages"""
    print("[*] Installing dependencies...")
    try:
        # Check if opencv is already installed
        import cv2
        print("[OK] opencv-python already installed")
    except ImportError:
        print("[*] Installing opencv-python...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "numpy"])
        print("[OK] Dependencies installed successfully")
    print()

def get_install_location():
    """Determine installation location"""
    home = Path.home()
    
    if os.name == 'nt':  # Windows
        install_dir = home / "AppData" / "Local" / "ASCIIPlayer"
        bin_dir = install_dir
    else:  # Linux/Mac
        install_dir = home / ".local" / "share" / "ascii-player"
        bin_dir = home / ".local" / "bin"
    
    return install_dir, bin_dir

def create_application(install_dir, bin_dir):
    """Create the application files"""
    print(f"[*] Installing to: {install_dir}")
    
    # Create directories
    install_dir.mkdir(parents=True, exist_ok=True)
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    # Write the player script
    player_file = install_dir / "ascii_player.py"
    with open(player_file, 'w', encoding='utf-8') as f:
        f.write(PLAYER_CODE)
    
    # Make it executable (Unix-like systems)
    try:
        os.chmod(player_file, 0o755)
    except:
        pass
    
    # Create launcher script
    if os.name == 'nt':  # Windows
        launcher = bin_dir / "ascii-player.bat"
        with open(launcher, 'w') as f:
            f.write(f'@echo off\n"{sys.executable}" "{player_file}" %*\n')
    else:  # Linux/Mac
        launcher = bin_dir / "ascii-player"
        with open(launcher, 'w') as f:
            f.write(f'#!/bin/bash\n"{sys.executable}" "{player_file}" "$@"\n')
        os.chmod(launcher, 0o755)
    
    print(f"[OK] Application installed: {player_file}")
    print(f"[OK] Launcher created: {launcher}")
    print()
    
    return bin_dir

def setup_path(bin_dir):
    """Provide instructions for PATH setup"""
    print("[*] PATH SETUP")
    print("-" * 60)
    
    if os.name == 'nt':  # Windows
        print("To use 'ascii-player' from anywhere, add this to your PATH:")
        print(f"\n  {bin_dir}\n")
        print("Steps:")
        print("1. Press Win + R, type 'sysdm.cpl' and press Enter")
        print("2. Go to 'Advanced' tab -> 'Environment Variables'")
        print("3. Under 'User variables', select 'Path' -> 'Edit'")
        print("4. Click 'New' and paste the path above")
        print("5. Click OK on all windows")
        print("6. Restart your terminal")
    else:  # Linux/Mac
        shell_rc = Path.home() / ".bashrc"
        if (Path.home() / ".zshrc").exists():
            shell_rc = Path.home() / ".zshrc"
        
        path_line = f'export PATH="$HOME/.local/bin:$PATH"'
        
        # Check if already in PATH
        try:
            with open(shell_rc, 'r') as f:
                if path_line in f.read():
                    print(f"[OK] PATH already configured in {shell_rc}")
                    print()
                    return
        except FileNotFoundError:
            pass
        
        print(f"Add this line to your {shell_rc.name}:")
        print(f"\n  {path_line}\n")
        print("Or run this command:")
        print(f"\n  echo '{path_line}' >> ~/{shell_rc.name}\n")
        print("Then restart your terminal or run:")
        print(f"  source ~/{shell_rc.name}")
    
    print()

def create_desktop_entry():
    """Create desktop entry for Linux"""
    if os.name != 'nt' and sys.platform.startswith('linux'):
        desktop_dir = Path.home() / ".local" / "share" / "applications"
        desktop_dir.mkdir(parents=True, exist_ok=True)
        
        desktop_file = desktop_dir / "ascii-player.desktop"
        with open(desktop_file, 'w') as f:
            f.write(f"""[Desktop Entry]
Name=ASCII Video Player
Comment=Play videos as ASCII art in terminal
Exec=x-terminal-emulator -e ascii-player %f
Icon=video-x-generic
Terminal=true
Type=Application
Categories=AudioVideo;Video;Player;
MimeType=video/mp4;video/x-matroska;video/webm;video/avi;
""")
        
        print("[OK] Desktop entry created (right-click videos -> 'Open With')")
        print()

def print_usage():
    """Print usage instructions"""
    print("[*] USAGE")
    print("-" * 60)
    print("After restarting your terminal, use:")
    print()
    print("  ascii-player video.mp4")
    print("  ascii-player video.mp4 -w 150")
    print("  ascii-player video.mp4 --detailed")
    print()
    print("For help:")
    print("  ascii-player --help")
    print()

def main():
    print_header()
    
    try:
        check_python()
        install_dependencies()
        
        install_dir, bin_dir = get_install_location()
        create_application(install_dir, bin_dir)
        setup_path(bin_dir)
        create_desktop_entry()
        print_usage()
        
        print("=" * 60)
        print("[SUCCESS] Installation complete!")
        print("=" * 60)
        print()
        print("TIP: Restart your terminal to use 'ascii-player' command")
        print()
        
    except KeyboardInterrupt:
        print("\n\n[X] Installation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n[X] Installation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()