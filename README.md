# ASCII Video Player 🎬

Play any video in your terminal as ASCII art!

![Demo](examples/demo.gif)

## Features

- 🎥 **Universal Format Support** - MP4, AVI, MOV, MKV, WEBM, and more
- ⚡ **Real-time Playback** - Synchronized frame rate for smooth viewing
- 🎨 **Two Quality Modes** - Standard and detailed ASCII character sets
- 📏 **Customizable Size** - Adjust width to fit any terminal
- 🚀 **Easy Installation** - One-command setup
- 💻 **Cross-Platform** - Works on Windows, Linux, and macOS

## Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/ascii-video-player.git
cd ascii-video-player

# Install dependencies
pip install -r requirements.txt

# Run the installer (optional - makes it a system command)
python install.py
```

### Usage
```bash
# Basic playback
python ascii_player.py video.mp4

# Custom width
python ascii_player.py video.mp4 -w 150

# High quality mode
python ascii_player.py video.mp4 --detailed

# Combine options
python ascii_player.py video.mp4 -w 200 --detailed
```

### After Installation

If you ran `install.py`, you can use it from anywhere:
```bash
ascii-player video.mp4
ascii-player video.mp4 -w 200 --detailed
```

## Requirements

- Python 3.6+
- OpenCV (opencv-python)
- NumPy

## Command Line Options
