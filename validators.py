"""
Validadores de entrada y sanitización para prevenir ataques.
"""
import re
from urllib.parse import urlparse
import bleach
from typing import Optional
from config import Config
from logger import logger


class InputValidator:
    """Validación y sanitización de entradas del usuario."""
    
    @staticmethod
    def sanitize_search_query(query: str) -> Optional[str]:
        """
        Sanitiza la consulta de búsqueda del usuario.
        
        Args:
            query: Consulta del usuario
            
        Returns:
            Consulta sanitizada o None si es inválida
        """
        if not query or not isinstance(query, str):
            logger.warning("Consulta vacía o tipo inválido")
            return None
        
        # Eliminar espacios excesivos
        query = " ".join(query.split())
        
        # Longitud razonable (prevenir DoS)
        if len(query) < 2:
            logger.warning("Consulta demasiado corta")
            return None
        
        if len(query) > 200:
            logger.warning("Consulta demasiado larga, truncando")
            query = query[:200]
        
        # Eliminar caracteres peligrosos pero mantener búsqueda útil
        # Permitir: letras, números, espacios, guiones, comillas
        sanitized = re.sub(r'[^\w\s\-"\'áéíóúñÁÉÍÓÚÑ]', '', query)
        
        if not sanitized.strip():
            logger.warning("Consulta quedó vacía después de sanitización")
            return None
        
        logger.info(f"Consulta sanitizada: '{sanitized}'")
        return sanitized
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Valida que una URL sea segura para acceder.
        
        Args:
            url: URL a validar
            
        Returns:
            True si es válida y segura
        """
        try:
            parsed = urlparse(url)
            
            # Validación básica de URL
            if not all([parsed.scheme, parsed.netloc]):
                logger.warning(f"URL inválida (falta esquema o dominio): {url}")
                return False
        except Exception as e:
            logger.warning(f"Error al parsear URL {url}: {str(e)}")
            return False
        
        # Verificar esquema permitido
        if parsed.scheme not in Config.ALLOWED_SCHEMES:
            logger.warning(f"Esquema no permitido: {parsed.scheme}")
            return False
        
        # Bloquear dominios locales (prevenir SSRF)
        if any(blocked in parsed.netloc for blocked in Config.BLOCKED_DOMAINS):
            logger.warning(f"Dominio bloqueado: {parsed.netloc}")
            return False
        
        return True
    
    @staticmethod
    def sanitize_html_content(content: str) -> str:
        """
        Elimina tags HTML peligrosos del contenido extraído.
        
        Args:
            content: Contenido HTML a sanitizar
            
        Returns:
            Contenido seguro en texto plano
        """
        # Bleach elimina tags peligrosos y scripts
        clean = bleach.clean(
            content,
            tags=[],  # No permitir ningún tag HTML
            strip=True
        )
        
        return clean.strip()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitiza un nombre de archivo para prevenir path traversal.
        
        Args:
            filename: Nombre de archivo propuesto
            
        Returns:
            Nombre de archivo seguro
        """
        # Eliminar path traversal attempts
        filename = filename.replace("..", "").replace("/", "").replace("\\", "")
        
        # Solo permitir caracteres seguros
        filename = re.sub(r'[^\w\-]', '_', filename)
        
        # Limitar longitud
        if len(filename) > 100:
            filename = filename[:100]
        
        # Asegurar que no esté vacío
        if not filename:
            filename = "reporte_sin_nombre"
        
        return filename
