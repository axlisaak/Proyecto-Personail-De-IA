"""
Módulo mejorado de búsqueda web con rate limiting y manejo de errores.
"""
from ddgs import DDGS
from ratelimit import limits, sleep_and_retry
from typing import List, Dict
from config import Config
from logger import logger
from validators import InputValidator


class WebSearcher:
    """Buscador web con protección contra rate limiting y validación."""
    
    def __init__(self):
        """Inicializa el buscador."""
        self.validator = InputValidator()
    
    @sleep_and_retry
    @limits(calls=10, period=60)  # Máximo 10 búsquedas por minuto
    def buscar_en_internet(
        self, 
        tema: str, 
        max_resultados: int = None
    ) -> List[Dict[str, str]]:
        """
        Busca información en internet de forma segura y controlada.
        
        Args:
            tema: Tema a buscar
            max_resultados: Número máximo de resultados (usa Config si es None)
            
        Returns:
            Lista de resultados con título, URL y snippet
        """
        # Sanitizar entrada
        tema_limpio = self.validator.sanitize_search_query(tema)
        if not tema_limpio:
            logger.error("Consulta de búsqueda inválida")
            return []
        
        if max_resultados is None:
            max_resultados = Config.MAX_RESULTADOS
        
        # Limitar resultados a un máximo razonable
        max_resultados = min(max_resultados, 10)
        
        logger.info(f"Buscando: '{tema_limpio}' (máx. {max_resultados} resultados)")
        
        resultados = []
        
        try:
            with DDGS() as ddgs:
                search_results = ddgs.text(
                    tema_limpio, 
                    max_results=max_resultados
                )
                
                for result in search_results:
                    # Validar cada URL antes de agregarla
                    url = result.get('href', '')
                    
                    if self.validator.validate_url(url):
                        resultados.append({
                            'title': result.get('title', 'Sin título'),
                            'href': url,
                            'snippet': result.get('body', '')
                        })
                    else:
                        logger.warning(f"URL rechazada: {url}")
                
            logger.info(f"Se encontraron {len(resultados)} resultados válidos")
            
        except Exception as e:
            logger.error(f"Error durante la búsqueda: {str(e)}")
        
        return resultados


# Mantener compatibilidad con código antiguo
def buscar_en_internet(tema: str, max_resultados: int = 3) -> List[Dict[str, str]]:
    """Función legacy para compatibilidad."""
    searcher = WebSearcher()
    return searcher.buscar_en_internet(tema, max_resultados)
