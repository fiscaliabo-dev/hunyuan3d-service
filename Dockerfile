FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y python3 python3-pip libgl1 libglib2.0-0 git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip3 install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu124
RUN pip3 install --no-cache-dir fastapi uvicorn python-multipart Pillow trimesh diffusers transformers accelerate
RUN git clone https://github.com/TencentARC/InstantMesh.git /app/InstantMesh
RUN pip3 install --no-cache-dir -r /app/InstantMesh/requirements.txt
COPY ./api_server.py /app/
COPY ./static /app/static
ENV PYTHONPATH=/app/InstantMesh
EXPOSE 8000
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
