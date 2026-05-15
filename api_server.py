import tempfile, os, base64
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from PIL import Image
import replicate

app = FastAPI(
    title="Hunyuan3D-2.1 API",
    description="Generación de modelos 3D - Siempre disponible",
    version="2.0.0",
    docs_url="/docs",
)

REPLICATE_TOKEN = os.environ.get("REPLICATE_TOKEN", "")
if REPLICATE_TOKEN:
    replicate.Client(api_token=REPLICATE_TOKEN)

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("/app/static/index.html") as f:
        return f.read()

@app.post("/generate-3d/")
async def generate_3d(file: UploadFile = File(...)):
    if not REPLICATE_TOKEN:
        return JSONResponse(
            {"error": "Token de Replicate no configurado"},
            status_code=500
        )
    
    with tempfile.TemporaryDirectory() as tmp:
        # Guardar imagen
        img = Image.open(file.file).convert("RGB")
        img_path = Path(tmp) / "input.png"
        img.save(img_path)
        
        # Subir a Replicate
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        
        # Llamar a la API de Replicate
        try:
            output = replicate.run(
                "tencent/hunyuan3d-2.1:model_hash",
                input={"image": f"data:image/png;base64,{data}"}
            )
            
            if output:
                # Descargar resultado
                import requests
                r = requests.get(output)
                out_path = Path(tmp) / "model.glb"
                with open(out_path, "wb") as f:
                    f.write(r.content)
                return FileResponse(str(out_path), filename="model.glb")
            
            return JSONResponse({"error": "No se pudo generar"}, status_code=500)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/health")
async def health():
    return {"status": "ok", "provider": "Replicate"}