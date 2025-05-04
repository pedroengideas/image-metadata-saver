# Estructura de Archivos y Guía de Instalación

## Estructura de directorios

Para que la extensión funcione correctamente, debes organizar los archivos de la siguiente manera:

```
image-metadata-saver/
│
├── README.md                   # Documentación principal
├── __init__.py                 # Archivo de inicialización
├── install.py                  # Script de instalación
├── style.css                   # Estilos CSS
│
├── scripts/                    # Código Python principal
│   ├── __init__.py             # Inicializador vacío 
│   ├── image_metadata_saver.py # Archivo principal con la funcionalidad
│   └── api.py                  # Endpoints de API
│
├── javascript/                 # Código JavaScript para la interfaz
│   └── script.js               # Script principal
│
├── saved_images/               # Directorio donde se guardarán las imágenes
└── metadata/                   # Directorio donde se guardarán los metadatos
```

## Guía de Instalación

### Paso 1: Preparar la estructura de directorios

1. Crea una carpeta llamada `image-metadata-saver` en el directorio `extensions` de tu instalación de Automatic1111.
2. Dentro de esta carpeta, crea las subcarpetas: `scripts`, `javascript`, `saved_images` y `metadata`.

### Paso 2: Copiar los archivos

1. Coloca `image_metadata_saver.py` y `api.py` en la carpeta `scripts/`.
2. Crea un archivo `__init__.py` vacío en la carpeta `scripts/`.
3. Coloca `script.js` en la carpeta `javascript/`.
4. Coloca `__init__.py`, `install.py` y `style.css` en la carpeta principal.
5. Coloca `README.md` en la carpeta principal.

### Paso 3: Ejecutar la instalación

1. Reinicia Automatic1111 WebUI.
2. Si es necesario, puedes ejecutar el script de instalación:
   ```
   cd /ruta/a/stable-diffusion-webui/extensions/image-metadata-saver/
   python install.py
   ```

### Paso 4: Verificar la instalación

1. Una vez reiniciado Automatic1111, deberías ver una nueva pestaña llamada "Image Metadata Saver".
2. Genera una imagen y comprueba que aparece el botón de guardado al pasar el cursor sobre la imagen.
3. Guarda una imagen y verifica que aparece en la pestaña "Guardados".

## Estructura Completa con Contenido

A continuación se detalla qué contiene cada archivo:

1. **image_metadata_saver.py**: Contiene la funcionalidad principal para extraer metadatos, guardar imágenes y crear la interfaz de usuario.

2. **api.py**: Implementa los endpoints de API para guardar imágenes, obtener metadatos y administrar el historial desde JavaScript.

3. **script.js**: Maneja la interacción del usuario con la interfaz, agrega botones a las imágenes generadas y muestra notificaciones.

4. **style.css**: Define los estilos visuales para la extensión, incluyendo la vista de historial, botones y modales.

5. **__init__.py**: Inicializa la extensión y carga los scripts necesarios.

6. **install.py**: Configura los directorios necesarios y comprueba las dependencias.

7. **README.md**: Proporciona documentación sobre cómo usar la extensión.

## Solución de problemas comunes

- **Error "Module not found"**: Asegúrate de que la estructura de directorios sea correcta y que todos los archivos estén en su lugar.

- **Los botones de guardado no aparecen**: Verifica que `script.js` esté correctamente ubicado y que la WebUI se haya reiniciado.

- **No se guardan las imágenes**: Comprueba que los directorios `saved_images` y `metadata` tengan permisos de escritura.

- **La pestaña no aparece**: Verifica los logs de Automatic1111 para ver si hay errores al cargar la extensión.

- **Errores en la consola JavaScript**: Abre la consola del navegador (F12) para ver si hay errores de JavaScript que puedan estar afectando la funcionalidad.
