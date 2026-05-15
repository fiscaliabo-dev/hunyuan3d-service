from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import subprocess

app = FastAPI(title="Hunyuan3D 2.1 Multi-View Service")

# Directorios para procesar archivos
UPLOAD_DIR = "./temp_uploads"
OUTPUT_DIR = "./outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/generate-3d/")
async def generate_3d(
    front: UploadFile = File(...),
    back: UploadFile = File(...),
    left: UploadFile = File(...),
    right: UploadFile = File(...),
    top: UploadFile = File(...),
    bottom: UploadFile = File(...)
):
    job_id = str(uuid.uuid4())
    job_path = os.path.join(UPLOAD_DIR, job_id)
    os.makedirs(job_path, exist_ok=True)
    
    # 1. Guardar las 6 imágenes
    images = {"front": front, "back": back, "left": left, "right": right, "top": top, "bottom": bottom}
    for name, file in images.items():
        with open(f"{job_path}/{name}.png", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    try:
        # 2. Ejecutar la inferencia de Hunyuan3D
        # Ajustamos el comando según la estructura de Hunyuan3D-2.1
        # Usamos subprocess para llamar al script de entrada del modelo
        input_vips = f"{job_path}/front.png" # El modelo suele tomar una principal y busca las demás
        output_model = f"{OUTPUT_DIR}/{job_id}.obj"
        
        command = [
            "python3", "main.py", 
            "--image_path", f"{job_path}/front.png", # Punto de entrada
            "--output_dir", OUTPUT_DIR,
            "--save_name", job_id,
            "--use_pbr" # Para alta calidad con tu RTX 4080
        ]
        
        # Ejecutamos el proceso (esto consumirá tu GPU)
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error en Hunyuan3D: {result.stderr}")

        # 3. Retornar el archivo generado (.obj o .glb)
        return FileResponse(
            path=f"{OUTPUT_DIR}/{job_id}/mesh.obj", 
            filename=f"model_{job_id}.obj",
            media_type='application/octet-stream'
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)