# 📝 Changelog

Todos los cambios notables en este proyecto serán documentados aquí.

## [2.0.0] - 2026-10-13

### 🔒 Seguridad (CRÍTICO)
- **FIXED:** API key movida de código fuente a variables de entorno
- **ADDED:** Validación completa de entradas de usuario
- **ADDED:** Protección contra SSRF (Server-Side Request Forgery)
- **ADDED:** Protección contra Path Traversal
- **ADDED:** Sanitización de contenido HTML (anti-XSS)
- **ADDED:** Rate limiting para prevenir abuso
- **ADDED:** Logger con redacción automática de secrets
- **ADDED:** Validación de URLs antes de acceder
- **ADDED:** Timeouts y reintentos configurables

### 🏗️ Arquitectura
- **CHANGED:** Refactorización completa a Programación Orientada a Objetos
- **ADDED:** Clase `InvestigadorIA` como orquestador principal
- **ADDED:** Clase `WebSearcher` para búsquedas
- **ADDED:** Clase `WebExtractor` para extracción
- **ADDED:** Clase `IAAnalyzer` para análisis
- **ADDED:** Clase `ReportManager` para gestión de archivos
- **ADDED:** Clase `InputValidator` para validación
- **ADDED:** Clase `Config` para configuración centralizada
- **ADDED:** Clase `SecureLogger` para logging profesional

### ⚡ Rendimiento
- **ADDED:** Extracción paralela de contenido (ThreadPoolExecutor)
- **ADDED:** Reintentos automáticos con backoff exponencial
- **IMPROVED:** Procesamiento más rápido con concurrencia

### 📦 Configuración
- **ADDED:** Archivo `.env` para variables de entorno
- **ADDED:** Archivo `.env.example` como plantilla
- **ADDED:** `config.py` para configuración centralizada
- **ADDED:** `.gitignore` para proteger archivos sensibles
- **ADDED:** Validación de configuración al inicio

### 📊 Logging
- **ADDED:** Sistema de logging estructurado
- **ADDED:** Logs en archivo y consola
- **ADDED:** Niveles de log configurables
- **ADDED:** Rotación de logs (opcional)
- **ADDED:** Sanitización automática de secrets en logs

### 📄 Documentación
- **ADDED:** README.md completo y profesional
- **ADDED:** SECURITY.md con análisis de vulnerabilidades
- **ADDED:** INSTALL.md con guía de instalación paso a paso
- **ADDED:** Este CHANGELOG.md
- **IMPROVED:** Comentarios y docstrings en todo el código

### 🧪 Testing
- **ADDED:** Estructura básica de tests con pytest
- **ADDED:** Tests para validadores
- **ADDED:** Configuración para cobertura de código

### 📝 Reportes
- **ADDED:** Metadatos en reportes (fecha, fuentes, etc.)
- **ADDED:** Archivos JSON con metadata separada
- **ADDED:** Timestamps únicos en nombres de archivo
- **IMPROVED:** Formato Markdown más profesional

### 🔧 Dependencias
- **ADDED:** requirements.txt con versiones específicas
- **ADDED:** Nuevas dependencias:
  - python-dotenv (variables de entorno)
  - ratelimit (control de frecuencia)
  - validators (validación de URLs)
  - bleach (sanitización HTML)
  - lxml (parsing XML/HTML más rápido)
  - pytest, black, flake8 (desarrollo)

### 🐛 Bug Fixes
- **FIXED:** Manejo de errores HTTP inconsistente
- **FIXED:** Timeout no configurado en todas las peticiones
- **FIXED:** Posible crash con páginas sin párrafos
- **FIXED:** Nombres de archivo con caracteres inválidos
- **FIXED:** Búsquedas vacías causaban errores

### 🗑️ Deprecated
- **DEPRECATED:** Funciones globales legacy (se mantienen para compatibilidad)

## [1.0.0] - 2026-04-13

### Versión Inicial
- Búsqueda básica en DuckDuckGo
- Extracción de contenido web
- Análisis con Google Gemini
- Guardado de reportes en Markdown

### ⚠️ Problemas Conocidos (v1.0)
- API key hardcodeada en código
- Sin validación de entradas
- Sin protección SSRF
- Sin protección Path Traversal
- Sin sanitización HTML
- Sin rate limiting
- Sin logging estructurado
- Sin manejo robusto de errores

---

## Formato

Este changelog sigue el formato de [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/lang/es/).

### Tipos de cambios
- **ADDED** - Nuevas características
- **CHANGED** - Cambios en funcionalidad existente
- **DEPRECATED** - Características que serán eliminadas
- **REMOVED** - Características eliminadas
- **FIXED** - Correcciones de bugs
- **SECURITY** - Vulnerabilidades corregidas
