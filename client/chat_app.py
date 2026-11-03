import requests
import crypt_utils
from nacl.public import PublicKey, Box
import asyncio
import websockets

#key generation and requests
key_pair = crypt_utils.generate_keypair()

username = input("Username: ")
credentials = {"username": username, "public_key": key_pair[1].encode().hex()}

print(requests.post('http://localhost:8000/register', json=credentials))

partner = input("\nWith who would you like to chat? ")

partner_query = requests.get('http://localhost:8000/keys/' + partner)

if partner_query.status_code != 200:
    print("User doesn't exist")
    exit(1)

data_partner = partner_query.json()

hex_string = data_partner["public_key"]
hex_partner_key = bytes.fromhex(hex_string)
partner_public_key = PublicKey(hex_partner_key)

box = Box(key_pair[0], partner_public_key)

#message exchange

async def send_messages(websocket):
    while True:
        msg = await asyncio.to_thread(input, "")

        
        cipher_bytes = msg.encode('utf-8')
        ciphertext = box.encrypt(cipher_bytes)
        
        await websocket.send(ciphertext)

async def receive_messages(websocket):
    async for message in websocket:
        plain_text = box.decrypt(message).decode('utf-8')
        print(f"{plain_text}")


async def chat():
    async with websockets.connect('ws://localhost:8765') as websocket:
        await asyncio.gather(
            send_messages(websocket),
            receive_messages(websocket)
        )        

asyncio.run(chat())