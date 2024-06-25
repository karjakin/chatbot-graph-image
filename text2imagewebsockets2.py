import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import random
import os

# Configuración inicial
server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())
ws = None  # WebSocket global


def create_websocket_connection():
    global ws
    if ws is None:
        ws = websocket.WebSocket()
        ws.connect(f"ws://{server_address}/ws?clientId={client_id}")
        print("Conexión WebSocket creada")

# Funciones de utilidad para interactuar con el servidor
def queue_prompt(prompt, ws):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        history = json.loads(response.read())
        #print("Historial completo:", history)  
        return history

# Funciones principales de procesamiento de imágenes
def get_image_paths(ws, prompt):
    prompt_id = queue_prompt(prompt,WindowsError)['prompt_id']
    output_image_paths = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break  # Execution is done
        else:
            continue  # previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_path = f"{image['subfolder']}/{image['filename']}"  # Assuming this is the desired format
                    images_output.append(image_path)
            output_image_paths[node_id] = images_output

    return output_image_paths
# Función para convertir la ruta de imagen en formato compatible con Windows
def convertir_ruta_formato_windows(ruta_original):
    directorio_base = "C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\"
    identificador_imagen, nombre_archivo = ruta_original.split('/')
    ruta_final = f"{directorio_base}{identificador_imagen}\\{nombre_archivo}"
    return ruta_final

def generate_random_15_digit_number():
    return random.randint(100000000000000, 999999999999999)

# Crear una conexión WebSocket centralizada

   


def selector(persons_path, id):
    with open('selector.json', 'r', encoding='utf-8') as json_file:
        dataselector = json.load(json_file)
    dataselector["5"]["inputs"]["image"] = persons_path
    dataselector["32"]["inputs"]["output_path"] = f"persona_{id}"
    images_paths = get_image_paths(ws, dataselector)
    return images_paths["32"]

def call_text_to_imagen(prompt, id):
    with open('text2image.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    data["1"]["inputs"]["seed"] = id   
    data["3"]["inputs"]["text"] = prompt
    data["9"]["inputs"]["output_path"] = f"image_{id}"
    images_paths = get_image_paths(ws, data)
    return images_paths["9"]

def call_imagen_to_imagen(image_path, prompt, id):
    with open('cambio_persona2.json', 'r', encoding='utf-8') as json_file:
        datacambio = json.load(json_file)
    negative_prompt = "deformed, naked,White and black ,watermarks,text, bad quality, low quality"
    datacambio["3"]["inputs"]["seed"] = id
    datacambio["4"]["inputs"]["ckpt_name"] = "Proteus-RunDiffusion.safetensors"
    datacambio["13"]["inputs"]["image"] = image_path
    datacambio["74"]["inputs"]["image"] = r"C:\Users\jairc\Downloads\face\pose1.png"
    datacambio["39"]["inputs"]["text"] = prompt
    datacambio["40"]["inputs"]["text"] = negative_prompt
    datacambio["102"]["inputs"]["output_path"] = f"persona_{id}"
    images_paths = get_image_paths(ws, datacambio)
    return images_paths["102"]

def call_background(img_path, prompt, id):
    with open('background-uno2.json', 'r', encoding='utf-8') as json_file:
        databackground = json.load(json_file)
    negative_prompt = "deformed, naked,White and black, watermarks, text, bad quality, low quality"
    databackground["33"]["inputs"]["noise_seed"] = id
    databackground["4"]["inputs"]["image"] = img_path[0]
    databackground["35"]["inputs"]["text"] = negative_prompt
    databackground["162"]["inputs"]["text"] = prompt
    databackground["161"]["inputs"]["output_path"] = f"persona_{id}"
    images_paths = get_image_paths(ws, databackground)
    return images_paths["161"]

def call_background2(img_path, prompt, id):
    with open('background-dos.json', 'r', encoding='utf-8') as json_file:
        databackground2 = json.load(json_file)
    negative_prompt = "deformed, naked,White and black, watermarks, text, bad quality, low quality"
    databackground2["33"]["inputs"]["noise_seed"] = id
    databackground2["163"]["inputs"]["image"] = img_path[0]
    databackground2["165"]["inputs"]["image"] = img_path[1]
    databackground2["35"]["inputs"]["text"] = negative_prompt
    databackground2["162"]["inputs"]["text"] = prompt
    databackground2["161"]["inputs"]["output_path"] = f"persona_{id}"
    images_paths = get_image_paths(ws, databackground2)
    return images_paths["161"]

def call_background3( img_path, prompt, id):
    with open('background-tres.json', 'r', encoding='utf-8') as json_file:
        databackground3 = json.load(json_file)
    negative_prompt = "deformed, naked,White and black, watermarks, text, bad quality, low quality"
    databackground3["33"]["inputs"]["noise_seed"] = id
    databackground3["163"]["inputs"]["image"] = img_path[0]
    databackground3["164"]["inputs"]["image"] = img_path[1]
    databackground3["174"]["inputs"]["image"] = img_path[2]
    databackground3["35"]["inputs"]["text"] = negative_prompt
    databackground3["162"]["inputs"]["text"] = prompt
    databackground3["161"]["inputs"]["output_path"] = f"persona_{id}"
    images_paths = get_image_paths(ws, databackground3)
    return images_paths["161"]

def call_background4(img_path, prompt, id):
    with open('cuatro.json', 'r', encoding='utf-8') as json_file:
        databackground4 = json.load(json_file)
    negative_prompt = "deformed, naked,White and black, watermarks, text, bad quality, low quality"
    databackground4["33"]["inputs"]["noise_seed"] = id
    databackground4["163"]["inputs"]["image"] = img_path[0]
    databackground4["164"]["inputs"]["image"] = img_path[1]
    databackground4["174"]["inputs"]["image"] = img_path[2]
    databackground4["183"]["inputs"]["image"] = img_path[3]
    databackground4["35"]["inputs"]["text"] = negative_prompt
    databackground4["162"]["inputs"]["text"] = prompt
    databackground4["161"]["inputs"]["output_path"] = f"persona_{id}"
    images_paths = get_image_paths(ws, databackground4)
    return images_paths["161"]

def dividir_y_aplicar_fondo(img_paths, prompt, id):
    
    longitud=len(img_paths)

    if longitud == 1:
        background=call_background( img_paths, prompt, id)
        return background

    elif longitud == 2:
        background=call_background2( img_paths, prompt, id)
        return background
    elif longitud == 3:
        background=call_background3( img_paths, prompt, id)
        return background
    elif longitud >= 4:
        # Si hay 4 o más, solo se procesan 4 debido a la limitación a fondo_cuatro
        selected_img_paths = img_paths[:4]
        print(selected_img_paths)  # Selecciona solo los primeros 4 si hay más

        background=call_background4( selected_img_paths, prompt, id)
        return background
    else:
        print("Número de imágenes no soportado.")

def full_image_to_image(img_path,prompt,promptf,id):

        personas=selector(img_path, id)
        print(len(personas))
        print(personas)
        cambios=[]
        for n in personas:
            directorio_final = convertir_ruta_formato_windows(n)
            print(f"Convirtiendo {n} a ruta de Windows: {directorio_final}")
            print("-----")
            try:
                a = call_imagen_to_imagen(directorio_final, prompt, id)
                print(a[0])
                cambios.append(a[0])
            except Exception as e:
                print(f"Error al procesar la imagen {n}: {e}")
        print(cambios) 
        cambios2=[]
        for n in cambios:
            new_path=convertir_ruta_formato_windows(n)   
            cambios2.append(new_path)
        print(cambios2)
        fondo=dividir_y_aplicar_fondo(cambios2, promptf, id)
        print(fondo[0])
        return fondo[0]

# Ejemplo de uso en el bloque principal
if __name__ == "__main__":
    create_websocket_connection()
    prompt = "Batman made outfit, full-body image (gears, wires, mechanical, electronics). PCB hyper-realistic, futuristic, stunning Unreal Engine render 5, product photography HDR 8k, hyper-realistic, high-quality model, ultra-sharp focus, golden ratio, diamond eyes, ultra-detail cinematic."
    id = generate_random_15_digit_number()
    persons=r"C:\Users\jairc\Downloads\ComfyUI_temp_gehnl_00009_.png"
    promptf="A photo of a landscape of a city similar to New York. Show skyscrapers but also skateparks around the area. The city is cool. The architecture is mid-century modern, but also some more run-down buildings in lower-class areas."
    final=full_image_to_image(persons,prompt,promptf,id)
    print(final)





    