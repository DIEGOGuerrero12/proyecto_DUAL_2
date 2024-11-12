from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import logging

# Configuración de registros para depuración
logging.basicConfig(level=logging.INFO)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Asignar la clave de API desde las variables de entorno
API_KEY = os.getenv("GROQ_API_KEY", "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")
url = "https://api.groq.com/openai/v1/chat/completions"

@app.get("/")
def read_root():
    return {"message": "API de FastAPI con Groq está en funcionamiento"}

@app.get("/groq/{query}")
def interact_with_groq(query: str, additional_query: str = None):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Clave de API de Groq no configurada.")

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        messages = [
            {"role": "system", "content": "Actúa como un asistente virtual."},
            {"role": "user", "content": query}
        ]
        
        if additional_query:
            messages.append({"role": "user", "content": additional_query})
        
        data = {
            "messages": messages,
            "model": "mixtral-8x7b-32768",
            "temperature": 1,
            "max_tokens": 1024,
            "top_p": 1,
            "stream": False,
            "stop": None
        }

        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        logging.info("Respuesta completa de Groq: %s", response_data)  # Log de la respuesta completa
        
        if "choices" not in response_data or not response_data["choices"]:
            raise HTTPException(status_code=500, detail="La API de Groq no devolvió resultados.")
        
        conversational_response = response_data['choices'][0]['message']['content']
        return {"response": conversational_response}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con Groq: {e}")
