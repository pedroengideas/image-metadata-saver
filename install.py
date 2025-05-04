"""
Script de instalación para la extensión Image Metadata Saver
"""

import os
import shutil
import sys
import subprocess

# Directorio de la extensión
EXT_DIR = os.path.dirname(os.path.realpath(__file__))

def main():
    print("Instalando Image Metadata Saver para Automatic1111...")
    
    # Crear estructura de directorios
    os.makedirs(os.path.join(EXT_DIR, "saved_images"), exist_ok=True)
    os.makedirs(os.path.join(EXT_DIR, "metadata"), exist_ok=True)
    
    # Verificar que todos los archivos necesarios estén presentes
    required_files = [
        "scripts/image_metadata_saver.py",
        "scripts/api.py",
        "javascript/script.js",
        "style.css",
        "__init__.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(EXT_DIR, file)):
            missing_files.append(file)
    
    if missing_files:
        print("Error: Faltan los siguientes archivos necesarios:")
        for file in missing_files:
            print(f"  - {file}")
        print("La instalación no puede continuar.")
        return 1
    
    # Instalar dependencias si es necesario
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-warn-script-location", "Pillow"])
    except subprocess.CalledProcessError:
        print("Advertencia: No se pudieron instalar dependencias. El plugin puede no funcionar correctamente.")
    
    print("La extensión Image Metadata Saver se ha instalado correctamente.")
    print("Reinicia Automatic1111 WebUI para activar la extensión.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())