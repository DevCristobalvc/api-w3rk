"""
Cliente de prueba para interactuar con el API de ASI1.AI
Este archivo contiene ejemplos de conversaciones y pruebas del sistema.
"""

import httpx
import asyncio
from logger_config import setup_logger

logger = setup_logger("TEST_CLIENT")

# Datos de prueba con conversaciones hardcodeadas
CONVERSACIONES_PRUEBA = [
    {
        "titulo": "Saludo inicial",
        "mensajes": [
            {"role": "user", "content": "¡Hola! ¿Cómo puedes ayudarme hoy?"}
        ]
    },
    {
        "titulo": "Conversación en español",
        "mensajes": [
            {"role": "user", "content": "¿Puedes escribir en español?"}
        ]
    },
    {
        "titulo": "Presentación personal",
        "mensajes": [
            {"role": "user", "content": "Soy Cristóbal y estoy en stream con David Zo y Juanjo"}
        ]
    },
    {
        "titulo": "Pregunta sobre memoria",
        "mensajes": [
            {"role": "user", "content": "¿Cómo me llamo?"}
        ]
    },
    {
        "titulo": "Conversación técnica",
        "mensajes": [
            {"role": "user", "content": "¿Puedes ayudarme a crear un agente inteligente para automatizar tareas?"}
        ]
    },
    {
        "titulo": "Consulta sobre programación",
        "mensajes": [
            {"role": "user", "content": "¿Cómo puedo integrar tu API en una aplicación Python?"}
        ]
    }
]

class ASI1Client:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
    
    async def test_health(self):
        """Prueba el endpoint de health check"""
        logger.info("🔍 Probando health check...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/health")
                if response.status_code == 200:
                    logger.info("✅ Health check exitoso")
                    return response.json()
                else:
                    logger.error(f"❌ Health check falló: {response.status_code}")
                    return None
            except Exception as e:
                logger.error(f"💥 Error en health check: {e}")
                return None
    
    async def enviar_chat(self, mensajes: list, titulo: str = ""):
        """Envía una conversación al API"""
        logger.info(f"📤 Enviando chat: {titulo}")
        
        payload = {
            "model": "asi1-mini",
            "messages": mensajes
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info("✅ Respuesta recibida exitosamente")
                    
                    # Mostrar la respuesta del asistente
                    if result.get("choices") and len(result["choices"]) > 0:
                        assistant_response = result["choices"][0]["message"]["content"]
                        logger.info(f"🤖 ASI1 responde: {assistant_response}")
                    
                    return result
                else:
                    logger.error(f"❌ Error en chat: {response.status_code}")
                    logger.error(f"📄 Detalle: {response.text}")
                    return None
                    
            except Exception as e:
                logger.error(f"💥 Error enviando chat: {e}")
                return None
    
    async def chat_simple(self, mensaje: str):
        """Envía un mensaje simple usando el endpoint simplificado"""
        logger.info(f"💬 Chat simple: {mensaje[:50]}...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/simple-chat",
                    params={"message": mensaje}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info("✅ Chat simple exitoso")
                    return result
                else:
                    logger.error(f"❌ Error en chat simple: {response.status_code}")
                    return None
                    
            except Exception as e:
                logger.error(f"💥 Error en chat simple: {e}")
                return None

async def ejecutar_pruebas():
    """Ejecuta todas las pruebas del cliente"""
    logger.info("🚀 Iniciando pruebas del cliente ASI1.AI")
    logger.info("=" * 60)
    
    client = ASI1Client()
    
    # Probar health check
    await client.test_health()
    
    logger.info("=" * 60)
    logger.info("🧪 Ejecutando conversaciones de prueba...")
    
    # Ejecutar cada conversación de prueba
    for i, conv in enumerate(CONVERSACIONES_PRUEBA, 1):
        logger.info(f"\n📋 Prueba {i}/{len(CONVERSACIONES_PRUEBA)}: {conv['titulo']}")
        logger.info("-" * 40)
        
        resultado = await client.enviar_chat(conv["mensajes"], conv["titulo"])
        
        if resultado:
            logger.info(f"✅ Prueba {i} completada exitosamente")
        else:
            logger.error(f"❌ Prueba {i} falló")
        
        # Pausa entre pruebas
        await asyncio.sleep(2)
    
    logger.info("\n" + "=" * 60)
    logger.info("🏁 Pruebas completadas")

if __name__ == "__main__":
    asyncio.run(ejecutar_pruebas())