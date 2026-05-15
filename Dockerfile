FROM python:3.11-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev curl

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn python-multipart pillow replicate

COPY ./api_server.py /app/
COPY ./static /app/static

EXPOSE 8000
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]