import aiohttp
import asyncio
import json
import random
import uuid
import websockets

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

async def queue_prompt(prompt):
    async with aiohttp.ClientSession() as session:
        p = {"prompt": prompt, "client_id": client_id}
        data = json.dumps(p).encode('utf-8')
        async with session.post(f"http://{server_address}/prompt", data=data) as response:
            return await response.json()

async def get_image(filename, subfolder, folder_type):
    async with aiohttp.ClientSession() as session:
        params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        async with session.get(f"http://{server_address}/view", params=params) as response:
            return await response.read()

async def get_history(prompt_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{server_address}/history/{prompt_id}") as response:
            return await response.json()

async def get_image_paths(ws, prompt):
    prompt_id = await queue_prompt(prompt)
    retries = 2  # Adjusted number of retries
    wait_time = 2  # Wait for 2 seconds before retrying
    for attempt in range(retries):
        try:
            history = await get_history(prompt_id['prompt_id'])
            # Assuming the structure of history is confirmed to be correct
            output_image_paths = extract_image_paths(history, prompt_id['prompt_id'])
            return output_image_paths
        except KeyError:
            print(f"Attempt {attempt + 1} of {retries} failed. Retrying in {wait_time} seconds...")
            await asyncio.sleep(wait_time)  # Adjust wait time as necessary
    print("Failed to fetch image paths after multiple attempts.")
    return {}

def extract_image_paths(history, prompt_id):
    history_data = history[prompt_id]
    output_image_paths = {}
    for node_id in history_data['outputs']:
        node_output = history_data['outputs'][node_id]
        if 'images' in node_output:
            images_output = [f"{image['subfolder']}/{image['filename']}" for image in node_output['images']]
            output_image_paths[node_id] = images_output
    return output_image_paths

def generate_random_15_digit_number():
    return random.randint(100000000000000, 999999999999999)

async def call_text_to_imagen(prompt, id, json_file_path='text2image.json'):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    data["1"]["inputs"]["seed"] = id
    data["3"]["inputs"]["text"] = prompt
    data["9"]["inputs"]["output_path"] = f"image_{id}"

    async with websockets.connect(f"ws://{server_address}/ws?clientId={client_id}") as ws:
        images_paths = await get_image_paths(ws, data)
        for node_id in images_paths:
            for image_path in images_paths[node_id]:
                return image_path

async def main():
    prompt = "An ice bonsai in a parallel universe, adorned with brilliant incandescent colors, with lightning bolts around it."
    id = generate_random_15_digit_number()
    path = await call_text_to_imagen(prompt, id)
    print(path)

if __name__ == "__main__":
    asyncio.run(main())