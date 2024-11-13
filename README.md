## 0. Actualizar la lista de versiones de las librerias del sistema operativo

Actualiza la lista de versiones de libreias del sistema operativo.

````bash
sudo apt update
````

## 1. Instalar neofetch 

Instalar neofetch para conocer las caracteristicas del sistema operativo que se esta utilizando.

````bash
sudo apt install neofetch -y
````

## 2. Ejecutar neofetch

Ejecutar neofetch

````bash
neofetch
````

Nota: Crear el archivo os.txt con la versión del sistema operativo utilizado

## 3. Crear un ambiente virtual

Crear un virtual enviroment para el proyecto

````bash
virtualenv venv
````

## 4. Entrar al ambiente virtual

Inicializar el ambiente virtual

````bash
source venv/bin/activate
````

## 5. Salir del ambiente virtual

Desactivar el ambiente virtual

````bash
deactivate
````

## 6. Crear el archivo .gitignore

Crear el arhvivo .gitignore y agregar las siguientes lineas

````bash
*.pyc
__pycache__/
venv/
````

## 7. Instalar las librerias necesarias 

Para este proyecto se usaran las librerias de [FastAPI](https://fastapi.tiangolo.com/#installation)

````bash
pip install "fastapi[standard]"
````

## 8. Crear el archivo requirements.txt

Se genera el archivo requirements.txt para listar las librerias necesarias para el proyecto y sus versiones.

````bash
pip freeze > requirements.txt
````

## 9. Crear el archivo runtime

Se genera el archivo runtime con la versión de Python que se esta utilizando

````bash
python3 -V > runtime
````

## Se realizan las importaciones necesarias.
````bash
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import logging
````

## Configuración de registros para depuración
````bash
logging.basicConfig(level=logging.INFO)
````

## Cargar variables de entorno desde el archivo .env
````bash
load_dotenv()
````

## Crea una instancia de FastAPI
````bash
Que es la aplicación principal para el servidor web.
````bash
app = FastAPI()
````

## Asignar la clave de API desde las variables de entorno
````bash
API_KEY = os.getenv("GROQ_API_KEY", "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")
url = "https://api.groq.com/openai/v1/chat/completions"
````

## Endpoint raíz
````bash
@app.get("/")
def read_root():
    return {"message": "API de FastAPI con Groq está en funcionamiento"}
````

## Endpoint /groq/{query} para Consultar la API de Groq
Define el endpoint /groq/{query}, que recibe un parámetro query (consulta principal) y un parámetro opcional additional_query.
````bash
@app.get("/groq/{query}")
def interact_with_groq(query: str, additional_query: str = None):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Clave de API de Groq no configurada.")
````

## Define los encabezados HTTP de la solicitud. Usa Bearer en el encabezado Authorization para autenticarse con la clave API.
````bash
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
````
## Crea la lista messages, que incluye mensajes para enviar a Groq.
````bash
        messages = [
            {"role": "system", "content": "Actúa como un asistente virtual."},
            {"role": "user", "content": query}
        ]
        
        if additional_query:
            messages.append({"role": "user", "content": additional_query})
````

## Crea el data con el modelo, configurando la temperatura, el límite de tokens y otras opciones de respuesta para Groq.
````bash
        data = {
            "messages": messages,
            "model": "mixtral-8x7b-32768",
            "temperature": 1,
            "max_tokens": 1024,
            "top_p": 1,
            "stream": False,
            "stop": None
        }
````
## Envía la solicitud POST a Groq y registra la respuesta completa para depuración.
````bash
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        logging.info("Respuesta completa de Groq: %s", response_data)  # Log de la respuesta completa
````

## Verifica que choices esté presente en la respuesta de Groq. Si falta, lanza un error HTTP 500.
````bash
        if "choices" not in response_data or not response_data["choices"]:
            raise HTTPException(status_code=500, detail="La API de Groq no devolvió resultados.")
````

## Extrae el contenido de la respuesta y lo devuelve en un diccionario JSON con la clave response.
````bash
        conversational_response = response_data['choices'][0]['message']['content']
        return {"response": conversational_response}
````

## Si ocurre un error en la solicitud HTTP, lanza un error HTTP 500 con un mensaje personalizado.
````bash
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con Groq: {e}")
````

## Middleware de CORS
Importa y configura el middleware CORS, permitiendo todas las fuentes, métodos y encabezados para que la API acepte solicitudes de cualquier origen. Puedes restringir estos permisos si es necesario.
````bash
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes; ajusta esto si es necesario.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
````