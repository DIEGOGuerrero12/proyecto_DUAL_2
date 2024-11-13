from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import requests
import os
from dotenv import load_dotenv
import logging
from PIL import Image, ImageFilter
from io import BytesIO
from pathlib import Path

# Configuración de registros para depuración
logging.basicConfig(level=logging.INFO)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Permitir solicitudes de cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Asignar la clave de API desde las variables de entorno
API_KEY = os.getenv("OLLAMA_API_KEY", "your_default_ollama_api_key")
OLLAMA_URL = "https://api.ollama.com/image-processing"  # Supongamos que esta es la URL de la API de Ollama

# Directorio para guardar las imágenes procesadas
PROCESSED_IMAGES_DIR = Path("processed_images")
PROCESSED_IMAGES_DIR.mkdir(exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "API de FastAPI con Ollama está en funcionamiento"}

@app.post("/ollama")
async def process_image(file: UploadFile = File(...)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Clave de API de Ollama no configurada.")

    try:
        # Leer el archivo de imagen
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))

        # Aplicar un filtro a la imagen (por ejemplo, desenfoque)
        filtered_image = image.filter(ImageFilter.BLUR)

        # Guardar la imagen procesada en el directorio
        image_filename = f"processed_{file.filename}"
        image_path = PROCESSED_IMAGES_DIR / image_filename
        filtered_image.save(image_path, format="JPEG")

        # Preparar la solicitud para la API de Ollama
        headers = {
            "Authorization": f"Bearer {API_KEY}",
        }
        files = {
            "file": (image_filename, image_path.open("rb"), "image/jpeg")
        }

        response = requests.post(OLLAMA_URL, headers=headers, files=files)
        response_data = response.json()
        logging.info("Respuesta completa de Ollama: %s", response_data)  # Log de la respuesta completa

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error en la API de Ollama")

        description = response_data.get("description", "No description available")

        return JSONResponse(content={"description": description, "image_url": f"/images/{image_filename}"})

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con Ollama: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la imagen: {e}")

@app.get("/images/{image_filename}")
async def get_image(image_filename: str):
    image_path = PROCESSED_IMAGES_DIR / image_filename
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return FileResponse(image_path)
