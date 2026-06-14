import os 
import json 

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

FERNET_KEY = os.getenv("FERNET_KEY")

fernet = Fernet(FERNET_KEY.encode())

def encrypt_data(data:dict) -> str:
    json_data = json.dumps(data)
    encrypted_data = fernet.encrypt(json_data.encode()).decode()
    return encrypted_data

def decrypt_data(data:str) -> dict:
    decrypted_data = fernet.decrypt(data.encode())
    data_json = json.loads(decrypted_data.decode())
    return data_json
