# Maddi's CLI UI for Moondream2 🎨👁️

A beautiful terminal-based image viewer and AI analyzer using Moondream2 vision model with **real image rendering** via Sixel graphics.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

## ✨ Features

- 🖼️ **Real Image Preview** - Sixel graphics for pixel-perfect images in terminal
- 🤖 **AI Image Analysis** - Moondream2 1.8B vision model
- ⚡ **Fast Navigation** - W/S/A/D keys for smooth browsing
- 🎯 **Interactive Q&A** - Ask questions about any image
- 💬 **Conversation Memory** - Multiple questions per image
- 🎨 **Beautiful UI** - Clean, modern terminal interface
- 🚀 **Uncensored** - Minimal filtering, detailed descriptions

## 📋 Prerequisites

### System Requirements
- **OS:** Linux (Ubuntu/Debian recommended)
- **GPU:** NVIDIA GPU with CUDA support (recommended)
- **RAM:** 8GB+ recommended
- **Python:** 3.8 or higher

### Required Tools

1. **ImageMagick** (for Sixel rendering)
```bash
sudo apt install imagemagick-6.q16
```

2. **Python 3 and pip**
```bash
sudo apt install python3 python3-pip python3-venv
```

3. **Terminal with Sixel support**
   - xterm (recommended)
   - mlterm
   - foot
   - WezTerm
   - Check support: `echo $TERM` should show `xterm-256color` or similar

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/maddi115/maddis-cli-ui-moondream2.git
cd maddis-cli-ui-moondream2
```

### 2. Create Virtual Environment
```bash
python3 -m venv moondream-env
source moondream-env/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install torch torchvision transformers pillow accelerate einops
```

### 4. Verify Sixel Support
```bash
convert ~/Pictures/test.jpg -resize 800x600 sixel:-
```
If you see an image, you're good to go! If not, you may need to use a different terminal emulator.

## 🎮 Usage

### Start the Application
```bash
cd ~/maddis-cli-ui-moondream2
source moondream-env/bin/activate
python3 run_moondream.py
```

### Navigation Controls

| Key | Action |
|-----|--------|
| `W` / `↑` | Move up one image |
| `S` / `↓` | Move down one image |
| `A` | Jump up 5 images |
| `D` | Jump down 5 images |
| `ENTER` | Analyze selected image |
| `Q` | Quit application |

### Analyzing Images

1. Navigate to your desired image using W/S/A/D
2. Press `ENTER` to open analysis mode
3. Type your question (or press Enter for default description)
4. Ask multiple questions about the same image
5. Type `back` or `b` to return to image selection

### Example Questions
- "Describe this image in detail"
- "What colors are prominent?"
- "Is this indoors or outdoors?"
- "What is the main subject?"
- "What time of day is this?"
- "Describe the person's clothing"

## 📁 File Structure
```
maddis-cli-ui-moondream2/
├── run_moondream.py          # Main application
├── moondream-env/            # Virtual environment
├── README.md                 # This file
└── .gitignore               # Git ignore rules
```

## 🔧 Configuration

### Change Image Directory
By default, images are scanned from `~/` (home directory). To change this, edit `run_moondream.py`:
```python
def find_images(directory="~"):  # Change "~" to your path
```

### Adjust Image Size
Modify the sixel resize parameters:
```python
# In show_selector function
subprocess.run(['convert', images[selected_idx], '-resize', '800x400', 'sixel:-'])
                                                            # ↑ Change these values
```

## 🐛 Troubleshooting

### Images Not Showing
**Problem:** No images appear, only text  
**Solution:** 
- Verify terminal supports Sixel: `echo $TERM`
- Install ImageMagick: `sudo apt install imagemagick-6.q16`
- Try xterm: `sudo apt install xterm` then run in xterm

### CUDA Out of Memory
**Problem:** GPU memory error  
**Solution:**
```python
# Edit run_moondream.py, change:
torch_dtype=torch.float16  # to float32 if needed
```

### Model Download Fails
**Problem:** Cannot download Moondream2 model  
**Solution:**
- Check internet connection
- Verify disk space (~4GB needed)
- Try manually: `huggingface-cli download vikhyatk/moondream2`

### Escape Sequences Appearing
**Problem:** Seeing `^[[A` or `^[[B` on screen  
**Solution:** Already fixed in latest version, pull latest changes

## 🎨 Terminal Recommendations

### Best Terminals for Sixel
1. **xterm** - Classic, reliable
```bash
   sudo apt install xterm
   xterm -e 'cd ~/maddis-cli-ui-moondream2 && source moondream-env/bin/activate && python3 run_moondream.py'
```

2. **mlterm** - Modern, fast
```bash
   sudo apt install mlterm
```

3. **foot** - Wayland-native
```bash
   sudo apt install foot
```

## 📝 Model Information

**Moondream2** - vikhyatk/moondream2
- Size: 1.8B parameters
- VRAM: ~2GB
- Quality: Excellent for its size
- Speed: Fast inference
- License: Apache 2.0

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Moondream2** by vikhyatk
- **Transformers** by Hugging Face
- **llama.cpp** community
- **ImageMagick** project

## 📧 Contact

Created by [@maddi115](https://github.com/maddi115)

---

**Enjoy analyzing images in your terminal!** 🎨👁️✨
