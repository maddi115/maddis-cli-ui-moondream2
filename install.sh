#!/bin/bash
set -e

echo "🎨 Installing Maddi's CLI UI for Moondream2..."
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ This installer is for Linux only"
    exit 1
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    imagemagick-6.q16 \
    git

# Create directory
INSTALL_DIR="$HOME/maddis-cli-ui-moondream2"
echo "📁 Creating directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download script
echo "⬇️  Downloading application..."
curl -O https://raw.githubusercontent.com/maddi115/maddis-cli-ui-moondream2/main/run_moondream.py

# Create virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv moondream-env
source moondream-env/bin/activate

# Install Python packages
echo "📚 Installing Python packages (this may take a few minutes)..."
pip install --upgrade pip
pip install torch torchvision transformers pillow accelerate einops

# Create launcher script
cat > "$HOME/moondream" << 'LAUNCHER'
#!/bin/bash
cd "$HOME/maddis-cli-ui-moondream2"
source moondream-env/bin/activate
python3 run_moondream.py
LAUNCHER

chmod +x "$HOME/moondream"

# Add to PATH
if ! grep -q 'export PATH="$HOME:$PATH"' "$HOME/.bashrc"; then
    echo 'export PATH="$HOME:$PATH"' >> "$HOME/.bashrc"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 To run, simply type:"
echo "   moondream"
echo ""
echo "Or run manually:"
echo "   cd $INSTALL_DIR"
echo "   source moondream-env/bin/activate"
echo "   python3 run_moondream.py"
echo ""
