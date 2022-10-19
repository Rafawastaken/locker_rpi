import requests
import json
import os

class Tek4DoorCom:
    def __init__(self,  link):
        self.link = link
        self.username, self.password = self.get_creds()

        # Utilizado para HTTP Auth
        self.auth = (self.username, self.password) 

    ### * Obtém as credencias de creds.json
    def get_creds(self):
        file = open(os.path.abspath(os.path.dirname(__file__)) + "\\creds.json")
        content = json.load(file)
        return content['username'], content['password'] 

    ### * Enviar Get Request
    def get_status(self):
        endpoint = f"{self.link}/devices_status"

        r = requests.get(endpoint, auth = self.auth)

        if r.status_code == 200: return r.json()
        return "Erro a enviar pedido"

    ### * Enviar patch request para alterar servidor
    def patch_status(self, value, target):
        endpoint = f"{self.link}/device_patch/{target}"

        if value: data = {"estado":"True"}
        elif not value: data = {"estado":"False"}
        
        r = requests.patch(endpoint, auth = self.auth, data = data)
        
        if r.status_code == 200: return r.json()
        return "Erro ao enviar pedido..."
