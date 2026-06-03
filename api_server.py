import sys, os, tempfile
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from PIL import Image
import torch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.insert(0, "/app/Hunyuan3D-2")

app = FastAPI(title="Hunyuan3D-2.1", version="1.0", docs_url="/docs")

device = "cuda" if torch.cuda.is_available() else "cpu"
CHECKPOINT_DIR = "/app/checkpoints/hunyuan3d-2.1"

logger.info(f"Cargando modelo en {device}...")

from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
    CHECKPOINT_DIR,
    subfolder="hunyuan3d-dit-v2-1",
    vae_subfolder="hunyuan3d-vae-v2-1",
    low_vram_mode=True,
    device=device
    use_safetensors=False 
)
logger.info("Modelo cargado")

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
        mesh = pipeline(image=str(path))[0]
        out = Path(tmp) / "model.obj"
        mesh.export(str(out))
        return FileResponse(str(out), filename="model.obj")

@app.get("/health")
async def health():
    return {"status": "ok"}
