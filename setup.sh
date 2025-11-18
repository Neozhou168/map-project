#!/bin/bash
# Quick setup script for macOS

echo "🔧 Setting up your Venue Geocoder app..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate it
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install packages one by one for better error handling
echo "📥 Installing Flask..."
pip install Flask

echo "📥 Installing pandas..."
pip install pandas

echo "📥 Installing other packages..."
pip install openpyxl requests Werkzeug python-dotenv

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure your .env file has your API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python app.py"
echo "4. Visit: http://localhost:5000"
echo ""
