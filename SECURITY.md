# 🔒 Política de Seguridad

## Vulnerabilidades Conocidas

Este documento detalla las vulnerabilidades encontradas en la versión 1.0 y cómo fueron mitigadas en la versión 2.0.

## 🚨 Vulnerabilidades Críticas Resueltas

### 1. API Key Hardcodeada (CRÍTICO)
**Versión 1.0:**
```python
GOOGLE_API_KEY = "AIzaSyDZndaC4O-FRw4EvWtnlWe9BUNMo5yAQ98"
```

**Riesgo:** Exposición de credenciales en repositorio público/privado.

**Solución v2.0:**
- API keys movidas a variables de entorno (`.env`)
- Validación de configuración al inicio
- `.gitignore` configurado correctamente
- Logger sanitiza automáticamente secrets

### 2. Inyección de Comandos
**Versión 1.0:**
```python
tema = input("\n¿Sobre que te gustaria investigar hoy?: ")
# Sin validación ni sanitización
```

**Riesgo:** Inyección de código malicioso en búsquedas.

**Solución v2.0:**
```python
def sanitize_search_query(query: str) -> Optional[str]:
    # Eliminar caracteres peligrosos
    sanitized = re.sub(r'[^\w\s\-"\'áéíóúñÁÉÍÓÚÑ]', '', query)
    # Limitar longitud
    # Validar tipo y contenido
```

### 3. Server-Side Request Forgery (SSRF)
**Versión 1.0:**
```python
respuesta = requests.get(url, headers=headers, timeout=10)
# Sin validación de URL
```

**Riesgo:** Acceso a recursos internos (localhost, 127.0.0.1).

**Solución v2.0:**
```python
def validate_url(url: str) -> bool:
    # Validar esquema (http/https)
    # Bloquear dominios locales
    # Verificar formato de URL
    if any(blocked in parsed.netloc for blocked in Config.BLOCKED_DOMAINS):
        return False
```

### 4. Path Traversal
**Versión 1.0:**
```python
nombre_archivo = f"reporte_{tema.replace(' ', '_')}.md"
# Sin sanitización de nombre de archivo
```

**Riesgo:** Escritura de archivos fuera del directorio permitido.

**Solución v2.0:**
```python
def sanitize_filename(filename: str) -> str:
    # Eliminar path traversal (.., /, \)
    filename = filename.replace("..", "").replace("/", "")
    # Solo caracteres seguros
    filename = re.sub(r'[^\w\-]', '_', filename)
```

### 5. Cross-Site Scripting (XSS) Almacenado
**Versión 1.0:**
```python
texto_completo = " ".join([p.text for p in parrafos])
# Sin sanitización de HTML
```

**Riesgo:** Scripts maliciosos en reportes guardados.

**Solución v2.0:**
```python
def sanitize_html_content(content: str) -> str:
    clean = bleach.clean(content, tags=[], strip=True)
    return clean.strip()
```

## 🛡️ Medidas de Seguridad Implementadas

### Autenticación y Autorización
- ✅ API keys gestionadas con variables de entorno
- ✅ Validación de configuración al inicio
- ✅ Sin credenciales en código fuente

### Validación de Entrada
- ✅ Sanitización de búsquedas del usuario
- ✅ Validación de URLs antes de acceder
- ✅ Sanitización de nombres de archivo
- ✅ Validación de longitud y tipo de datos

### Protección contra Ataques Web
- ✅ Anti-SSRF (bloqueo de localhost)
- ✅ Anti-Path Traversal
- ✅ Sanitización HTML (anti-XSS)
- ✅ Rate limiting (anti-DoS)

### Manejo de Errores
- ✅ Try-catch en todas las operaciones críticas
- ✅ Logging sin exponer información sensible
- ✅ Mensajes de error genéricos al usuario
- ✅ Logs detallados para debugging

### Red y Comunicaciones
- ✅ Timeouts configurables
- ✅ Reintentos con backoff exponencial
- ✅ User-Agent configurado
- ✅ Validación de tipo de contenido

### Logging y Auditoría
- ✅ Sistema de logging estructurado
- ✅ Redacción automática de secrets
- ✅ Logs en archivo y consola
- ✅ Niveles de log configurables

## 🔍 Recomendaciones de Uso Seguro

### Para Desarrolladores
1. **Nunca** commitear el archivo `.env`
2. Usar `.gitignore` correctamente
3. Rotar API keys periódicamente
4. Revisar logs de seguridad
5. Mantener dependencias actualizadas:
   ```bash
   pip list --outdated
   pip install --upgrade -r requirements.txt
   ```

### Para Usuarios
1. Descargar solo de fuentes confiables
2. Verificar integridad del código
3. Usar entorno virtual aislado
4. No ejecutar con privilegios elevados
5. Revisar permisos de archivos

## 🐛 Reportar Vulnerabilidades

Si encuentras una vulnerabilidad de seguridad:

1. **NO** la publiques en issues públicos
2. Envía un reporte privado al mantenedor
3. Incluye:
   - Descripción de la vulnerabilidad
   - Pasos para reproducir
   - Impacto potencial
   - Sugerencia de solución (opcional)

## 📊 Matriz de Riesgo

| Vulnerabilidad | Severidad v1.0 | Estado v2.0 |
|----------------|----------------|-------------|
| API Key expuesta | 🔴 Crítico | ✅ Resuelto |
| Inyección de comandos | 🔴 Crítico | ✅ Resuelto |
| SSRF | 🟠 Alto | ✅ Resuelto |
| Path Traversal | 🟠 Alto | ✅ Resuelto |
| XSS | 🟡 Medio | ✅ Resuelto |
| Sin rate limiting | 🟡 Medio | ✅ Resuelto |
| Logging inseguro | 🟡 Medio | ✅ Resuelto |

## 🔄 Actualizaciones de Seguridad

### v2.0.0 (Actual)
- ✅ Refactorización completa de seguridad
- ✅ Todas las vulnerabilidades críticas resueltas
- ✅ Implementación de mejores prácticas

### v1.0.0 (Deprecado)
- ⚠️ Múltiples vulnerabilidades críticas
- ⚠️ No recomendado para uso en producción

## 📚 Referencias

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Google API Security](https://cloud.google.com/docs/security)

---

**Última actualización:** Octubre 2026  
**Versión del documento:** 2.0
