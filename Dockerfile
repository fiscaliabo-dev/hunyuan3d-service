FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar PyTorch 2.3.0 (estable, sin Conda)
RUN pip3 install --no-cache-dir torch==2.3.0 torchvision==0.18.0 --index-url https://download.pytorch.org/whl/cu121

# Instalar dependencias
RUN pip3 install --no-cache-dir \
    "numpy<2" \
    scipy \
    scikit-image \
    pymeshlab \
    trimesh \
    "transformers<4.45" \
    fastapi \
    uvicorn \
    python-multipart \
    Pillow \
    opencv-python \
    einops \
    omegaconf \
    huggingface_hub \
    diffusers \
    peft \
    accelerate \
    safetensors \
    jaxtyping

COPY ./Hunyuan3D-2 /app/Hunyuan3D-2
COPY ./api_server.py /app/
COPY ./static /app/static

RUN cd /app/Hunyuan3D-2 && pip3 install --no-cache-dir --no-deps -e .
RUN mkdir -p /app/checkpoints

ENV PYTHONPATH=/app/Hunyuan3D-2
EXPOSE 8000
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
