FROM fiscaliabo/spann3r-3d:latest

WORKDIR /app

# Instalar solo lo adicional que necesita Hunyuan3D
RUN pip install --no-cache-dir scikit-image pymeshlab diffusers peft accelerate safetensors jaxtyping omegaconf

COPY ./Hunyuan3D-2 /app/Hunyuan3D-2
COPY ./api_server.py /app/
COPY ./static /app/static

RUN cd /app/Hunyuan3D-2 && pip install --no-cache-dir --no-deps -e .
RUN mkdir -p /app/checkpoints

ENV PYTHONPATH=/app/Hunyuan3D-2
EXPOSE 8000
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
