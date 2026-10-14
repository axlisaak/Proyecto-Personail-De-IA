"""
Asistente de Investigación IA v2.0 - Mejorado y Seguro
Módulo principal con arquitectura robusta y concurrente.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import sys

from config import Config
from logger import logger
from buscador import WebSearcher
from extractor import WebExtractor
from analista import IAAnalyzer
from archivero import ReportManager


class InvestigadorIA:
    """Clase principal del sistema de investigación automatizado."""
    
    def __init__(self):
        """Inicializa todos los componentes del investigador."""
        try:
            # Validar configuración antes de iniciar
            Config.validate()
            
            self.buscador = WebSearcher()
            self.extractor = WebExtractor()
            self.analista = IAAnalyzer()
            self.archivero = ReportManager()
            
            logger.info("InvestigadorIA inicializado correctamente")
            
        except ValueError as e:
            logger.error(f"Error de configuración: {str(e)}")
            print(f"\n❌ Error de configuración:\n{str(e)}")
            print("\n💡 Asegúrate de:")
            print("  1. Copiar .env.example a .env")
            print("  2. Agregar tu GOOGLE_API_KEY en .env")
            sys.exit(1)
    
    def extraer_contenido_concurrente(
        self, 
        resultados: List[Dict[str, str]]
    ) -> List[tuple]:
        """
        Extrae contenido de múltiples URLs en paralelo.
        
        Args:
            resultados: Lista de resultados de búsqueda
            
        Returns:
            Lista de tuplas (índice, título, contenido)
        """
        contenidos = []
        
        with ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
            # Crear tareas para cada URL
            futures = {
                executor.submit(
                    self.extractor.extraer_texto, 
                    res['href']
                ): (i, res['title'])
                for i, res in enumerate(resultados, 1)
            }
            
            # Procesar resultados conforme se completan
            for future in as_completed(futures):
                idx, titulo = futures[future]
                try:
                    contenido = future.result()
                    if contenido:
                        contenidos.append((idx, titulo, contenido))
                        logger.info(f"[{idx}/{len(resultados)}] Contenido extraído: {titulo}")
                    else:
                        logger.warning(f"[{idx}/{len(resultados)}] Sin contenido: {titulo}")
                except Exception as e:
                    logger.error(f"Error al extraer {titulo}: {str(e)}")
        
        return contenidos
    
    def iniciar_investigacion(self, tema: str = None):
        """
        Ejecuta el proceso completo de investigación.
        
        Args:
            tema: Tema a investigar (si es None, solicita al usuario)
        """
        print("\n" + "="*60)
        print("    🔍 Asistente de Investigación IA v2.0")
        print("    🔒 Versión Segura y Profesional")
        print("="*60)
        
        # Solicitar tema si no se proporciona
        if not tema:
            tema = input("\n¿Sobre qué te gustaría investigar hoy?: ").strip()
        
        if not tema:
            print("❌ Debes proporcionar un tema de investigación")
            return
        
        print("\n" + "-"*60)
        logger.info(f"Iniciando investigación sobre: '{tema}'")
        
        # 1. Búsqueda en internet
        print(f"\n🔎 Buscando información sobre: '{tema}'...")
        resultados = self.buscador.buscar_en_internet(tema)
        
        if not resultados:
            print("❌ No se encontraron resultados. Intenta con otro tema.")
            logger.warning("Búsqueda sin resultados")
            return
        
        print(f"✅ Se encontraron {len(resultados)} fuentes")
        
        # 2. Extracción de contenido (paralelo)
        print(f"\n📥 Extrayendo contenido de {len(resultados)} fuentes...")
        contenidos = self.extraer_contenido_concurrente(resultados)
        
        if not contenidos:
            print("❌ No se pudo extraer contenido de ninguna fuente")
            logger.error("Extracción fallida para todas las fuentes")
            return
        
        print(f"✅ Contenido extraído de {len(contenidos)} fuentes")
        
        # 3. Combinar contenido
        texto_combinado = ""
        for idx, titulo, contenido in contenidos:
            texto_combinado += f"\n\n{'='*50}\n"
            texto_combinado += f"FUENTE {idx}: {titulo}\n"
            texto_combinado += f"{'='*50}\n{contenido}"
        
        # 4. Análisis con IA
        print("\n🤖 Analizando información con IA...")
        reporte_final = self.analista.resumir_texto(texto_combinado, tema)
        
        if not reporte_final:
            print("❌ Error al generar el análisis con IA")
            logger.error("Análisis IA falló")
            return
        
        # 5. Mostrar resultado
        print("\n" + "="*60)
        print("    📊 REPORTE DE INVESTIGACIÓN")
        print("="*60)
        print(reporte_final)
        print("="*60 + "\n")
        
        # 6. Guardar reporte
        metadata = {
            "fuentes_consultadas": len(resultados),
            "fuentes_exitosas": len(contenidos),
            "urls": [r['href'] for r in resultados]
        }
        
        ruta_guardado = self.archivero.guardar_reporte(
            tema, 
            reporte_final,
            metadata
        )
        
        if ruta_guardado:
            print(f"💾 Reporte guardado en: {ruta_guardado}\n")
        
        logger.info("Investigación completada exitosamente")


def main():
    """Punto de entrada principal de la aplicación."""
    try:
        investigador = InvestigadorIA()
        investigador.iniciar_investigacion()
    except KeyboardInterrupt:
        print("\n\n⚠️  Investigación cancelada por el usuario")
        logger.info("Programa interrumpido por el usuario")
    except Exception as e:
        logger.critical(f"Error crítico no manejado: {str(e)}", exc_info=True)
        print(f"\n❌ Error crítico: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
