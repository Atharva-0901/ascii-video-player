#!/usr/bin/env python3
"""
Terminal ASCII Video Player
Plays videos in the terminal using ASCII characters
Supports: MP4, AVI, MOV, MKV, WEBM, FLV, and more
"""

import cv2
import numpy as np
import sys
import time
import os
from threading import Thread
import argparse

# ASCII characters from darkest to lightest
ASCII_CHARS = '@%#*+=-:. '
# Alternative detailed set: ASCII_CHARS = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '

class ASCIIVideoPlayer:
    def __init__(self, video_path, width=120, detailed=False):
        self.video_path = video_path
        self.width = width
        self.detailed = detailed
        
        if detailed:
            self.ascii_chars = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
        else:
            self.ascii_chars = ASCII_CHARS
        
        # Open video
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")
        
        # Get video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.original_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.original_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate height to maintain aspect ratio
        self.height = int(self.width * self.original_height / self.original_width * 0.55)
        
    def frame_to_ascii(self, frame):
        """Convert a video frame to ASCII art"""
        # Resize frame
        frame = cv2.resize(frame, (self.width, self.height))
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Map pixel values to ASCII characters
        ascii_frame = ''
        for row in gray:
            for pixel in row:
                # Map 0-255 to ASCII character index
                char_index = int(pixel / 255 * (len(self.ascii_chars) - 1))
                ascii_frame += self.ascii_chars[char_index]
            ascii_frame += '\n'
        
        return ascii_frame
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def play(self, start_frame=0):
        """Play the video"""
        try:
            # Set starting frame
            if start_frame > 0:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
            frame_delay = 1.0 / self.fps if self.fps > 0 else 0.033
            frame_num = start_frame
            
            print(f"\nPlaying: {os.path.basename(self.video_path)}")
            print(f"Resolution: {self.original_width}x{self.original_height} -> {self.width}x{self.height} (ASCII)")
            print(f"FPS: {self.fps:.2f} | Frames: {self.frame_count}")
            print(f"\nPress Ctrl+C to stop\n")
            time.sleep(2)
            
            self.clear_screen()
            
            while True:
                start_time = time.time()
                
                # Read frame
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Convert to ASCII
                ascii_frame = self.frame_to_ascii(frame)
                
                # Display
                print(f"\033[H", end='')  # Move cursor to top
                print(ascii_frame, end='')
                print(f"\nFrame: {frame_num}/{self.frame_count} | {frame_num/self.frame_count*100:.1f}%", end='')
                
                frame_num += 1
                
                # Maintain frame rate
                elapsed = time.time() - start_time
                sleep_time = frame_delay - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            print("\n\n✓ Video playback complete!")
            
        except KeyboardInterrupt:
            print("\n\n⏸ Playback stopped by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Release resources"""
        self.cap.release()


def main():
    parser = argparse.ArgumentParser(
        description='Play videos in terminal as ASCII art',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s video.mp4
  %(prog)s video.mp4 -w 150
  %(prog)s video.mp4 --detailed
  %(prog)s video.mp4 -w 100 -s 30
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
    
    # Check if file exists
    if not os.path.isfile(args.video):
        print(f"Error: File not found: {args.video}")
        sys.exit(1)
    
    # Create player and play
    try:
        player = ASCIIVideoPlayer(args.video, width=args.width, detailed=args.detailed)
        player.play(start_frame=args.start)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
