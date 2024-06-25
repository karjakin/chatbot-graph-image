
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
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break

json_file_path = 'text2image.json'

# Load JSON data from file
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

def queue_prompt(prompt):
    try:
        p = {"prompt": prompt}
        data = json.dumps(p).encode('utf-8')  # Prepara los datos de la solicitud
        req = request.Request("http://127.0.0.1:8188/prompt", data=data, method='POST')  # Configura la solicitud POST
        with request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))  # Decodifica la respuesta
            print("Request successful, response:", response_data)

            if 'prompt_id' in response_data:
                print(f"Prompt ID: {response_data['prompt_id']}")
                return response_data['prompt_id']  # Retorna el prompt_id para su posterior seguimiento
            else:
                print("Response did not contain a 'prompt_id'.")
                return None
    except error.HTTPError as e:
        print('HTTPError:', e.code, e.reason)
    except error.URLError as e:
        print('URLError:', e.reason)
    except Exception as e:
        print('Generic Exception:', e)
        return None
    
def query_status(prompt_id):
    try:
        url = f"http://127.0.0.1:8188/status?prompt_id={prompt_id}"
        req = request.Request(url)
        with request.urlopen(req) as response:
            status_data = json.loads(response.read().decode('utf-8'))
            return status_data  # Este dict contiene el estado actual de la solicitud
    except error.HTTPError as e:
        print(f'HTTPError: {e.code} {e.reason}')
        return None
    except error.URLError as e:
        print(f'URLError: {e.reason}')
        return None
    except Exception as e:
        print(f'Generic Exception: {e}')
        return None

def wait_for_completion(prompt_id):
    print(f"Waiting for completion of the process with prompt_id: {prompt_id}")
    while True:
        status_data = query_status(prompt_id)
        if status_data:
            if 'status' in status_data:
                status = status_data['status']
                print(f"Current status for {prompt_id}: {status}")

                if status == 'completed':
                    print(f"Process with prompt_id: {prompt_id} completed successfully.")
                    break
                elif status == 'error':
                    print(f"Process with prompt_id: {prompt_id} encountered an error.")
                    break
            else:
                print(f"Unexpected response structure: {status_data}")
                break
        else:
            print("Failed to retrieve the status. Retrying...")
        
        time.sleep(5) 

def generate_random_15_digit_number():
    return random.randint(100000000000000, 999999999999999)

def text_to_imagen(prompt,id):
    print(prompt)
    print(id)
    

    
    # Create directory
    dir_path = f'C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\image_{id}'
    os.makedirs(dir_path, exist_ok=True)
    print(f"Directory created at {dir_path}")
    

  
    data["1"]["inputs"]["seed"] = id    
    data["3"]["inputs"]["text"] = prompt
    data["9"]["inputs"]["output_path"] = f"image_{id}"
    queue_prompt(data)  # Assuming this generates the image and saves it to the specified path

def call_text_to_imagen(prompt,directory_path,id,limite,json_output_path):
    
    text_to_imagen(prompt,id)
    output=monitor_directory(directory_path,limite,json_output_path)
    output2=output["1"]
    return output2

if __name__ == "__main__" :
    prompt="The pixelated beach scene with a vibrant orange and pink sunset, silhouetted palm trees swaying in the breeze is a beautiful and serene sight."
    
    neg_prompts= "deformed, naked,White and black ,watermarks,text, bad quality, low quality"
    id=generate_random_15_digit_number()
    directory_path = f"C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\image_{id}"
    limite= 1
    json_output_path = "output3.json"
    
    a=call_text_to_imagen(prompt,directory_path,id,limite,json_output_path)
    print(a)
