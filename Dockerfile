FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir \
    "numpy<2" \
    scipy \
    scikit-image \
    pymeshlab \
    trimesh \
    transformers \
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

RUN cd /app/Hunyuan3D-2 && pip install --no-cache-dir --no-deps -e .
RUN mkdir -p /app/checkpoints

ENV PYTHONPATH=/app/Hunyuan3D-2
EXPOSE 8000
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
