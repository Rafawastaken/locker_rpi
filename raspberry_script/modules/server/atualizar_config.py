"""
    Atualizar ficheiro config
        Recebe access_name e access_key e descarrega config
        Config armazenada em "./data/config.json"

"""

import requests
import json

class AtualizarConfig:
    def __init__(self, access_name:str, access_key:str, endpoint:str):
        self.access_name = access_name # Nome de acesso - Servidor
        self.access_key = access_key # Código de acesso - Servidor
        self.endpoint = endpoint # Endpoint de link - Api Endpoint 

    def descarregar_config(self):
        r = requests.get(self.endpoint, auth = (self.access_name, self.access_key))
        
        with open('./data/config.json', "w") as conf:
            content = json.loads(r.content)
            conf.write(str(content).replace("'", '"'))