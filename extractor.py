"""
Módulo mejorado de extracción de contenido web con seguridad y robustez.
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional
from config import Config
from logger import logger
from validators import InputValidator


class WebExtractor:
    """Extractor de contenido web con manejo robusto de errores y seguridad."""
    
    def __init__(self):
        """Inicializa el extractor con configuración de reintentos."""
        self.session = self._create_session()
        self.validator = InputValidator()
    
    def _create_session(self) -> requests.Session:
        """Crea una sesión HTTP con reintentos automáticos."""
        session = requests.Session()
        
        # Configurar estrategia de reintentos
        retry_strategy = Retry(
            total=Config.MAX_RETRIES,
            backoff_factor=Config.BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def extraer_texto(self, url: str) -> Optional[str]:
        """
        Extrae texto de una página web de forma segura.
        
        Args:
            url: URL de la página a extraer
            
        Returns:
            Texto extraído o None si falla
        """
        # Validar URL antes de hacer la petición
        if not self.validator.validate_url(url):
            logger.error(f"URL rechazada por validación: {url}")
            return None
        
        logger.info(f"Extrayendo contenido de: {url}")
        
        try:
            headers = {'User-Agent': Config.USER_AGENT}
            
            # Petición con timeout
            response = self.session.get(
                url, 
                headers=headers, 
                timeout=Config.REQUEST_TIMEOUT,
                allow_redirects=True
            )
            
            response.raise_for_status()  # Lanzar excepción si status != 2xx
            
            # Verificar tipo de contenido
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                logger.warning(f"Tipo de contenido no HTML: {content_type}")
                return None
            
            # Parsear HTML (usando html.parser, no requiere dependencias externas)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Eliminar scripts y estilos
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            
            # Extraer párrafos
            paragraphs = soup.find_all('p')
            texto = " ".join([p.get_text(strip=True) for p in paragraphs])
            
            if not texto:
                # Intentar con todo el body si no hay párrafos
                body = soup.find('body')
                texto = body.get_text(separator=' ', strip=True) if body else ""
            
            # Sanitizar contenido
            texto_limpio = self.validator.sanitize_html_content(texto)
            
            # Limitar tamaño
            if len(texto_limpio) > Config.MAX_CARACTERES_POR_PAGINA:
                texto_limpio = texto_limpio[:Config.MAX_CARACTERES_POR_PAGINA]
            
            logger.info(f"Extraídos {len(texto_limpio)} caracteres de {url}")
            return texto_limpio
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout al acceder a {url}")
        except requests.exceptions.TooManyRedirects:
            logger.error(f"Demasiadas redirecciones en {url}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error HTTP {e.response.status_code} en {url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de red al acceder a {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Error inesperado al extraer {url}: {str(e)}")
        
        return None


# Mantener compatibilidad con código antiguo
def extraer_texto(url: str) -> str:
    """Función legacy para compatibilidad."""
    extractor = WebExtractor()
    resultado = extractor.extraer_texto(url)
    return resultado if resultado else f"[!] Error al extraer contenido de {url}"
