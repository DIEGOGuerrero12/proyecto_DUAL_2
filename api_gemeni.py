from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from google.oauth2 import service_account
from google.cloud import aiplatform
from dotenv import load_dotenv
import logging

# Configuración de registros para depuración
logging.basicConfig(level=logging.INFO)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Configurar la cuenta de servicio y el proyecto
API_KEY = os.getenv("AIzaSyAPg7NIPczoP0eZtYWlht1kc9rFtS3_GfE")
PROJECT_ID = os.getenv("https://aistudio.google.com/app/apikey")
LOCATION = "us-central1"  # Cambia la región si es necesario

# Inicializar Vertex AI con el proyecto y las credenciales
aiplatform.init(project=PROJECT_ID, location=LOCATION)

@app.get("/")
def read_root():
    return {"message": "API de FastAPI con Google Gemini está en funcionamiento"}

@app.get("/gemini/{query}")
def interact_with_gemini(query: str, additional_query: str = None):
    try:
        # Configura el endpoint de Vertex AI y llama al modelo
        client = aiplatform.gapic.PredictionServiceClient()
        endpoint = client.endpoint_path(project=PROJECT_ID, location=LOCATION, endpoint="<YOUR_ENDPOINT_ID>")

        instances = [
            {"content": query},
        ]
        if additional_query:
            instances.append({"content": additional_query})

        parameters = {
            "temperature": 1,
            "max_tokens": 1024,
            "top_p": 1,
        }

        response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
        
        # Extrae la respuesta
        conversational_response = response.predictions[0]["content"]
        return {"response": conversational_response}

    except Exception as e:
        logging.error("Error al conectar con Gemini: %s", e)
        raise HTTPException(status_code=500, detail=f"Error al conectar con Gemini: {e}")
