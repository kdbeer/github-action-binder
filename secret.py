import requests
import base64
import yaml
from nacl import public, encoding, exceptions

def encrypt_secret(secret: str, base64_public_key: str) -> str:
    # Decode base64 public key to bytes
    public_key_bytes = base64.b64decode(base64_public_key)

    # Load public key
    public_key = public.PublicKey(public_key_bytes)

    # Encrypt using crypto_box_seal equivalent
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret.encode("utf-8"))

    # Encode encrypted data to base64
    return base64.b64encode(encrypted).decode("utf-8")

def get_public_key(org_name: str, repo_name: str, headers) -> tuple[str, str]:
    # เรียก API
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/actions/secrets/public-key"
    response = requests.get(url, headers=headers)
    

    # แสดงผลลัพธ์
    if response.status_code == 200:
        public_key_data = response.json()
        return public_key_data["key_id"], public_key_data["key"]
    
    return "", ""

def check_repository_secret_exist(org_name: str, repo_name: str, secret_name: str, headers) -> bool:
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/actions/secrets/{secret_name}"
    response = requests.get(url, headers=headers)
    return response.status_code == 200
        
def create_secret(org_name: str, repo_name: str, secret_name: str, payload, headers) :
    print(f"creating a new secret: ", secret_name)
    
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/actions/secrets/{secret_name}"    
    res = requests.put(url, headers=headers, json=payload)
    if res.status_code not in [201, 204]:
        print(f"[ERROR] Failed to set variable {org_name} in {repo_name}: {res.status_code} {res.text}") 