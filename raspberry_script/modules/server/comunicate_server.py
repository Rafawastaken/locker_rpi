import requests
import json
import os

class ComunicarServidor:
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
        r = requests.put(endpoint, auth = self.auth, json = data, verify=False)
        print(r.status_code)
        if r.status_code == 200:
            return "Log adicionado com sucesso!"
        return "Ocorreu um problem ao adicionar o log"