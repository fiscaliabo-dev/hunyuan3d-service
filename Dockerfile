FROM fiscaliabo/spann3r-3d:latest

WORKDIR /app

# Instalar transformers compatible con PyTorch 2.6
RUN pip install --no-cache-dir "transformers==4.45.0"

# Instalar dependencias adicionales
RUN pip install --no-cache-dir scikit-image pymeshlab trimesh diffusers peft accelerate safetensors jaxtyping omegaconf einops

COPY ./Hunyuan3D-2 /app/Hunyuan3D-2
COPY ./api_server.py /app/
COPY ./static /app/static

RUN cd /app/Hunyuan3D-2 && pip install --no-cache-dir --no-deps -e .
RUN mkdir -p /app/checkpoints

ENV PYTHONPATH=/app/Hunyuan3D-2
EXPOSE 8000
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
