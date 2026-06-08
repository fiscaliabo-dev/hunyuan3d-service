FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn python-multipart Pillow trimesh diffusers transformers accelerate einops omegaconf
RUN pip install --no-cache-dir git+https://github.com/tatsy/torchmcubes.git

# Clonar TripoSR y copiar solo el código
RUN git clone https://github.com/VAST-AI-Research/TripoSR.git /tmp/triposr && \
    cp -r /tmp/triposr/tsr /app/tsr && \
    rm -rf /tmp/triposr
# Instalar dependencias de TripoSR
RUN pip install --no-cache-dir diffusers transformers accelerate

COPY ./api_server.py /app/
COPY ./static /app/static

EXPOSE 8000
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
