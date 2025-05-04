"""
API endpoints para la extensión Image Metadata Saver
"""

import os
import json
import datetime
from fastapi import FastAPI, HTTPException, Request
from PIL import Image
from modules import script_callbacks, shared
from modules.shared import opts
from modules.api import api

from scripts.image_metadata_saver import (
    extract_metadata, 
    save_image_with_metadata, 
    SAVED_IMAGES_DIR, 
    METADATA_DIR
)

# Crear endpoint API para guardar imágenes
def image_metadata_saver_api(_: gr.Blocks, app: FastAPI):
    @app.post("/api/image_metadata_saver/save")
    async def save_image(request: Request):
        try:
            data = await request.json()
            gallery_id = data.get("gallery_id")
            image_index = data.get("image_index", 0)
            
            # Validar datos
            if not gallery_id:
                raise HTTPException(status_code=400, detail="Se requiere gallery_id")
            
            # Obtener la imagen del gallery
            if gallery_id == "txt2img_gallery":
                if not shared.txt2img_gallery:
                    raise HTTPException(status_code=404, detail="No se encontró la galería txt2img")
                image_data = shared.txt2img_gallery[image_index] if image_index < len(shared.txt2img_gallery) else None
            elif gallery_id == "img2img_gallery":
                if not shared.img2img_gallery:
                    raise HTTPException(status_code=404, detail="No se encontró la galería img2img")
                image_data = shared.img2img_gallery[image_index] if image_index < len(shared.img2img_gallery) else None
            else:
                raise HTTPException(status_code=400, detail=f"Galería desconocida: {gallery_id}")
            
            if not image_data:
                raise HTTPException(status_code=404, detail=f"No se encontró la imagen con índice {image_index}")
            
            # Extraer imagen y metadata
            image = image_data.get("image")
            if not image:
                raise HTTPException(status_code=404, detail="No se encontró la imagen en los datos")
            
            # Obtener información de generación
            generation_info = None
            if hasattr(shared, 'generation_info') and shared.generation_info is not None:
                generation_info = shared.generation_info[image_index] if image_index < len(shared.generation_info) else None
            
            # Guardar imagen y metadatos
            image_path, json_path = save_image_with_metadata(image, p=generation_info)
            
            return {
                "success": True,
                "image_path": image_path,
                "metadata_path": json_path
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
    
    @app.get("/api/image_metadata_saver/history")
    async def get_history():
        try:
            history_file = os.path.join(METADATA_DIR, "history.json")
            if not os.path.exists(history_file):
                return {"success": True, "data": []}
            
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
            
            return {"success": True, "data": history}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @app.get("/api/image_metadata_saver/metadata/{filename}")
    async def get_metadata(filename: str):
        try:
            # Validar nombre de archivo para evitar path traversal
            if ".." in filename or "/" in filename or "\\" in filename:
                raise HTTPException(status_code=400, detail="Nombre de archivo inválido")
            
            # Obtener ruta completa
            json_path = os.path.join(METADATA_DIR, filename)
            if not os.path.exists(json_path):
                raise HTTPException(status_code=404, detail=f"No se encontró el archivo de metadatos: {filename}")
            
            with open(json_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            
            return {"success": True, "data": metadata}
        except HTTPException as e:
            raise e
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @app.delete("/api/image_metadata_saver/delete/{filename}")
    async def delete_image(filename: str):
        try:
            # Validar nombre de archivo para evitar path traversal
            if ".." in filename or "/" in filename or "\\" in filename:
                raise HTTPException(status_code=400, detail="Nombre de archivo inválido")
            
            # Obtener rutas completas
            image_path = os.path.join(SAVED_IMAGES_DIR, filename)
            json_path = os.path.join(METADATA_DIR, f"{os.path.splitext(filename)[0]}.json")
            
            # Eliminar archivos si existen
            if os.path.exists(image_path):
                os.remove(image_path)
            
            if os.path.exists(json_path):
                os.remove(json_path)
            
            # Actualizar historial
            history_file = os.path.join(METADATA_DIR, "history.json")
            if os.path.exists(history_file):
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
                
                # Filtrar el elemento eliminado
                history = [item for item in history if item["filename"] != filename]
                
                with open(history_file, "w", encoding="utf-8") as f:
                    json.dump(history, f, indent=2, ensure_ascii=False)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Registrar callback para API
script_callbacks.on_app_started(image_metadata_saver_api)