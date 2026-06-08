import tempfile
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
import torch
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="InstantMesh API", version="1.0", docs_url="/docs")
device = "cuda" if torch.cuda.is_available() else "cpu"

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("/app/static/index.html") as f:
        return f.read()

@app.post("/generate-3d/")
async def generate_3d(file: UploadFile = File(...)):
    return {"status": "ok", "message": "Modelo cargándose..."}

@app.get("/health")
async def health():
    return {"status": "ok"}
