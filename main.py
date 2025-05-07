import requests
import base64
import yaml
import nacl.public
from variable import check_repository_variable_exist, create_variable, update_variable
from secret import get_public_key, create_secret

def encrypt_secret(value, public_key):
    public_key_bytes = base64.b64decode(public_key)
    sealed_box = nacl.public.SealedBox(nacl.public.PublicKey(public_key_bytes))
    encrypted = sealed_box.encrypt(str(value).encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

def write_variables(repo_info, variables, headers):
    for name, value in variables.items():
        exists = check_repository_variable_exist(
            org_name=repo_info['owner'],
            repo_name=repo_info['repo'],
            variable_name=name,
            headers=headers
        )
        if not exists:
            create_variable(repo_info['owner'], repo_info['repo'], name, value, headers)
        else:
            update_variable(repo_info['owner'], repo_info['repo'], name, value, headers)

def write_secrets(repo_info, secrets, key_id, public_key, headers):
    for name, value in secrets.items():
        encrypted_value = encrypt_secret(value, public_key)
        payload = {
            "encrypted_value": encrypted_value,
            "key_id": key_id
        }
        create_secret(repo_info['owner'], repo_info['repo'], name, payload, headers)

# ========== MAIN ==========
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

token = config["token"]
repos = config["repositories"]
global_variables = config.get("global_variables", {})
global_secrets = config.get("global_secrets", {})

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

print("=== Writing variables and secrets to repositories ===")
for repo in repos:
    owner = repo['owner']
    repo_name = repo['repo']
    print(f"\n📦 Repo: {owner}/{repo_name}")
    
    key_id, public_key = get_public_key(owner, repo_name, headers)
    if not public_key:
        print("❌ Failed to get public key")
        continue

    print("🔧 Global Variables")
    write_variables(repo, global_variables, headers)

    print("🔧 Custom Variables")
    write_variables(repo, repo.get("overrides", {}).get("variables", {}), headers)

    print("🔐 Global Secrets")
    write_secrets(repo, global_secrets, key_id, public_key, headers)

    print("🔐 Custom Secrets")
    write_secrets(repo, repo.get("overrides", {}).get("secrets", {}), key_id, public_key, headers)
