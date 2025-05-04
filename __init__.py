"""
Image Metadata Saver - Extensión para Automatic1111 WebUI
Permite guardar imágenes junto con sus metadatos en formato JSON y visualizar un historial de imágenes guardadas.
"""

import os
import importlib
import pkgutil
import sys

# Asegúrate de que los scripts se carguen correctamente
scripts_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, scripts_dir)

# Importar submódulos automáticamente
for _, name, _ in pkgutil.iter_modules([scripts_dir]):
    importlib.import_module(f'scripts.{name}')