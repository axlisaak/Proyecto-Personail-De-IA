"""
Configuración centralizada y segura de la aplicación.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Config:
    """Clase de configuración con validación y valores por defecto seguros."""
    
    # Directorios
    BASE_DIR = Path(__file__).parent
    REPORTS_DIR = BASE_DIR / "reportes_guardados"
    LOGS_DIR = BASE_DIR / "logs"
    
    # API Keys (NUNCA hardcodear aquí)
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Configuración de búsqueda
    MAX_RESULTADOS = int(os.getenv("MAX_RESULTADOS", 3))
    MAX_CARACTERES_POR_PAGINA = int(os.getenv("MAX_CARACTERES_POR_PAGINA", 3000))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", 5))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "investigador.log"
    
    # Seguridad
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    MAX_RETRIES = 3
    BACKOFF_FACTOR = 0.3
    
    # Validación de URLs permitidas (whitelist básico)
    ALLOWED_SCHEMES = ["http", "https"]
    BLOCKED_DOMAINS = ["localhost", "127.0.0.1", "0.0.0.0"]
    
    @classmethod
    def validate(cls):
        """Valida la configuración antes de iniciar la aplicación."""
        errors = []
        
        if not cls.GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY no está configurada en .env")
        
        if cls.MAX_RESULTADOS < 1 or cls.MAX_RESULTADOS > 10:
            errors.append("MAX_RESULTADOS debe estar entre 1 y 10")
        
        if errors:
            raise ValueError(f"Errores de configuración:\n" + "\n".join(f"- {e}" for e in errors))
        
        # Crear directorios necesarios
        cls.REPORTS_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
        
        return True
