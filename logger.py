"""
Sistema de logging profesional y seguro.
"""
import logging
import sys
from pathlib import Path
from config import Config


class SecureLogger:
    """Logger con sanitización automática de datos sensibles."""
    
    SENSITIVE_PATTERNS = [
        'api_key', 'apikey', 'api-key',
        'password', 'passwd', 'pwd',
        'token', 'secret', 'auth'
    ]
    
    @staticmethod
    def setup_logger(name: str = "investigador") -> logging.Logger:
        """Configura el logger de la aplicación."""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Evitar duplicados
        if logger.handlers:
            return logger
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler para archivo
        try:
            file_handler = logging.FileHandler(
                Config.LOG_FILE, 
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"No se pudo configurar log en archivo: {e}")
        
        return logger
    
    @staticmethod
    def sanitize_message(message: str) -> str:
        """Elimina información sensible de los mensajes de log."""
        sanitized = message
        for pattern in SecureLogger.SENSITIVE_PATTERNS:
            if pattern in message.lower():
                # Reemplazar cualquier cosa después del patrón sensible
                sanitized = sanitized.replace(pattern, f"{pattern}=***REDACTED***")
        return sanitized


# Logger global
logger = SecureLogger.setup_logger()
