import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import random
import os

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images

def get_image_paths(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
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

def generate_random_15_digit_number():
    return random.randint(100000000000000, 999999999999999)


json_selector = 'selector.json'
with open(json_selector, 'r', encoding='utf-8') as json_file:
    dataselector = json.load(json_file)

def selector(persons_path, id):
    dataselector["5"]["inputs"]["image"] = persons_path
    dataselector["32"]["inputs"]["output_path"] = f"persona_{id}"
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    """
    images = get_images(ws, dataselector)
    for image_data in images["32"]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.show()
    """
    images_paths = get_image_paths(ws, dataselector)
    return images_paths["32"]

json_file_path = 'text2image.json'
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

def call_text_to_imagen(prompt,id):
    data["1"]["inputs"]["seed"] = id   
    data["3"]["inputs"]["text"] = prompt
    data["9"]["inputs"]["output_path"] = f"image_{id}"

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    
    
    """
    images = get_images(ws, data)
    for image_data in images["9"]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.show()
    """
    images_paths = get_image_paths(ws, data)
    return images_paths["9"]

json_cambio= 'cambio_persona2.json'
with open(json_cambio, 'r', encoding='utf-8') as json_file:
    datacambio = json.load(json_file)

def convertir_ruta_formato_windows(ruta_original):
    # Partes fijas de la ruta deseada
    directorio_base = "C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\"
    
    # Extrae el identificador de la imagen y el nombre del archivo de la ruta original
    partes_ruta = ruta_original.split('/')
    identificador_imagen = partes_ruta[0]
    nombre_archivo = partes_ruta[1]
    
    # Construye la nueva ruta con el formato deseado
    ruta_final = f"{directorio_base}{identificador_imagen}\\{nombre_archivo}"
    
    return ruta_final

def call_imagen_to_imagen(image_path,prompt,id):
    
    
    negative_prompt = "deformed, naked,White and black ,watermarks,text, bad quality, low quality"

    datacambio["3"]["inputs"]["seed"] = id
    datacambio["4"]["inputs"]["ckpt_name"] = "Proteus-RunDiffusion.safetensors"
    datacambio["13"]["inputs"]["image"] = image_path
    datacambio["74"]["inputs"]["image"] = r"C:\Users\jairc\Downloads\face\pose1.png"
    datacambio["39"]["inputs"]["text"] = prompt
    datacambio["40"]["inputs"]["text"] = negative_prompt

    datacambio["102"]["inputs"]["output_path"] = f"persona_{id}"

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    """
       images = get_images(ws, datacambio)
    for image_data in images["102"]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.show()
    """
    images_paths = get_image_paths(ws, datacambio)
    return images_paths

jsonbackground = 'background-uno2.json'
with open(jsonbackground, 'r', encoding='utf-8') as json_file:
    databackground = json.load(json_file)

def call_background(img_path,prompt,id):
    negative_prompt = "deformed, naked,White and black ,watermarks,text, bad quality, low quality"

    databackground["33"]["inputs"]["noise_seed"] = id    
    databackground["4"]["inputs"]["image"] = img_path["1"]
    databackground["35"]["inputs"]["text"] = negative_prompt
    databackground["162"]["inputs"]["text"] = prompt
    #databackground["86"]["inputs"]["text"] = " "
    #databackground["87"]["inputs"]["text"] = " "
    databackground["161"]["inputs"]["output_path"] = f"persona_{id}"

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    
    
    """
    images = get_images(ws, databackground)
    for image_data in images["161"]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.show()
    """
    images_paths = get_image_paths(ws, databackground)
    return images_paths["161"]

jsonbackground2 = 'background-dos.json'
with open(jsonbackground2, 'r', encoding='utf-8') as json_file:
    databackground2 = json.load(json_file)

def call_background2(img_path,prompt,id):
    negative_prompt = "deformed, naked,White and black ,watermarks,text, bad quality, low quality"

    
    databackground2["33"]["inputs"]["noise_seed"] = id    
    databackground2["163"]["inputs"]["image"] = img_path["1"]
    databackground2["165"]["inputs"]["image"] = img_path["2"]
    databackground2["35"]["inputs"]["text"] = negative_prompt
    databackground2["162"]["inputs"]["text"] = prompt
    #data["86"]["inputs"]["text"] = " "
    #data["87"]["inputs"]["text"] = " "
    databackground2["161"]["inputs"]["output_path"] = f"persona_{id}"

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    
    
    """
    images = get_images(ws, databackground2)
    for image_data in images["161"]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.show()
    """
    images_paths = get_image_paths(ws, databackground2)
    return images_paths["161"]

jsonbackground3 = 'background-tres.json'
with open(jsonbackground3, 'r', encoding='utf-8') as json_file:
    databackground3 = json.load(json_file)

def call_background3(img_path,prompt,id):
    negative_prompt = "deformed, naked,White and black ,watermarks,text, bad quality, low quality"

    
    databackground3["33"]["inputs"]["noise_seed"] = id    
    databackground3["163"]["inputs"]["image"] = img_path["1"]
    databackground3["164"]["inputs"]["image"] = img_path["2"]
    databackground3["174"]["inputs"]["image"] = img_path["3"]
    databackground3["35"]["inputs"]["text"] = negative_prompt
    databackground3["162"]["inputs"]["text"] = prompt
    #data["86"]["inputs"]["text"] = " "
    #data["87"]["inputs"]["text"] = " "
    databackground3["161"]["inputs"]["output_path"] = f"persona_{id}"

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    
    
    """
    images = get_images(ws, databackground3)
    for image_data in images["161"]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.show()
    """
    images_paths = get_image_paths(ws, databackground3)
    return images_paths["161"]


jsonbackground4 = 'cuatro.json'
with open(jsonbackground4, 'r', encoding='utf-8') as json_file:
    databackground4 = json.load(json_file)

def call_background4(img_path,prompt,id):
    negative_prompt = "deformed, naked,White and black ,watermarks,text, bad quality, low quality"

    
    databackground4["33"]["inputs"]["noise_seed"] = id    
    databackground4["163"]["inputs"]["image"] = img_path["1"]
    databackground4["164"]["inputs"]["image"] = img_path["2"]
    databackground4["174"]["inputs"]["image"] = img_path["3"]
    databackground4["183"]["inputs"]["image"] = img_path["4"]
    databackground4["35"]["inputs"]["text"] = negative_prompt
    databackground4["162"]["inputs"]["text"] = prompt
    #data["86"]["inputs"]["text"] = " "
    #data["87"]["inputs"]["text"] = " "
    databackground4["161"]["inputs"]["output_path"] = f"persona_{id}"

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    
    
    """
    images = get_images(ws, databackground4)
    for image_data in images["161"]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.show()
    """
    images_paths = get_image_paths(ws, databackground4)
    return images_paths["161"]



if __name__ == "__main__":
    prompt="Ultra realistic photography of a full-body elegant young mexican man, looking at the camera, in shape, suit, elegant, VERY VERY SHORT black hair, messy short hair, ID photo, work, cinematic, 4K shot on X2D 100C, XCD4/45P lens 17mm"
    id=generate_random_15_digit_number()
    #path=call_text_to_imagen(prompt,id)
    #print(path[0])
    
    """
     for n in personas:
        directorio_final = convertir_ruta_formato_windows(n)
        print(f"Convirtiendo {n} a ruta de Windows: {directorio_final}")
        
        try:
            a = call_imagen_to_imagen(directorio_final, prompt, id)
            print(f"Rutas de las imágenes procesadas: {a}")
        except Exception as e:
            print(f"Error al procesar la imagen {n}: {e}")

    """
    persons=r"C:\Users\jairc\Downloads\ComfyUI_temp_gehnl_00009_.png"
    personas=selector(persons, id)
    print(len(personas))
    print(personas)
    

    img="persona_242267221906646/persona_0001.png"
    final_img=convertir_ruta_formato_windows(img)
    cambio=call_imagen_to_imagen(final_img,prompt,id)
    print(cambio)
    
    
    



    
