
from urllib import request, error
import json
import random
import os
import time
from face import call_selector
from fondo_uno import fondo_uno
from fondo_dos import fondo_dos
from fondo_tres import fondo_tres
from fondo_cuatro import fondo_cuatro
def monitor_directory(path, threshold, json_output_path):
    while True:
        try:
            # Lista todos los archivos en el directorio
            file_list = os.listdir(path)
            # Cuenta la cantidad de archivos
            file_count = len(file_list)

            print(f"Comprobando... {file_count} archivos encontrados.")  # Imprime la cantidad de archivos actual

            # Si se alcanza o supera el umbral, crea un archivo JSON
            if file_count >= threshold:
                image_data = {f"{i}": os.path.join(path, file) for i, file in enumerate(file_list, start=1)}
                with open(json_output_path, 'w') as json_file:
                    json.dump(image_data, json_file, indent=4)
                
                print(f"Archivo JSON creado con {file_count} elementos.")
                return image_data # Termina el bucle después de crear el archivo JSON
            else:
                print(f"Esperando a alcanzar el umbral de {threshold} archivos...")

            # Espera 10 segundos antes de la próxima comprobación
            time.sleep(20)
        except Exception as e:
            print(f"Error: {e}")
            break

json_file_path = 'cambio_persona2.json'

# Load JSON data from file
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

def queue_prompt(prompt):
    try:
        p = {"prompt": prompt}
        data = json.dumps(p).encode('utf-8')  # Convert the Python dictionary back to a JSON formatted string to send in the request
        req = request.Request("http://127.0.0.1:8188/prompt", data=data)
        with request.urlopen(req) as response:
            print("Request successful, response:", response.read())
    except error.HTTPError as e:
        print('HTTPError: ', e.code, e.reason)
    except error.URLError as e:
        print('URLError: ', e.reason)
    except Exception as e:
        print('Generic Exception: ', e)

def generate_random_15_digit_number():
    return random.randint(100000000000000, 999999999999999)

def json_imagen(json_data,prompt, id, negative_prompt):
  
    negative_prompt

    
    # Create directory
    #dir_path = f'C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\persona_{id}'
    #os.makedirs(dir_path, exist_ok=True)
    #print(f"Directory created at {dir_path}")
    

    for i, image_path in json_data.items():
        
        data["3"]["inputs"]["seed"] = id
        data["4"]["inputs"]["ckpt_name"] = "Proteus-RunDiffusion.safetensors"
        data["13"]["inputs"]["image"] = image_path
        data["74"]["inputs"]["image"] = r"C:\Users\jairc\Downloads\face\pose1.png"
        data["39"]["inputs"]["text"] = prompt
        data["40"]["inputs"]["text"] = negative_prompt

        data["102"]["inputs"]["output_path"] = f"persona_{id}"
        queue_prompt(data)  # Assuming this generates the image and saves it to the specified path

    return "comfyui"


def call_cambio(datos,prompt,id,negative_prompt):

    json_imagen(datos,prompt, id, negative_prompt)
    directory_path = f"C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\persona_{id}"
    json_output_path = "output2.json"
    limite=len(datos) * 2
    
    output=monitor_directory(directory_path,limite,json_output_path)
    return output
def dividir_y_aplicar_fondo(img_paths, prompt, id, neg_prompts, directory_path, json_output_path):
    """
    Divide el diccionario de img_paths por la mitad y aplica un fondo a la primera mitad,
    seleccionando entre fondo_uno, fondo_dos, fondo_tres, o fondo_cuatro basado en la cantidad
    de imágenes en la primera mitad.

    :param img_paths: Diccionario de paths de imágenes.
    :param prompt: Prompt para la generación de la imagen.
    :param id: Identificador único.
    :param neg_prompts: Prompts negativos para evitar en la generación.
    :param directory_path: Directorio donde se guardarán las imágenes procesadas.
    :param json_output_path: Path para el archivo JSON de salida.
    """
    # Calcula el número de paths y divide por la mitad, redondeando hacia abajo para la primera mitad
    num_img_paths = len(img_paths)
    print(img_paths)
    num_img_paths_mas= num_img_paths+1
    if num_img_paths == 0:
        print("No hay imágenes para procesar.")
        return
    
    # Divide el diccionario en dos, aunque solo se procesará la primera mitad
    primera_mitad_keys = list(img_paths)[:num_img_paths // 2]
    primera_mitad = {key: img_paths[key] for key in primera_mitad_keys}

    # Determina cuál función de fondo utilizar basada en el número de imágenes en la primera mitad
    num_primera_mitad = len(primera_mitad)
    print(f"Procesando la primera mitad con {num_primera_mitad} imágenes...")
    print(primera_mitad)

    if num_primera_mitad == 1:
        f=fondo_uno(primera_mitad, prompt, id, neg_prompts, directory_path,num_img_paths_mas, json_output_path)
        return f
    elif num_primera_mitad == 2:
        f=fondo_dos(primera_mitad, prompt, id, neg_prompts, directory_path,num_img_paths_mas,json_output_path)
        return f
    elif num_primera_mitad == 3:
        f=fondo_tres(primera_mitad, prompt, id, neg_prompts, directory_path,num_img_paths_mas,json_output_path)
        return f
    elif num_primera_mitad >= 4:
        # Si hay 4 o más, solo se procesan 4 debido a la limitación a fondo_cuatro
        selected_keys = primera_mitad_keys[:4]  # Selecciona solo los primeros 4 si hay más
        selected_images = {key: img_paths[key] for key in selected_keys}
        f=fondo_cuatro(selected_images, prompt, id, neg_prompts, directory_path,num_img_paths_mas, json_output_path)
        return f
    else:
        print("Número de imágenes no soportado.")


      
def cambio_multiples_caras(persons,id,prompt,prompt_b):
    directory_path = f"C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\persona_{id}"
    json_output_path = "output.json"
    personas=call_selector(persons,directory_path,json_output_path,id)
    print(personas)
    num_personas=len(personas)
    negative_prompt= "deformed, naked,White and black ,watermarks,text, bad quality, low quality"
    cambio_paths=call_cambio(personas,prompt,id,negative_prompt)
    print(cambio_paths)
    num_personas
    #img_path= r"C:\Users\jairc\Downloads\ComfyUI_temp_yizse_00004_.png"
    neg_prompts= "deformed, naked,White and black ,watermarks,text, bad quality, low quality"
    json_output_path = "output3.json"

    final=dividir_y_aplicar_fondo(cambio_paths, prompt_b, id, neg_prompts, directory_path, json_output_path)
    print(final)
    
    return final

if __name__ == "__main__":

    id=generate_random_15_digit_number()
    persons=r"C:\Users\jairc\Downloads\ComfyUI_temp_cghpg_00016_.png"
    #persons=r"C:\Users\jairc\Downloads\DALL·E 2023-12-16 21.53.21 - Four office workers in a modern office setting, each from a different background. The first is a Hispanic man, young and energetic, working at a compu.png"
    prompt = "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up,standing greek statue of philosophy with beard and muscle, cinematic, 8k, dark background"
    prompt_b=" beautiful field of flowers, colorful, perfect lighting, leica summicron 35mm f2.0, kodak portra 400, film grain" 

    a=cambio_multiples_caras(persons,id,prompt,prompt_b)
    print("-----")
    print(a)