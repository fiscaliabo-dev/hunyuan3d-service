"""
Descargar modelos pre-entrenados de Hunyuan3D-2.1
"""
import os
from huggingface_hub import snapshot_download

MODEL_DIR = "/app/checkpoints/hunyuan3d-2.1"
os.makedirs(MODEL_DIR, exist_ok=True)

print("📥 Descargando modelos de Hunyuan3D-2.1...")
print("   (esto puede tardar 10-20 minutos, los modelos pesan ~5 GB)")

try:
    snapshot_download(
        repo_id="tencent/Hunyuan3D-2.1",
        local_dir=MODEL_DIR,
        ignore_patterns=["*.md", "*.txt"],
        resume_download=True
    )
    print("✅ Modelos descargados correctamente")
except Exception as e:
    print(f"❌ Error descargando modelos: {e}")
    print("\n⚠️  Alternativa manual:")
    print("   git lfs install")
    print("   git clone https://huggingface.co/tencent/Hunyuan3D-2.1")