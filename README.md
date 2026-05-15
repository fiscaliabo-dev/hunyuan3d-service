# Hunyuan3D-2.1 - Generador de Modelos 3D

Genera modelos 3D completos (malla + textura) a partir de **una sola imagen**.

## 🚀 Inicio rápido

```bash
# 1. Clonar
git clone <repo-url> -b hunyuan3d
cd hunyuan3d-service

# 2. Descargar modelos (5 GB, solo primera vez)
python download_models.py

# 3. Iniciar
docker compose up -d

# 4. Abrir
http://localhost:8002