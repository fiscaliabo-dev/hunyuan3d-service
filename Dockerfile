FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip3 install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu124
RUN pip3 install --no-cache-dir "numpy<2" scipy scikit-image transformers fastapi uvicorn python-multipart Pillow
RUN pip3 install --no-cache-dir trimesh opencv-python einops omegaconf huggingface_hub
RUN pip3 install --no-cache-dir diffusers peft accelerate safetensors jaxtyping

COPY ./Hunyuan3D-2 /app/Hunyuan3D-2
COPY ./api_server.py /app/
COPY ./static /app/static

RUN cd /app/Hunyuan3D-2 && pip3 install --no-cache-dir --no-deps -e .
RUN mkdir -p /app/checkpoints

ENV PYTHONPATH=/app/Hunyuan3D-2
EXPOSE 8000
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
