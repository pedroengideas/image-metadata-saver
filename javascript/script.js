// Image Metadata Saver - JavaScript para la interfaz de usuario
document.addEventListener('DOMContentLoaded', function() {
    // Esperamos a que la UI de Automatic1111 esté completamente cargada
    const checkUILoaded = setInterval(function() {
        if (document.querySelector('#txt2img_generate') || document.querySelector('#img2img_generate')) {
            clearInterval(checkUILoaded);
            initializePlugin();
        }
    }, 1000);
});

function initializePlugin() {
    // Añadir botones de guardado a la interfaz de generación de imágenes
    addSaveButtonsToGallery('txt2img_gallery');
    addSaveButtonsToGallery('img2img_gallery');
    
    // Añadir observador para detectar nuevas imágenes generadas
    observeGalleries();
}

function addSaveButtonsToGallery(galleryId) {
    const gallery = document.getElementById(galleryId);
    if (!gallery) return;
    
    // Buscar el contenedor de imágenes dentro de la galería
    const imgContainers = gallery.querySelectorAll('.thumbnail-item');
    
    imgContainers.forEach((container, index) => {
        // Verificar si ya tiene el botón de guardar
        if (container.querySelector('.save-metadata-btn')) return;
        
        // Crear el botón de guardar
        const saveBtn = document.createElement('button');
        saveBtn.className = 'save-metadata-btn';
        saveBtn.innerHTML = '💾 Guardar';
        saveBtn.title = 'Guardar imagen con metadatos';
        saveBtn.style.cssText = `
            position: absolute;
            bottom: 10px;
            right: 10px;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px 8px;
            font-size: 12px;
            cursor: pointer;
            z-index: 10;
        `;
        
        // Añadir evento al botón
        saveBtn.addEventListener('click', function(e) {
            e.stopPropagation(); // Evitar que se abra la imagen al hacer clic en el botón
            saveImageWithMetadata(galleryId, index);
        });
        
        // Añadir el botón al contenedor
        container.style.position = 'relative';
        container.appendChild(saveBtn);
    });
}

function saveImageWithMetadata(galleryId, index) {
    // Aquí hacemos una llamada a la API de la extensión para guardar la imagen
    // Esto requiere que establezcamos un endpoint en la extensión Python
    
    fetch('/api/image_metadata_saver/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            gallery_id: galleryId,
            image_index: index
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Imagen guardada correctamente con sus metadatos');
        } else {
            showNotification('Error al guardar la imagen: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error de conexión al guardar la imagen', 'error');
    });
}

function observeGalleries() {
    // Observamos cambios en las galerías para añadir botones a nuevas imágenes
    const galleries = ['txt2img_gallery', 'img2img_gallery'];
    
    galleries.forEach(galleryId => {
        const gallery = document.getElementById(galleryId);
        if (!gallery) return;
        
        // Configurar el observador
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' || mutation.type === 'subtree') {
                    // Cuando hay cambios en la galería, añadimos botones
                    addSaveButtonsToGallery(galleryId);
                }
            });
        });
        
        // Iniciar observación
        observer.observe(gallery, { 
            childList: true, 
            subtree: true 
        });
    });
}

function showNotification(message, type = 'success') {
    // Crear notificación
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: ${type === 'success' ? '#4caf50' : '#f44336'};
        color: white;
        padding: 15px;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        z-index: 1000;
        max-width: 300px;
    `;
    
    // Añadir al DOM
    document.body.appendChild(notification);
    
    // Eliminar después de 3 segundos
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.5s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 3000);
}

// Función para crear una vista de detalles
function viewImageDetails(metadataFile, imagePath) {
    // Crear modal para mostrar detalles completos
    const modal = document.createElement('div');
    modal.className = 'metadata-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    `;
    
    // Crear contenido del modal
    const modalContent = document.createElement('div');
    modalContent.className = 'metadata-modal-content';
    modalContent.style.cssText = `
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        width: 80%;
        max-width: 800px;
        max-height: 80vh;
        overflow-y: auto;
        display: flex;
        gap: 20px;
    `;
    
    // Cargar los metadatos
    fetch(metadataFile)
        .then(response => response.json())
        .then(metadata => {
            // Crear contenido del modal con la imagen y metadatos
            modalContent.innerHTML = `
                <div style="flex: 1; max-width: 50%;">
                    <h2>Imagen</h2>
                    <img src="${imagePath}" style="max-width: 100%; max-height: 70vh;" />
                </div>
                <div style="flex: 1; overflow-y: auto;">
                    <h2>Metadatos</h2>
                    <button id="copyMetadataBtn" style="margin-bottom: 10px; padding: 5px 10px; background: #4a6cf7; color: white; border: none; border-radius: 4px; cursor: pointer;">Copiar Metadatos</button>
                    <pre style="background: #f5f5f5; padding: 10px; border-radius: 4px; white-space: pre-wrap;">${JSON.stringify(metadata, null, 2)}</pre>
                </div>
                <button id="closeModalBtn" style="position: absolute; top: 10px; right: 10px; background: none; border: none; font-size: 24px; cursor: pointer;">×</button>
            `;
            
            modal.appendChild(modalContent);
            document.body.appendChild(modal);
            
            // Añadir evento para cerrar el modal
            document.getElementById('closeModalBtn').addEventListener('click', function() {
                document.body.removeChild(modal);
            });
            
            // Añadir evento para copiar metadatos
            document.getElementById('copyMetadataBtn').addEventListener('click', function() {
                navigator.clipboard.writeText(JSON.stringify(metadata, null, 2));
                showNotification('Metadatos copiados al portapapeles');
            });
        })
        .catch(error => {
            console.error('Error al cargar metadatos:', error);
            modalContent.innerHTML = `
                <div style="text-align: center; width: 100%;">
                    <h2>Error al cargar metadatos</h2>
                    <p>No se pudieron cargar los metadatos de la imagen.</p>
                </div>
                <button id="closeModalBtn" style="position: absolute; top: 10px; right: 10px; background: none; border: none; font-size: 24px; cursor: pointer;">×</button>
            `;
            
            modal.appendChild(modalContent);
            document.body.appendChild(modal);
            
            document.getElementById('closeModalBtn').addEventListener('click', function() {
                document.body.removeChild(modal);
            });
        });
}

// Exponer la función al ámbito global para que pueda ser llamada desde HTML
window.viewImageDetails = viewImageDetails;