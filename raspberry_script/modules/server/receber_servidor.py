from time import sleep
import requests
import json

from modules.ios.control_gpios import ControlarGpios

class ProcessarServidor:
    def __init__(self, server_auth:str, endpoint:str, server_logs_driver, logs_endpoint:str, patch_endpoint:str):
        # Dados para executar request
        self.auth = server_auth
        self.endpoint = endpoint

        # Logs
        self.server_logs_driver = server_logs_driver
        self.logs_endpoint = logs_endpoint
        self.patch_endpoint = patch_endpoint 


    # Atualizar estado de device na base de dados
    def atualizar_device(self, device_id, status):
        data = {"estado":status}
        link_patch = self.patch_endpoint + device_id
        r = requests.patch(link_patch, auth = self.auth, json = data, verify=False)

        if r.status_code == 200:
            print("Estado alterado com sucesso")
        else:
            print("Ocorreu um erro na comunicação - Erro: ", str(r.status_code))


    # Interpretar requests
    def request_parser(self, content):
        dispositivos = json.loads(content)
                
        for dispositivo in dispositivos:
            if dispositivo.get('estado'):
                # Variavel helper melhor readable
                nome = dispositivo.get('nome').title()
                device_id = dispositivo.get("device_id")

                # Abrir Porta
                print(f"{dispositivo.get('nome').title()} - Aberta [Servidor]") # Print abrir porta
                ControlarGpios.abrir(dispositivo.get('pin')) # Alterar GPIO
                self.server_logs_driver.adicionar_log("Servidor", nome + " - Aberta", "Servidor", self.logs_endpoint) # Adicionar Log

                sleep(5) # Delay
                
                # Fechar porta
                print(f"{dispositivo.get('nome').title()} - Fechada [Servidor]") # Fechar mostra print
                ControlarGpios.fechar(dispositivo.get('pin')) # Alterar gpios
                print("Alterar estado de dispositivo servidor")
                self.atualizar_device(device_id, False) # Patch server false dispositivo servidor
                self.server_logs_driver.adicionar_log("Servidor", nome + " - Fechada", "Servidor", self.logs_endpoint) # Adicionar Log

                print("-" * 30)

            # Certificar que esta fechada - nao e necessario log
            if not dispositivo.get('estado'):
                ControlarGpios.fechar(dispositivo.get('pin'))


    # Ler estado de portas no servidor
    def ler_servidor(self):
        r = requests.get(self.endpoint, auth = self.auth)

        if r.status_code == 200:
            self.request_parser(r.content)


    # Alterar codigo de porta
    def alterar_codigo(self, device_id, novo_codigo):
        data = {"codigo":novo_codigo}
        link_patch = self.patch_endpoint + device_id
        r = requests.patch(link_patch, auth = self.auth, json = data, verify=False)
        if r.status_code == 200:
            print("Pedido de alteracao de codigo enviado com sucesso")