import replicate
import requests

# Configurar token
REPLICATE_TOKEN = "tu_token_aqui"
client = replicate.Client(api_token=REPLICATE_TOKEN)

# Generar modelo
output = client.run(
    "tencent/hunyuan3d-2.1",
    input={"image": open("foto.png", "rb")}
)

# Descargar resultado
with open("modelo.glb", "wb") as f:
    f.write(requests.get(output).content)
print("✅ Modelo guardado")
