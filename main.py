from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Asignar la clave de API directamente en el código
GROQ_API_KEY = "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"


# Ruta para verificar si el servicio está activo
@app.get("/")
def read_root():
    return {"message": "API de FastAPI con Groq está en funcionamiento"}

# Ruta para interactuar con Groq
@app.post("/groq")
def interact_with_groq(query: str):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Clave de API de Groq no configurada.")
    
    try:
        # Configurar la URL y los encabezados de la API de Groq
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        groq_api_url = "https://console.groq.com/keys"  # Cambia esta URL según la documentación de Groq
        response = requests.post(groq_api_url, json={"query": query}, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al conectar con Groq.")
        
        response_data = response.json()
        return {"response": response_data.get("result", "No hay respuesta disponible")}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con Groq: {e}")
