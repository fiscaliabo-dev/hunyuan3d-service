import requests
import os

# Configuración
URL_API = "http://localhost:8000/generate-3d/"
CARPETA_IMAGENES = "pruebas"
IMAGENES_REQUERIDAS = ["front.png", "back.png", "left.png", "right.png", "top.png", "bottom.png"]

def probar_generacion_3d():
    print("Iniciando prueba de generación 3D...")
    
    # 1. Preparar los archivos para enviar
    files = {}
    try:
        for nombre in IMAGENES_REQUERIDAS:
            ruta = os.path.join(CARPETA_IMAGENES, nombre)
            if not os.path.exists(ruta):
                print(f"❌ Error: No se encuentra la imagen {ruta}")
                return
            files[nombre.split('.')[0]] = (nombre, open(ruta, 'rb'), 'image/png')
    except Exception as e:
        print(f"❌ Error al abrir imágenes: {e}")
        return

    # 2. Enviar la petición al contenedor Docker
    try:
        print("📤 Enviando imágenes a la RTX 4080 (esto puede tardar 1-2 minutos)...")
        response = requests.post(URL_API, files=files, timeout=300) 
        
        if response.status_code == 200:
            nombre_archivo = "resultado_modelo.obj"
            with open(nombre_archivo, "wb") as f:
                f.write(response.content)
            print(f"✅ ¡Éxito! Modelo 3D guardado como: {nombre_archivo}")
        else:
            print(f"❌ Error del servidor ({response.status_code}): {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor. ¿Está corriendo el Docker?")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")
    finally:
        # Cerrar archivos abiertos
        for _, f_tuple in files.items():
            f_tuple[1].close()

if __name__ == "__main__":
    probar_generacion_3d()