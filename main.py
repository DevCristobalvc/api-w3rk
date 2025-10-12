from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from typing import List, Optional
from config import ASI_API_KEY, ASI_API_URL
from logger_config import setup_logger

# Configurar el logger
logger = setup_logger(__name__)

app = FastAPI(
    title="ASI1.AI Chat API",
    description="API para interactuar con ASI1.AI usando FastAPI",
    version="1.0.0"
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "asi1-mini"
    messages: List[Message]
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    id: str
    model: str
    choices: List[dict]
    usage: dict
    conversation_id: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Iniciando servidor FastAPI para ASI1.AI")
    logger.info("📡 API configurada para conectar con ASI1.AI")

@app.get("/")
async def root():
    logger.info("📋 Endpoint raíz accedido")
    return {
        "message": "¡Hola! API para chatear con ASI1.AI",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    logger.info("❤️ Health check realizado")
    return {"status": "healthy", "service": "asi1-chat-api"}

@app.post("/chat", response_model=dict)
async def chat_with_asi(request: ChatRequest):
    """
    Endpoint para chatear con ASI1.AI
    """
    try:
        logger.info("💬 Nueva solicitud de chat recibida")
        logger.info(f"📝 Modelo: {request.model}")
        logger.info(f"📊 Número de mensajes: {len(request.messages)}")
        
        # Log del último mensaje del usuario
        if request.messages:
            last_message = request.messages[-1]
            logger.info(f"👤 Usuario ({last_message.role}): {last_message.content[:100]}...")
        
        # Preparar los headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ASI_API_KEY}"
        }
        
        # Preparar el payload
        payload = {
            "model": request.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages]
        }
        
        if request.conversation_id:
            payload["conversation_id"] = request.conversation_id
        
        logger.info("🔄 Enviando solicitud a ASI1.AI...")
        
        # Hacer la solicitud HTTP
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                ASI_API_URL,
                headers=headers,
                json=payload
            )
            
        logger.info(f"📡 Respuesta recibida - Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Log de la respuesta del asistente
            if result.get("choices") and len(result["choices"]) > 0:
                assistant_message = result["choices"][0].get("message", {}).get("content", "")
                logger.info(f"🤖 ASI1 responde: {assistant_message[:100]}...")
            
            # Log de usage tokens si están disponibles
            if result.get("usage"):
                usage = result["usage"]
                logger.info(f"📈 Tokens utilizados - Prompt: {usage.get('prompt_tokens')}, "
                          f"Completion: {usage.get('completion_tokens')}, "
                          f"Total: {usage.get('total_tokens')}")
            
            logger.info("✅ Respuesta exitosa enviada al cliente")
            return result
            
        else:
            error_msg = f"Error de ASI1.AI API: {response.status_code}"
            logger.error(f"❌ {error_msg}")
            logger.error(f"📄 Respuesta: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=error_msg)
            
    except httpx.TimeoutException:
        error_msg = "Timeout al conectar con ASI1.AI"
        logger.error(f"⏰ {error_msg}")
        raise HTTPException(status_code=504, detail=error_msg)
        
    except httpx.RequestError as e:
        error_msg = f"Error de conexión: {str(e)}"
        logger.error(f"🔌 {error_msg}")
        raise HTTPException(status_code=503, detail=error_msg)
        
    except Exception as e:
        error_msg = f"Error interno: {str(e)}"
        logger.error(f"💥 {error_msg}", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/simple-chat")
async def simple_chat(message: str):
    """
    Endpoint simplificado para enviar un mensaje rápido
    """
    logger.info(f"💬 Chat simple - Mensaje: {message[:50]}...")
    
    chat_request = ChatRequest(
        messages=[Message(role="user", content=message)]
    )
    
    return await chat_with_asi(chat_request)

if __name__ == "__main__":
    import uvicorn
    logger.info("🎯 Iniciando servidor en modo directo...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)