
from urllib import request, error
import json
import random
import os
import time
from face import call_selector
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

json_file_path = 'cuatro.json'

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

def json_imagen(img_path,prompt, id, neg_prompts):
    print(prompt)
    

    
    # Create directory
    dir_path = f'C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\persona_{id}'
    os.makedirs(dir_path, exist_ok=True)
    print(f"Directory created at {dir_path}")
    

  
    data["33"]["inputs"]["noise_seed"] = id    
    data["163"]["inputs"]["image"] = img_path["1"]
    data["164"]["inputs"]["image"] = img_path["2"]
    data["174"]["inputs"]["image"] = img_path["3"]
    data["183"]["inputs"]["image"] = img_path["4"]
    data["35"]["inputs"]["text"] = neg_prompts
    data["162"]["inputs"]["text"] = prompt
    #data["86"]["inputs"]["text"] = " "
    #data["87"]["inputs"]["text"] = " "
    data["161"]["inputs"]["output_path"] = f"persona_{id}"
    queue_prompt(data)  # Assuming this generates the image and saves it to the specified path

def fondo_cuatro(img_path,prompt, id, neg_prompts,directory_path,limite,json_output_path):
    
    json_imagen(img_path,prompt, id, neg_prompts)    
    output=monitor_directory(directory_path,limite,json_output_path)
    print(output)
    return output

if __name__ == "__main__" :
    img_path= r"C:\Users\jairc\Downloads\ComfyUI_temp_yizse_00004_.png"
    prompt="The pixelated beach scene with a vibrant orange and pink sunset, silhouetted palm trees swaying in the breeze is a beautiful and serene sight."
    id=generate_random_15_digit_number()
    neg_prompts= "deformed, naked,White and black ,watermarks,text, bad quality, low quality"
    directory_path = f"C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\persona_{id}"
    json_output_path = "output3.json"
    limite= 1
    fondo_cuatro(img_path,prompt, id, neg_prompts,directory_path,limite,json_output_path)

