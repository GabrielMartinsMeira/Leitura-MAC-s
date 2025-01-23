import os
import requests

MAINPATH = os.path.join(os.path.dirname(os.path.abspath("consult.py")))

def consulta_mac(mac):
    try:
        URL = "https://" + mac    

        with open(os.path.join(MAINPATH, "config", "token.txt"), 'r') as file:
            token = file.read().strip()

        headers = {
        "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(URL, headers=headers)
        
        if response.status_code == 200:
            status = response.json()['profile']['status']
            client = response.json()['profile']['name']
            version = response.json()['fw_version']
            
            #print(status, client, version)

            return status, version, client
        else:
            nomac = 10
            return nomac
    except Exception as e:
        print("Error ", e)