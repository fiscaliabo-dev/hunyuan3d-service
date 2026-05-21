import replicate, requests, os

REPLICATE_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=REPLICATE_TOKEN)

image_path = "/work/pruebas/vista1.png"

# Intentar varios nombres de modelo
MODELOS = [
    "tencent/hunyuan3d-2.1",
    "tencent/hunyuan3d-2",
    "tencent/hunyuan-3d-2.1",
    "cjwbw/hunyuan3d-2.1",
    "adirik/hunyuan3d-2.1",
]

for modelo in MODELOS:
    try:
        print(f"Intentando: {modelo}")
        output = client.run(modelo, input={"image": open(image_path, "rb")})
        print(f"✅ Funcionó: {modelo}")
        print(f"   Resultado: {output}")
        if output:
            with open("/work/modelo.glb", "wb") as f:
                f.write(requests.get(output).content)
            print("   ✅ Modelo guardado")
        break
    except Exception as e:
        print(f"   ❌ {e}")
