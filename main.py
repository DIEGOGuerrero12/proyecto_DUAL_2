import requests
import json

API_KEY = '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'
url = "https://api.groq.com/openai/v1/chat/completions"

def respuesta_ia(texto: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": "Actúa como un asistente virtual."
            },
            {
                "role": "user",
                "content": texto
            }
        ],
        "model": "mixtral-8x7b-32768",
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": False,
        "stop": None
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        response_data = response.json()

        # Verificar si la respuesta contiene los datos esperados
        if 'choices' in response_data and response_data['choices']:
            return response_data['choices'][0]['message']['content']
        else:
            # Registrar toda la respuesta en caso de que falten los datos esperados
            return f"Respuesta inesperada de la API: {response_data}"

    except requests.exceptions.RequestException as e:
        return f"Error en la solicitud HTTP: {e}"
    except json.JSONDecodeError:
        return "Error al decodificar la respuesta JSON de la API"
    except KeyError:
        return "Error: La respuesta de la API no contiene las claves esperadas"
