import logging
import colorlog
from pythonjsonlogger import jsonlogger
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Configura un logger con formato colorido y estructura JSON para consola
    """
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar duplicar handlers si ya existen
    if logger.handlers:
        return logger
    
    # Formato para consola con colores
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        reset=True,
        style='%'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Agregar handlers al logger
    logger.addHandler(console_handler)
    
    # Configurar logging para httpx (para ver las requests)
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)  # Reducir verbosidad de httpx
    
    return logger

def setup_file_logger(name: str, filename: str = "app.log") -> logging.Logger:
    """
    Configura un logger adicional para archivos con formato JSON
    """
    
    # Crear logger para archivo
    file_logger = logging.getLogger(f"{name}_file")
    file_logger.setLevel(logging.INFO)
    
    # Formato JSON para archivo
    json_formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s",
        rename_fields={
            "asctime": "timestamp",
            "name": "logger_name", 
            "levelname": "level"
        }
    )
    
    # Handler para archivo
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(json_formatter)
    file_handler.setLevel(logging.INFO)
    
    file_logger.addHandler(file_handler)
    
    return file_logger

# Logger principal de la aplicación
app_logger = setup_logger("ASI1_API")