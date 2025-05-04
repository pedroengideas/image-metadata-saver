# Image Metadata Saver - Extensión para Automatic1111 WebUI

Una extensión para Automatic1111 WebUI (Stable Diffusion) que permite guardar imágenes generadas junto con todos sus metadatos en formato JSON, y proporciona una interfaz para visualizar el historial de imágenes guardadas.

## Características

- Botones de guardado en cada imagen generada en las galerías de txt2img y img2img
- Guarda la imagen en formato PNG junto con un archivo JSON que contiene:
  - Prompt utilizado
  - Negative prompt
  - Semilla (seed)
  - Pasos (steps)
  - Sampler
  - CFG Scale
  - Tamaño de la imagen
  - Modelo utilizado
  - Hash del modelo
  - Otros parámetros de generación
- Pestaña "Guardados" que muestra un historial de todas las imágenes guardadas
- Visor detallado de metadatos con función para copiar al portapapeles
- Interfaz intuitiva y fácil de usar

## Instalación

### Método 1: Desde la interfaz de WebUI

1. Ve a la pestaña "Extensions" en Automatic1111 WebUI
2. Haz clic en "Install from URL"
3. Introduce la URL de este repositorio
4. Haz clic en "Install"
5. Reinicia la WebUI

### Método 2: Instalación manual

1. Clona este repositorio en la carpeta `extensions` de tu instalación de Automatic1111:
   ```bash
   cd /ruta/a/stable-diffusion-webui/extensions/
   git clone https://github.com/tu-usuario/sd-webui-image-metadata-saver
   ```
2. Reinicia la WebUI

## Uso

### Guardar una imagen y sus metadatos

1. Genera una imagen en txt2img o img2img
2. Haz clic en el botón "💾 Guardar" que aparece al pasar el cursor sobre la imagen en la galería
3. La imagen y sus metadatos se guardarán automáticamente

### Ver imágenes guardadas

1. Ve a la pestaña "Image Metadata Saver" en la interfaz de WebUI
2. En la subpestaña "Guardados" encontrarás todas las imágenes que has guardado
3. Cada imagen muestra una vista previa junto con información básica
4. Haz clic en "Ver detalles" para ver todos los metadatos de la imagen

### Configuración

En la pestaña de "Configuración" puedes:
- Ver la ubicación de los directorios donde se guardan las imágenes y metadatos
- Configurar opciones adicionales (en desarrollo)

## Estructura de directorios

- `saved_images/`: Directorio donde se guardan las imágenes PNG
- `metadata/`: Directorio donde se guardan los archivos JSON con metadatos
- `history.json`: Archivo que almacena el historial de imágenes guardadas

## Formato de metadatos

Los metadatos se guardan en formato JSON y contienen:

```json
{
  "timestamp": "2025-05-04T10:30:00.000Z",
  "filename": "image_20250504_103000_1234567890.png",
  "parameters": {
    "prompt": "texto del prompt utilizado",
    "negative_prompt": "texto del negative prompt utilizado",
    "steps": 20,
    "sampler": "DPM++ 2M",
    "cfg_scale": 7,
    "seed": 1234567890,
    "size": "512x512",
    "model": "thePrunedStableDiffusionXL",
    "model_hash": "a7d2d9a924",
    "batch_size": 1,
    "type": "txt2img"
  }
}
```

## Desarrollo

Si deseas contribuir al desarrollo de este plugin:

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b mi-nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin mi-nueva-caracteristica`)
5. Crea un nuevo Pull Request

## Resolución de problemas

Si encuentras algún problema:

- Verifica que todos los archivos necesarios estén instalados correctamente
- Comprueba los logs de Automatic1111 para ver si hay errores
- Abre un issue en el repositorio con una descripción detallada del problema

## Licencia

Este proyecto está licenciado bajo la licencia MIT. Ver el archivo LICENSE para más detalles.
