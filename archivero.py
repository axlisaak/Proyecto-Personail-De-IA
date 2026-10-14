"""
Módulo mejorado de gestión de archivos con seguridad y metadatos.
"""
import os
from pathlib import Path
from datetime import datetime
import json
from typing import Optional
from config import Config
from logger import logger
from validators import InputValidator


class ReportManager:
    """Gestor de reportes con validación y metadatos."""
    
    def __init__(self):
        """Inicializa el gestor de reportes."""
        self.reports_dir = Config.REPORTS_DIR
        self.validator = InputValidator()
        
        # Asegurar que el directorio existe
        self.reports_dir.mkdir(exist_ok=True)
        
        logger.info(f"ReportManager inicializado: {self.reports_dir}")
    
    def guardar_reporte(
        self, 
        tema: str, 
        contenido_reporte: str,
        metadata: Optional[dict] = None
    ) -> Optional[Path]:
        """
        Guarda un reporte con validación y metadatos.
        
        Args:
            tema: Tema de la investigación
            contenido_reporte: Contenido del reporte generado
            metadata: Metadatos adicionales (opcional)
            
        Returns:
            Path del archivo guardado o None si falla
        """
        logger.info("Preparando reporte para guardar...")
        
        # Validar contenido
        if not contenido_reporte or len(contenido_reporte) < 50:
            logger.error("Contenido de reporte insuficiente")
            return None
        
        # Sanitizar nombre de archivo
        nombre_base = self.validator.sanitize_filename(tema)
        
        # Generar nombre único con timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_archivo = f"reporte_{nombre_base}_{timestamp}.md"
        
        ruta_completa = self.reports_dir / nombre_archivo
        
        # Preparar metadatos
        meta = {
            "tema": tema,
            "fecha_creacion": datetime.now().isoformat(),
            "longitud_caracteres": len(contenido_reporte),
            "version": "2.0"
        }
        
        if metadata:
            meta.update(metadata)
        
        try:
            # Guardar reporte en Markdown
            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(f"# Reporte de Investigación: {tema}\n\n")
                f.write(f"**Fecha:** {meta['fecha_creacion']}\n\n")
                f.write("---\n\n")
                f.write(contenido_reporte)
                f.write("\n\n---\n\n")
                f.write("*Generado automáticamente por Asistente de Investigación IA v2.0*\n")
            
            # Guardar metadatos en JSON separado
            meta_path = ruta_completa.with_suffix('.json')
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Reporte guardado exitosamente: {ruta_completa}")
            return ruta_completa
            
        except OSError as e:
            logger.error(f"Error de sistema al guardar archivo: {str(e)}")
        except Exception as e:
            logger.error(f"Error inesperado al guardar reporte: {str(e)}")
        
        return None
    
    def listar_reportes(self) -> list:
        """Lista todos los reportes guardados."""
        try:
            reportes = sorted(
                self.reports_dir.glob("reporte_*.md"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            return reportes
        except Exception as e:
            logger.error(f"Error al listar reportes: {str(e)}")
            return []
    
    def cargar_reporte(self, filename: str) -> Optional[str]:
        """Carga un reporte existente."""
        try:
            ruta = self.reports_dir / filename
            if ruta.exists() and ruta.is_file():
                with open(ruta, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"Error al cargar reporte: {str(e)}")
        return None


# Mantener compatibilidad con código antiguo
def guardar_reporte(tema: str, contenido_reporte: str):
    """Función legacy para compatibilidad."""
    manager = ReportManager()
    result = manager.guardar_reporte(tema, contenido_reporte)
    if result:
        print(f"   [+] ¡Éxito! Reporte guardado en: {result}")
    else:
        print("   [!] Error al intentar guardar el archivo")
