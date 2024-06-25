from urllib import request, error
import json
import random
import os
import time
def monitor_directory_final(path, json_output_path):
    last_file_count = 0
    no_new_files_wait_time = 3  # Aumentado para dar más tiempo al proceso externo
    final_wait_time = 3 # Igualmente aumentado para ser más permisivo

    while True:
        try:
            file_list = os.listdir(path)
            file_count = len(file_list)

            print(f"Comprobando... {file_count} archivos encontrados.")

            if file_count > last_file_count:
                print("Se encontraron nuevos archivos. Reiniciando el contador de espera.")
                last_file_count = file_count
                time.sleep(no_new_files_wait_time)
            else:
                print("No se encontraron nuevos archivos. Esperando tiempo adicional antes de decidir.")
                time.sleep(final_wait_time)

                file_list_after_wait = os.listdir(path)
                if len(file_list_after_wait) == file_count:
                    if file_count > 0:
                        image_data = {f"{i}": os.path.join(path, file) for i, file in enumerate(file_list, start=1)}
                        with open(json_output_path, 'w') as json_file:
                            json.dump(image_data, json_file, indent=4)
                        
                        print(f"Archivo JSON creado con {file_count} elementos.")
                        return image_data
                    else:
                        print("No se encontraron archivos para incluir en el JSON.")
                        return {}
                    break
                else:
                    print("Se encontraron nuevos archivos durante el tiempo de espera adicional. Reiniciando el proceso.")
                    last_file_count = len(file_list_after_wait)
        except Exception as e:
            print(f"Error: {e}")
            break

json_file_path = 'selector.json'

# Load JSON data from file
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

def queue_prompt(prompt):
    try:
        p = {"prompt": prompt}
        data = json.dumps(p).encode('utf-8')
        req = request.Request("http://127.0.0.1:8188/prompt", data=data)
        with request.urlopen(req) as response:
            response_data = response.read()
            print("Request successful, response:", response_data)
            if response.status != 200:
                print(f"Error en la solicitud: HTTP {response.status}")
    except error.HTTPError as e:
        print('HTTPError:', e.code, e.reason)
    except error.URLError as e:
        print('URLError:', e.reason)
    except Exception as e:
        print('Generic Exception:', e)

def generate_random_15_digit_number():
    return random.randint(100000000000000, 999999999999999)


def selector(persons_path, id):
    dir_path = f'C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\persona_{id}'
    os.makedirs(dir_path, exist_ok=True)
    print(f"Directory created at {dir_path}")

    data["5"]["inputs"]["image"] = persons_path
    data["32"]["inputs"]["output_path"] = f"persona_{id}"
    queue_prompt(data)

def call_selector(persons, directory_path, json_output_path,id):
    selector(persons,id)
    output = monitor_directory_final(directory_path, json_output_path)
    if not output:  # Verifica si 'output' está vacío
        print("No se encontraron archivos para procesar.")
        return output

    longitud = len(output)
    print(longitud)
    return output




if __name__ == "__main__":
    id=generate_random_15_digit_number()
    directory_path = f"C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\persona_{id}"
    json_output_path = "output.json"
    persons=r"C:\Users\jairc\Downloads\ComfyUI_temp_gehnl_00009_.png"
    personas=call_selector(persons,directory_path,json_output_path,id)
    print(personas)