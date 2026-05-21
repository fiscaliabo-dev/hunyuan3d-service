import tempfile, traceback
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from gradio_client import Client, handle_file
from PIL import Image
import sys

app = FastAPI(title="Hunyuan3D API", version="1.0.0", docs_url="/docs")

print("Iniciando servidor...", flush=True)

# Intentar conectar a HuggingFace
try:
    print("Conectando a HuggingFace...", flush=True)
    client = Client("tencent/Hunyuan3D-2.1")
    print("✅ Conectado a HuggingFace", flush=True)
except Exception as e:
    print(f"❌ Error HuggingFace: {e}", flush=True)
    client = None

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("/app/static/index.html") as f:
        return f.read()

@app.post("/generate-3d/")
async def generate_3d(file: UploadFile = File(...)):
    print(f"Recibido archivo: {file.filename}", flush=True)
    
    if client is None:
        return JSONResponse({"error": "Servicio no disponible. HuggingFace está caído."}, status_code=503)
    
    try:
        with tempfile.TemporaryDirectory() as tmp:
            img = Image.open(file.file).convert("RGB")
            path = Path(tmp) / "input.png"
            img.save(path)
            print(f"Imagen guardada: {path}", flush=True)
            
            print("Llamando a HuggingFace...", flush=True)
            result = client.predict(
                input_image=handle_file(str(path)),
                api_name="/predict"
            )
            print(f"Resultado recibido: {type(result)}", flush=True)
            
            if result and result[0]:
                out = Path(tmp) / "model.glb"
                with open(out, "wb") as f:
                    f.write(result[0])
                print(f"Modelo guardado: {out.stat().st_size} bytes", flush=True)
                return FileResponse(str(out), filename="model.glb")
            
            return JSONResponse({"error": "No se pudo generar el modelo"}, status_code=500)
    
    except Exception as e:
        print(f"ERROR: {traceback.format_exc()}", flush=True)
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/health")
async def health():
    return {"status": "ok" if client else "degraded"}