"""
Módulo mejorado de análisis con IA con seguridad y manejo robusto.
"""
import google.generativeai as genai
from typing import Optional
from config import Config
from logger import logger


class IAAnalyzer:
    """Analizador de contenido usando IA de Google con protección de API key."""
    
    def __init__(self):
        """Inicializa el analizador con la configuración segura."""
        if not Config.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY no configurada. "
                "Agrega tu clave en el archivo .env"
            )
        
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # Configurar safety settings para contenido apropiado
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        self.modelo = genai.GenerativeModel('models/gemini-2.5-flash')
        
        logger.info("Analizador IA inicializado correctamente")
    
    def resumir_texto(self, texto_extraido: str, tema: str) -> Optional[str]:
        """
        Analiza y resume el texto extraído usando IA.
        
        Args:
            texto_extraido: Texto compilado de múltiples fuentes
            tema: Tema original de investigación
            
        Returns:
            Reporte generado o None si falla
        """
        logger.info("Iniciando análisis con IA...")
        
        # Validar entrada
        if not texto_extraido or len(texto_extraido) < 100:
            logger.error("Texto insuficiente para análisis")
            return None
        
        # Limitar tamaño para evitar costos excesivos
        # Gemini Flash tiene límite de ~1M tokens, pero limitamos preventivamente
        max_chars = 50000
        if len(texto_extraido) > max_chars:
            logger.warning(f"Texto truncado de {len(texto_extraido)} a {max_chars} caracteres")
            texto_extraido = texto_extraido[:max_chars]
        
        prompt = f"""
Actúa como un investigador experto y analista profesional. Has recopilado información de múltiples fuentes web sobre el tema: "{tema}".

**Tu tarea:**
1. Analiza cuidadosamente toda la información proporcionada
2. Cruza referencias entre las distintas fuentes
3. Identifica los puntos clave y más relevantes
4. Elimina información duplicada o contradictoria
5. Redacta un reporte exhaustivo, estructurado y profesional

**Estructura del reporte:**
- Resumen ejecutivo (2-3 párrafos)
- Puntos principales (bullet points)
- Análisis detallado por secciones
- Conclusiones y hallazgos clave

**Información extraída de las fuentes:**
{texto_extraido}

**Importante:** Mantén un tono profesional, objetivo y basado en hechos.
"""
        
        try:
            # Generar contenido con configuración de seguridad
            response = self.modelo.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )
            
            # Verificar si la respuesta fue bloqueada por seguridad
            if not response.text:
                logger.error("Respuesta bloqueada por filtros de seguridad")
                return None
            
            logger.info(f"Análisis completado: {len(response.text)} caracteres generados")
            return response.text
            
        except Exception as e:
            logger.error(f"Error al procesar con IA: {str(e)}")
            return None


# Mantener compatibilidad con código antiguo
def resumir_texto(texto_extraido: str, tema: str) -> str:
    """Función legacy para compatibilidad."""
    try:
        analyzer = IAAnalyzer()
        resultado = analyzer.resumir_texto(texto_extraido, tema)
        return resultado if resultado else "[!] Error al generar el análisis con IA"
    except Exception as e:
        logger.error(f"Error al inicializar analizador: {str(e)}")
        return f"[!] Error crítico: {str(e)}"
