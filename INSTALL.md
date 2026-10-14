# 📦 Guía de Instalación Completa

Esta guía te llevará paso a paso por la instalación del Asistente de Investigación IA v2.0.

## 📋 Prerrequisitos

### 1. Python

Necesitas Python 3.8 o superior.

**Verificar instalación:**
```bash
python --version
```

**Instalar Python (si no lo tienes):**
- **Windows:** Descarga desde [python.org](https://www.python.org/downloads/)
- **Linux:** `sudo apt install python3 python3-pip`
- **Mac:** `brew install python3`

### 2. pip (Gestor de paquetes)

Normalmente viene con Python. Verificar:
```bash
pip --version
```

## 🚀 Instalación

### Paso 1: Descargar el proyecto

```bash
# Si usas git
git clone <url-del-repositorio>
cd ia_investigadora

# O descomprime el ZIP si lo descargaste
```

### Paso 2: Crear entorno virtual (RECOMENDADO)

Un entorno virtual aísla las dependencias del proyecto.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Verás `(venv)` al inicio de tu terminal cuando esté activado.

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

Este comando instalará:
- requests (peticiones HTTP)
- beautifulsoup4 (extracción web)
- duckduckgo-search (búsqueda)
- google-generativeai (IA)
- Y más...

### Paso 4: Configurar variables de entorno

1. **Copiar plantilla:**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. **Obtener API Key de Google:**
   - Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Inicia sesión con tu cuenta Google
   - Click en "Create API Key"
   - Copia la clave generada

3. **Editar archivo .env:**
   - Abre `.env` con tu editor de texto favorito
   - Reemplaza `tu_clave_aqui` con tu API key real:
   ```env
   GOOGLE_API_KEY=AIzaSy...tu_clave_real_aqui
   ```
   - Guarda el archivo

### Paso 5: Verificar instalación

```bash
python main.py
```

Si todo está bien, verás:
```
============================================================
    🔍 Asistente de Investigación IA v2.0
    🔒 Versión Segura y Profesional
============================================================
```

## ⚠️ Solución de Problemas

### Error: "No module named '...'"

**Problema:** Faltan dependencias.

**Solución:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Error: "GOOGLE_API_KEY no está configurada"

**Problema:** El archivo .env no existe o está vacío.

**Solución:**
1. Verifica que `.env` existe en la carpeta del proyecto
2. Abre `.env` y asegúrate de tener:
   ```env
   GOOGLE_API_KEY=tu_clave_real
   ```
3. Sin espacios alrededor del `=`
4. Sin comillas en la clave

### Error: "ModuleNotFoundError: No module named 'dotenv'"

**Problema:** python-dotenv no está instalado.

**Solución:**
```bash
pip install python-dotenv
```

### Error de permisos en Windows

**Problema:** No se puede activar el entorno virtual.

**Solución:**
```bash
# Ejecuta PowerShell como administrador
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### La búsqueda no retorna resultados

**Problema:** DuckDuckGo puede estar bloqueado.

**Solución:**
- Verifica tu conexión a internet
- Prueba con otro término de búsqueda
- Espera unos minutos (puede ser rate limiting temporal)

## 🔄 Actualización

Para actualizar a una nueva versión:

```bash
# Actualizar código (si usas git)
git pull

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Verificar que .env tiene nuevas variables (comparar con .env.example)
```

## 🗑️ Desinstalación

```bash
# Desactivar entorno virtual
deactivate

# Eliminar entorno virtual
# Windows
rmdir /s venv

# Linux/Mac
rm -rf venv

# Eliminar proyecto
cd ..
# Windows
rmdir /s ia_investigadora

# Linux/Mac
rm -rf ia_investigadora
```

## 📱 Próximos Pasos

Después de la instalación exitosa:

1. Lee el [README.md](README.md) para aprender a usar el sistema
2. Revisa [SECURITY.md](SECURITY.md) para conocer las medidas de seguridad
3. Ejecuta tu primera investigación:
   ```bash
   python main.py
   ```

## 🆘 Ayuda Adicional

Si tienes problemas:

1. Revisa los logs en `logs/investigador.log`
2. Verifica que todas las dependencias están instaladas: `pip list`
3. Asegúrate de estar en el entorno virtual: verifica el `(venv)` en tu terminal
4. Consulta la documentación de Python: [docs.python.org](https://docs.python.org/)

---

**¿Instalación exitosa?** ¡Excelente! Ahora estás listo para investigar con IA 🎉
