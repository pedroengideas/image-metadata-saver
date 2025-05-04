"""
Image Metadata Saver - Extension for Automatic1111 WebUI
Permite guardar imágenes junto con sus metadatos en formato JSON y visualizar un historial de imágenes guardadas.
"""

import os
import json
import datetime
import gradio as gr
from modules import script_callbacks, shared, ui_components
from modules.processing import StableDiffusionProcessingTxt2Img, StableDiffusionProcessingImg2Img
from modules.images import save_image
from PIL import Image
import base64
from io import BytesIO

# Configuración de la extensión
EXTENSION_NAME = "Image Metadata Saver"
SAVED_IMAGES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "saved_images")
METADATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "metadata")
HISTORY_FILE = os.path.join(METADATA_DIR, "history.json")

# Asegurarse de que los directorios existan
os.makedirs(SAVED_IMAGES_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

# Inicializar el historial si no existe
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def extract_metadata(image, p=None):
    """Extrae los metadatos de la imagen generada y el procesamiento"""
    metadata = {
        "timestamp": datetime.datetime.now().isoformat(),
        "filename": "",  # Se establecerá después de guardar
        "parameters": {}
    }
    
    # Extraer parámetros de generación si están disponibles
    if p:
        if isinstance(p, (StableDiffusionProcessingTxt2Img, StableDiffusionProcessingImg2Img)):
            metadata["parameters"] = {
                "prompt": p.prompt,
                "negative_prompt": p.negative_prompt,
                "steps": p.steps,
                "sampler": p.sampler_name,
                "cfg_scale": p.cfg_scale,
                "seed": p.seed,
                "size": f"{p.width}x{p.height}",
                "model": shared.sd_model.model_name if hasattr(shared, "sd_model") and shared.sd_model else "unknown",
                "model_hash": shared.sd_model.sd_model_hash if hasattr(shared, "sd_model") and shared.sd_model else "unknown",
                "batch_size": p.batch_size if hasattr(p, "batch_size") else 1,
                "type": "txt2img" if isinstance(p, StableDiffusionProcessingTxt2Img) else "img2img"
            }
        else:
            # Intenta extraer información desde otros tipos de procesamiento o imágenes
            try:
                metadata["parameters"] = p.__dict__
            except:
                pass
    
    # Intenta extraer metadatos de la imagen
    if hasattr(image, "info") and image.info:
        metadata["image_info"] = image.info
    
    # Intenta extraer metadatos desde los parámetros de generación en la imagen
    try:
        parameters = image.info.get("parameters", "")
        if parameters:
            # Aquí podrías parsear los parámetros de texto a un diccionario estructurado
            metadata["parsed_parameters"] = parameters
    except:
        pass
        
    return metadata

def save_image_with_metadata(image, metadata=None, p=None):
    """Guarda la imagen y sus metadatos"""
    if metadata is None:
        metadata = extract_metadata(image, p)
    
    # Generar nombre de archivo único
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}_{metadata['parameters'].get('seed', 'unknown')}"
    
    # Guardar la imagen
    image_path = os.path.join(SAVED_IMAGES_DIR, f"{filename}.png")
    image.save(image_path)
    
    # Actualizar metadatos con el nombre de archivo
    metadata["filename"] = f"{filename}.png"
    metadata["image_path"] = image_path
    
    # Guardar metadatos como JSON
    json_path = os.path.join(METADATA_DIR, f"{filename}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # Actualizar el historial
    update_history(metadata)
    
    return image_path, json_path

def update_history(metadata):
    """Actualiza el archivo de historial con los nuevos metadatos"""
    history = []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except:
        history = []
    
    # Añadir nuevos metadatos al historial
    history.append({
        "timestamp": metadata["timestamp"],
        "filename": metadata["filename"],
        "preview": metadata.get("parameters", {}).get("prompt", "")[:100] + "..." if len(metadata.get("parameters", {}).get("prompt", "")) > 100 else metadata.get("parameters", {}).get("prompt", ""),
        "metadata_file": os.path.join(METADATA_DIR, f"{metadata['filename'].split('.')[0]}.json")
    })
    
    # Guardar historial actualizado
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def image_to_base64(image):
    """Convierte una imagen PIL a base64 para mostrar en la interfaz"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

def load_history():
    """Carga el historial de imágenes guardadas"""
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def create_history_html():
    """Crea el HTML para mostrar el historial de imágenes guardadas"""
    history = load_history()
    
    if not history:
        return "<div class='history-empty'>No hay imágenes guardadas en el historial.</div>"
    
    html = "<div class='history-container'>"
    
    # Ordenar por timestamp (más reciente primero)
    history.sort(key=lambda x: x["timestamp"], reverse=True)
    
    for item in history:
        image_path = os.path.join(SAVED_IMAGES_DIR, item["filename"])
        
        if os.path.exists(image_path):
            # Cargar metadatos para mostrar información detallada
            metadata = {}
            try:
                with open(item["metadata_file"], "r", encoding="utf-8") as f:
                    metadata = json.load(f)
            except:
                metadata = {"parameters": {"prompt": "Metadatos no disponibles"}}
            
            # Crear tarjeta para la imagen en el historial
            html += f"""
            <div class='history-item'>
                <div class='history-image'>
                    <img src='file={image_path}' alt='{item["filename"]}'>
                </div>
                <div class='history-details'>
                    <h4>{item["filename"]}</h4>
                    <p><strong>Fecha:</strong> {datetime.datetime.fromisoformat(item["timestamp"]).strftime("%d/%m/%Y %H:%M:%S")}</p>
                    <p><strong>Prompt:</strong> {metadata.get("parameters", {}).get("prompt", "No disponible")[:100]}...</p>
                    <p><strong>Seed:</strong> {metadata.get("parameters", {}).get("seed", "No disponible")}</p>
                    <button class='view-details' onclick='viewImageDetails("{item["metadata_file"]}","{image_path}")'>Ver detalles</button>
                </div>
            </div>
            """
    
    html += "</div>"
    return html

def on_ui():
    """Función principal para crear la interfaz de usuario de la extensión"""
    with gr.Blocks(analytics_enabled=False) as ui:
        with gr.Tab("Guardados"):
            gr.HTML("""
            <style>
                .history-container {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                }
                .history-item {
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 10px;
                    width: 300px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .history-image img {
                    width: 100%;
                    height: auto;
                    border-radius: 4px;
                }
                .history-details {
                    margin-top: 10px;
                }
                .view-details {
                    background-color: #4a6cf7;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 4px;
                    cursor: pointer;
                    margin-top: 10px;
                }
                .view-details:hover {
                    background-color: #3a5ce5;
                }
                .history-empty {
                    padding: 20px;
                    text-align: center;
                    color: #666;
                }
            </style>
            <script>
                function viewImageDetails(metadataFile, imagePath) {
                    // Aquí podrías implementar un modal para mostrar los detalles completos
                    // O redirigir a una página de detalles
                    fetch(metadataFile)
                        .then(response => response.json())
                        .then(data => {
                            alert(JSON.stringify(data, null, 2));
                        });
                }
            </script>
            """)
            
            # Botón para refrescar el historial
            refresh_btn = gr.Button("Refrescar historial")
            
            # Panel para mostrar el historial
            history_panel = gr.HTML(create_history_html())
            
            # Refrescar el historial cuando se haga clic en el botón
            refresh_btn.click(
                fn=lambda: gr.update(value=create_history_html()),
                outputs=history_panel
            )
        
        with gr.Tab("Configuración"):
            gr.Markdown("""
            # Configuración del Image Metadata Saver
            
            Esta extensión te permite guardar automáticamente las imágenes generadas junto con sus metadatos.
            También puedes ver un historial de las imágenes guardadas en la pestaña "Guardados".
            """)
            
            save_dir = gr.Textbox(
                label="Directorio de imágenes guardadas",
                value=SAVED_IMAGES_DIR,
                interactive=False
            )
            
            metadata_dir = gr.Textbox(
                label="Directorio de metadatos",
                value=METADATA_DIR,
                interactive=False
            )
            
            # Opciones adicionales que podrías implementar
            auto_save = gr.Checkbox(
                label="Guardar automáticamente todas las imágenes generadas",
                value=False
            )
            
            # Esta función se implementaría para aplicar la configuración
            save_config_btn = gr.Button("Guardar configuración")
            save_config_btn.click(
                fn=lambda x: gr.update(value="Configuración guardada!"),
                inputs=[auto_save],
                outputs=[gr.Textbox(value="", visible=False)]
            )
    
    return [(ui, EXTENSION_NAME, EXTENSION_NAME.lower().replace(" ", "_"))]

# Agregar botones a la interfaz de generación de imágenes
def add_save_buttons(image_path, gallery, generation_info, html_info, html_log, index=0):
    """Agrega botones de guardado a cada imagen generada"""
    # Obtener la imagen actual del índice
    if gallery and hasattr(gallery, "selected_gallery"):
        current_image_info = gallery.selected_gallery[index] if index < len(gallery.selected_gallery) else None
        if current_image_info:
            current_image = current_image_info.get("image", None)
            if current_image:
                # Crear un botón para guardar esta imagen
                save_btn = gr.Button(f"💾 Guardar imagen y metadatos")
                save_btn.click(
                    fn=lambda: save_image_with_metadata(current_image, p=generation_info),
                    outputs=[gr.Textbox(value="Imagen y metadatos guardados correctamente")]
                )
                return [save_btn]
    return []

# Registrar callbacks
def on_app_started(demo, app):
    """Se ejecuta cuando se inicia la aplicación"""
    script_callbacks.on_ui_tabs(on_ui)
    
    # Registrar callback para agregar botones a las imágenes generadas
    # Esto dependerá de la estructura exacta de la UI de Automatic1111
    # y podría requerir ajustes adicionales

script_callbacks.on_app_started(on_app_started)