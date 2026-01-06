#!/bin/bash

# Setup script for Demain N'Attend Pas Multi-Agent System (Mac/Linux)

echo "================================================"
echo "  Demain N'Attend Pas - Multi-Agent Setup"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher first."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "⚠️  WARNING: ffmpeg is not installed."
    echo "The Short Video Agent requires ffmpeg to process videos."
    echo ""
    echo "To install ffmpeg:"
    echo "  - Mac: brew install ffmpeg"
    echo "  - Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo ""
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: You need to add your API keys to the .env file"
    echo ""
fi

echo ""
echo "================================================"
echo "✅ Setup complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit the .env file and add your API keys:"
echo "   - ANTHROPIC_API_KEY (get from: https://console.anthropic.com/settings/keys)"
echo "   - OPENAI_API_KEY (get from: https://platform.openai.com/api-keys)"
echo ""
echo "2. Run the application:"
echo "   ./run.sh"
echo ""
echo "Or manually:"
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
echo ""
