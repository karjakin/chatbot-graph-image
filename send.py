import requests

def send_image(numero, filePath):
    url = "http://localhost:3000/envio"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "numero": numero,
        "filePath": filePath  
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)

#send_image("5212223632487", r"C:\Users\jairc\Downloads\ComfyUI_temp_lyxsd_00022_.png")
        
def send_message(numero, mensaje):
    url = "http://localhost:3000/envio"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "numero": numero,
        "mensaje": mensaje 
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)

# Ejemplo de uso
#send_message("5212223632487", "hola, soy pardy")