#!/bin/bash

# RoomSense Flask - Quick Start Script
# This script sets up the development environment

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║      RoomSense Flask - Quick Start Setup              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Setup environment file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file with your credentials:"
    echo "   - MongoDB URI"
    echo "   - Email settings (Gmail)"
    echo "   - Base URL"
    echo ""
    read -p "Press Enter to continue after you've edited .env..."
else
    echo "✅ .env file already exists"
    echo ""
fi

# Check if .env is configured
echo "🔍 Checking configuration..."
if grep -q "your-email@gmail.com" .env; then
    echo "⚠️  Warning: .env file still contains default values!"
    echo "   Please update the following in your .env file:"
    echo "   - MAIL_USERNAME"
    echo "   - MAIL_PASSWORD"
    echo "   - MONGO_URI (if you want to use a different database)"
    echo ""
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║              Setup Complete!                           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 To start the application:"
echo "   python app.py"
echo ""
echo "📖 To run tests:"
echo "   python test_api.py"
echo ""
echo "🐳 To run with Docker:"
echo "   docker-compose up -d"
echo ""
echo "📚 For more information, see README.md"
echo ""

# Ask if user wants to start the app
read -p "Would you like to start the application now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting RoomSense Flask application..."
    echo "   Available at: http://localhost:8061"
    echo "   Press Ctrl+C to stop"
    echo ""
    python app.py
fi
