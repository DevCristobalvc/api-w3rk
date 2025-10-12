# ASI1.AI FastAPI Chat Client

Este proyecto implementa una API FastAPI para interactuar con ASI1.AI, con logs formateados y coloreados para una mejor experiencia de desarrollo.

## 🚀 Características

- **FastAPI**: API REST moderna y rápida
- **Logs con colores**: Sistema de logging con formato colorido para consola
- **Cliente de prueba**: Conversaciones hardcodeadas para testing
- **Manejo de errores**: Gestión robusta de errores con logs detallados
- **Documentación automática**: Swagger UI disponible en `/docs`

## 📁 Estructura del Proyecto

```
ethonline/
├── main.py              # Aplicación FastAPI principal
├── config.py            # Configuración de API keys y URLs  
├── logger_config.py     # Configuración de logging con colores
├── test_client.py       # Cliente de prueba con conversaciones
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Este archivo
```

## 🛠️ Instalación

1. **Clonar y activar entorno virtual** (ya configurado):
```bash
cd /Users/cristobal.valencia/Desktop/personal/ethonline
source .venv/bin/activate
```

2. **Instalar dependencias** (ya instaladas):
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Uso

### Iniciar el servidor

```bash
# Método 1: Con uvicorn directamente
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Método 2: Ejecutar el archivo principal
python main.py
```

El servidor estará disponible en: http://localhost:8000

### Documentación interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints disponibles

1. **GET /**
   - Información básica de la API

2. **GET /health**
   - Health check del servicio

3. **POST /chat**
   - Conversación completa con ASI1.AI
   - Body JSON con mensajes estructurados

4. **POST /simple-chat**
   - Chat simplificado con un mensaje directo
   - Parámetro query: `message`

### Probar con el cliente de prueba

```bash
python test_client.py
```

Este comando ejecutará conversaciones de prueba predefinidas y mostrará logs coloreados.

## 📝 Ejemplo de uso con curl

```bash
# Chat completo
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "asi1-mini",
    "messages": [
      {"role": "user", "content": "¡Hola! ¿Cómo estás?"}
    ]
  }'

# Chat simple
curl -X POST "http://localhost:8000/simple-chat?message=Hola%20ASI1"
```

## 🎨 Logs con colores

El sistema de logging incluye:
- **Verde**: Mensajes informativos
- **Amarillo**: Advertencias
- **Rojo**: Errores
- **Cyan**: Debug
- **Emojis**: Iconos descriptivos para cada tipo de operación

Ejemplo de log:
```
2024-10-11 15:30:25 | INFO     | ASI1_API | 🚀 Iniciando servidor FastAPI para ASI1.AI
2024-10-11 15:30:26 | INFO     | ASI1_API | 💬 Nueva solicitud de chat recibida
2024-10-11 15:30:27 | INFO     | ASI1_API | 🤖 ASI1 responde: ¡Hola! Me da mucho gusto saludarte...
```

## ⚙️ Configuración

Edita `config.py` para modificar:
- API Key de ASI1.AI
- URL de la API
- Puerto del servidor
- Configuración de debug

## 🧪 Conversaciones de prueba incluidas

El cliente de prueba incluye estas conversaciones hardcodeadas:
1. Saludo inicial
2. Conversación en español
3. Presentación personal (Cristóbal en stream)
4. Pregunta sobre memoria
5. Consulta técnica sobre agentes
6. Pregunta sobre integración con Python

## 🔧 Desarrollo

Para desarrollo activo:
```bash
# Servidor con auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Ver logs en tiempo real
tail -f app.log  # Si se habilita logging a archivo
```

## 📞 Soporte

Para dudas o problemas, contacta al equipo de desarrollo.