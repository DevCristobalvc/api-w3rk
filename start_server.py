#!/usr/bin/env python3
"""
Script de inicio para el servidor FastAPI ASI1.AI
Uso: python start_server.py
"""

import uvicorn
import sys
from logger_config import setup_logger

# Configurar logger para el script de inicio
logger = setup_logger("START_SERVER")

def main():
    logger.info("🎯 Iniciando servidor ASI1.AI FastAPI...")
    logger.info("📡 Configuración:")
    logger.info("   - Host: 0.0.0.0")
    logger.info("   - Puerto: 8000")  
    logger.info("   - Reload: Activado")
    logger.info("   - Docs: http://localhost:8000/docs")
    logger.info("")
    logger.info("🛑 Para detener el servidor: Ctrl+C")
    logger.info("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("🛑 Servidor detenido por el usuario")
    except Exception as e:
        logger.error(f"💥 Error iniciando servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()