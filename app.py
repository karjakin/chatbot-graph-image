from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from text2imagewebsockets2 import create_websocket_connection,convertir_ruta_formato_windows
from send import *
from Ollamajson import call_graph
import time
app = FastAPI()

class Message(BaseModel):
    numero: str
    mensaje: str

# Este es el diccionario global para mantener el estado entre solicitudes
estados_usuarios = {}

def extraer_path_archivo(texto):
    # Busca la frase objetivo en el texto
    inicio_frase = "Archivo recibido: "
    inicio = texto.find(inicio_frase)
    
    # Si se encuentra la frase, intenta extraer el path del archivo
    if inicio != -1:
        # Ajusta el índice de inicio para capturar el path después de la frase
        inicio += len(inicio_frase)
        # Asume que el path termina al final del texto o en un espacio si hay más contenido después
        fin = texto.find(" ", inicio)
        fin = fin if fin != -1 else len(texto)
        # Extrae y devuelve el path del archivo
        return texto[inicio:fin]
    else:
        # Devuelve None si la frase objetivo no se encuentra en el texto
        return texto

def extraer_primer_valor(valor):
    if isinstance(valor, list):
        return valor[0] if valor else None
    elif isinstance(valor, str):
        return valor
    else:
        return None

@app.get("/")
def read_root():
    return {"Hello": "World from FastAPI"}

@app.post("/webhook")
def read_webhook(item: Message):
    print(f"Received message from {item.numero}: {item.mensaje}")
    numero_usuario = item.numero.replace("@c.us", "")

    # Aquí, asegúrate de obtener correctamente el estado actual para este usuario
    estado_actual = estados_usuarios.get(numero_usuario, {})

    print("user:")
    print(item.mensaje)
    fix_mensaje=extraer_path_archivo(item.mensaje)
    print(fix_mensaje)

    # Suponiendo que call_graph ahora devuelve el nuevo estado junto con la respuesta
    response, nuevo_estado = call_graph(numero_usuario, fix_mensaje, estado_actual)

    # Actualiza el diccionario de estados con el nuevo estado para este usuario
    estados_usuarios[numero_usuario] = nuevo_estado
    
    print("-----")
    print("ai:")
    print(response)
    print("-----")
   
    

    if response and ".png" in response:
        try:
            time.sleep(1)
            send_image(numero_usuario, response)
        except Exception as e:
            print(f"Error al enviar imagen: {e}")
    else:
        try:
            send_message(numero_usuario, response)
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")

    return {"received": True}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
