FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    build-essential cmake ninja-build \
    libgl1 libglib2.0-0 git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar PyTorch con CUDA
RUN pip3 install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu124

# Instalar dependencias
RUN pip3 install --no-cache-dir fastapi uvicorn python-multipart Pillow trimesh diffusers transformers accelerate einops omegaconf

# Compilar torchmcubes (AHORA CON g++ y cmake)
RUN pip3 install --no-cache-dir git+https://github.com/tatsy/torchmcubes.git

# Clonar TripoSR
RUN git clone https://github.com/VAST-AI-Research/TripoSR.git /tmp/triposr && \
    cp -r /tmp/triposr/tsr /app/tsr && \
    rm -rf /tmp/triposr

COPY ./api_server.py /app/
COPY ./static /app/static

EXPOSE 8000
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
