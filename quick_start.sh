#!/bin/bash

# W3RK Platform - Enhanced Quick Start Script
# ASI Alliance Hackathon 2024

echo "🚀 W3RK Platform - ASI Alliance Hackathon Quick Start"
echo "================================================="

# Check Python version
echo "🐍 Checking Python version..."
python3 --version || { echo "❌ Python 3.9+ required"; exit 1; }

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔋 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "� Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment configuration..."
    cat > .env << EOF
# ASI Alliance Configuration
ASI1_API_KEY=your_asi1_api_key_here
AGENTVERSE_API_KEY=your_agentverse_key_here

# OpenAI Configuration (for fallback AI features)  
OPENAI_API_KEY=your_openai_key_here

# Blockchain Configuration
WEB3_PROVIDER_URL=https://sepolia.infura.io/v3/your_project_id
ETHEREUM_PRIVATE_KEY=your_private_key_here

# IPFS Configuration
IPFS_API_URL=http://localhost:5001
PINATA_API_KEY=your_pinata_key
PINATA_SECRET_KEY=your_pinata_secret

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# Demo Mode
DEMO_MODE=true
EOF
    echo "📝 Created .env file - please update with your API keys"
fi

echo ""
echo "🎯 W3RK Platform Setup Complete!"
echo "================================="
echo ""
echo "🚀 To start the platform:"
echo "   python start_server.py"
echo ""
echo "📚 API Documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "🧪 Run demo:"
echo "   python demo_script.py"
echo ""
echo "🧪 Run comprehensive tests:"
echo "   python test_comprehensive.py"
echo ""
echo "🏆 Ready for ASI Alliance Hackathon!"

# Optionally start the server automatically
read -p "🚀 Start the server now? (y/N): " start_server
if [[ $start_server =~ ^[Yy]$ ]]; then
    echo "🎬 Starting W3RK Platform..."
    python start_server.py
fi
echo "   curl -X POST \"http://localhost:8000/simple-chat?message=Hola\""
echo ""
echo "6. Ver logs en tiempo real:"
echo "   tail -f server.log"
echo ""
echo "💡 Tip: La API Key de ASI1.AI está configurada en config.py"
echo "🔗 Documentos: README.md contiene toda la información"
echo ""

# Opcional: iniciar automáticamente
read -p "¿Quieres iniciar el servidor ahora? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🎯 Iniciando servidor..."
    python start_server.py
fi