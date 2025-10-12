#!/bin/bash
# Script de inicio rápido para el proyecto ASI1.AI FastAPI

echo "🚀 Proyecto ASI1.AI FastAPI - Inicio Rápido"
echo "==========================================="

# Verificar si el entorno virtual está activado
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Entorno virtual activado: $VIRTUAL_ENV"
else
    echo "⚠️  Activando entorno virtual..."
    source .venv/bin/activate
fi

echo ""
echo "📋 Comandos disponibles:"
echo ""
echo "1. Iniciar servidor:"
echo "   python start_server.py"
echo ""
echo "2. Ejecutar pruebas:"
echo "   python test_client.py"
echo ""
echo "3. Documentación API:"
echo "   http://localhost:8000/docs"
echo ""
echo "4. Health Check:"
echo "   curl http://localhost:8000/health"
echo ""
echo "5. Chat simple:"
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