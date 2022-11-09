import requests
import json
import os

class AdicionarLogServidor:
    def __init__(self, access_name:str, access_key:str):
        # Validacao api
        self.access_name = access_name
        self.access_key = access_key
        self.auth = (self.access_name, self.access_key)

    def adicionar_log(self, utilizador, device, origem, endpoint):
        self.utilizador = utilizador
        self.device = device,
        self.origem = origem
        
        data = {
            "nome":self.utilizador,
            "target":self.device,
            "origem":self.origem
        }

        print("Publicar log no servidor")        

        # Enviar put request para API
        r = requests.put(endpoint, auth = self.auth, json = data, verify = False)

        if r.status_code == 200:
            print("Log adicionado com sucesso!")
            return True

        print("Ocorreu um problem ao adicionar o log")
        return False
