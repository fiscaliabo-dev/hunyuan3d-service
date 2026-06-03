import tempfile
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
import torch
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TripoSR API", version="1.0", docs_url="/docs")

device = "cuda" if torch.cuda.is_available() else "cpu"

# Cargar modelo
from tsr.system import TSR
model = TSR.from_pretrained("stabilityai/TripoSR", device=device)
logger.info("✅ TripoSR cargado")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("/app/static/index.html") as f:
        return f.read()

@app.post("/generate-3d/")
async def generate_3d(file: UploadFile = File(...)):
    with tempfile.TemporaryDirectory() as tmp:
        img = Image.open(file.file).convert("RGB")
        path = Path(tmp) / "input.png"
        img.save(path)
        
        scene_codes = model([str(path)], device=device)
        mesh = model.extract_mesh(scene_codes[0])
        
        out = Path(tmp) / "model.glb"
        mesh.export(str(out))
        
        return FileResponse(str(out), filename="model.glb")

@app.get("/health")
async def health():
    return {"status": "ok"}
