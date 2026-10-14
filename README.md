# Asistente de Investigación IA v2.0

Sistema de investigación automatizado que utiliza IA para buscar, extraer y analizar información de múltiples fuentes web.

## Características

### Funcionalidades
- Búsqueda inteligente en internet (DuckDuckGo)
- Extracción paralela de contenido web
- Análisis con IA (Google Gemini)
- Generación automática de reportes en Markdown
- Sistema de logging profesional

### Seguridad
- API keys protegidas con variables de entorno
- Validación y sanitización de todas las entradas
- Protección contra SSRF y path traversal
- Rate limiting para prevenir abuso
- Sanitización de contenido HTML
- Manejo seguro de errores y excepciones

### Arquitectura
- Programación Orientada a Objetos
- Separación de responsabilidades (SoC)
- Configuración centralizada
- Logging estructurado
- Procesamiento concurrente
- Manejo robusto de errores

## Requisitos

- Python 3.8 o superior
- Cuenta de Google AI Studio (para API key gratuita)

## Instalación

### 1. Clonar o descargar el proyecto

\`\`\`bash
cd ia_investigadora
\`\`\`

### 2. Crear entorno virtual (recomendado)

\`\`\`bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
\`\`\`

### 3. Instalar dependencias

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configurar variables de entorno

\`\`\`bash
# Copiar el archivo de ejemplo
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Editar .env y agregar tu API key de Google
\`\`\`

**Obtener API Key gratuita:**
1. Ir a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crear una nueva API key
3. Copiarla en el archivo `.env`

## Uso

### Modo básico

\`\`\`bash
python main.py
\`\`\`

### Uso programático

\`\`\`python
from main import InvestigadorIA

investigador = InvestigadorIA()
investigador.iniciar_investigacion("Inteligencia Artificial 2024")
\`\`\`

## Estructura del Proyecto

\`\`\`
ia_investigadora/
├── config.py           # Configuración centralizada
├── logger.py           # Sistema de logging
├── validators.py       # Validación y sanitización
├── buscador.py         # Búsqueda web
├── extractor.py        # Extracción de contenido
├── analista.py         # Análisis con IA
├── archivero.py        # Gestión de reportes
├── main.py             # Punto de entrada
├── requirements.txt    # Dependencias
├── .env.example        # Plantilla de configuración
├── .gitignore          # Archivos ignorados por git
└── README.md           # Este archivo
```

## Configuración Avanzada

Edita el archivo `.env` para personalizar:

\`\`\`env
MAX_RESULTADOS=5              # Número de fuentes a buscar
MAX_CARACTERES_POR_PAGINA=5000  # Caracteres por página
REQUEST_TIMEOUT=15            # Timeout de peticiones HTTP
MAX_WORKERS=10                # Workers para extracción paralela
LOG_LEVEL=DEBUG               # Nivel de logging
\`\`\`

## Testing (Próximamente)

\`\`\`bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=. --cov-report=html
\`\`\`

## Consideraciones de Seguridad

### Implementado
- Variables de entorno para secrets
- Validación de URLs (anti-SSRF)
- Sanitización de nombres de archivo
- Rate limiting
- Sanitización HTML
- Logging seguro (redacta secrets)
- Timeouts y reintentos configurables

### Recomendaciones
- Nunca commitear el archivo `.env`
- Rotar las API keys periódicamente
- Revisar logs regularmente
- Mantener dependencias actualizadas

## Actualizaciones desde v1.0

### Seguridad
- API key movida a variables de entorno
- Validación completa de entradas
- Protección contra ataques comunes
- Rate limiting implementado

### Arquitectura
- Refactorización completa a POO
- Sistema de logging profesional
- Configuración centralizada
- Extracción concurrente (más rápido)

### Funcionalidad
- Metadatos en reportes
- Manejo robusto de errores
- Reintentos automáticos
- Mejor calidad de extracción

## Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## Soporte

Si encuentras algún problema:
1. Revisa los logs en `logs/investigador.log`
2. Verifica tu archivo `.env`
3. Asegúrate de tener las dependencias correctas
4. Crea un issue en el repositorio

## Autor

Desarrollado como proyecto educativo de IA y seguridad.

---
hola
**Versión:** 2.0.0  
**Última actualización:** 2026
