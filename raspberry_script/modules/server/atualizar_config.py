"""
    Atualizar ficheiro config
        Recebe access_name e access_key e descarrega config
        Config armazenada em "./data/config.json"

"""

from time import sleep
import requests
import json


class AtualizarConfig:
    def __init__(self, access_name:str, access_key:str, descarregar_config_endpoint:str, verificar_endpoint):
        self.auth = (access_name, access_key) # Auth 
        self.descarregar_config_endpoint = descarregar_config_endpoint # Endpoint de link - Api Endpoint 
        self.verificar_endpoint = verificar_endpoint # Verificar endpoint


    # Apos update alterar atualizar
    def patch_config_estado(self):
        data = {"atualizar":False}
        r = requests.patch(self.verificar_endpoint, auth = self.auth, json = data, verify = False)


    # Descarregar config
    def descarregar_config(self):
        print("Descarregar config atualizada")
        r = requests.get(self.descarregar_config_endpoint, auth = self.auth)

        with open('./data/config.json', "w") as conf:
            content = json.loads(r.content)
            conf.write(str(content).replace("'", '"'))

        # Atualização de config terminada com sucesso
        self.patch_config_estado()
        print("Ficheiro config atualizado com sucesso")


    # Verificar se necessario update
    def verificar_config(self):
        try:
            r = requests.get(self.verificar_endpoint, auth = self.auth, timeout=1000)
            content = json.loads(r.content)
            if content.get('atualizar'):
                self.descarregar_config()
                return True
            return False
        except requests.exceptions.ConnectionError:
            print("Conexao recusada, tentar novamente...")
            sleep(5)


        