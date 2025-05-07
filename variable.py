import requests
import base64
import yaml
import nacl.public

def check_repository_variable_exist(org_name: str, repo_name: str, variable_name: str, headers) -> bool:
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/actions/variables/{variable_name}"
    response = requests.get(url, headers=headers)
    return response.status_code == 200

def create_variable(org_name: str, repo_name: str, variable_name: str, value: str, headers) :
    print(f"creating a new variable: ", value)
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/actions/variables"
    payload = { "name": str(variable_name), "value": str(value) }
    
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code not in [201, 204]:
        print(f"[ERROR] Failed to set variable {name} in {repo}: {res.status_code} {res.text}")       
        
def update_variable(org_name: str, repo_name: str, variable_name: str, value: str, headers) :
    print(f"updating variable: ", value)
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/actions/variables/{variable_name}"
    payload = { "name": str(variable_name), "value": str(value) }
    res = requests.patch(url, headers=headers, json=payload)
    if res.status_code not in [201, 204]:
        print(f"[ERROR] Failed to set variable {name} in {repo}: {res.status_code} {res.text}")