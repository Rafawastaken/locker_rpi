# GSM - SIM900
from modules.gsm.sim900_driver import DriverSIM900
from modules.gsm.processar_mensagem import ProcessarMensagem

# Server Comunication
from modules.server.atualizar_config import AtualizarConfig
from modules.server.comunicate_server import ComunicarServidor

# Keypad driver
from modules.keypad.keypad import KeypadDriver


# Generalistas
import json
import os

# Ler creds
def read_creds():
    # Ler ficheiro "creds.json" e carregar com json
    with open('./data/creds.json', "r", encoding='utf-8') as file:
        creds = json.load(file)

    # Retorna nome de acesso e codigo associado
    return creds.get('access_name'), creds.get('access_key')

def atualizar_creds(access_name, access_key, endpoint):
    # Verificar se ficheiro de config.json existe
    config = AtualizarConfig(access_name, access_key, endpoint)
    config.descarregar_config()


def main():
    access_name, access_key = read_creds()

    # Verificar if config.json existe
    if not os.path.exists('./data/config.json'):
        print("Descarregar config")
        endpoint = "http://192.168.1.65:5000/config"
        atualizar_creds(access_name, access_key, endpoint)
    
    # Carregar config.json
    with open("./data/config.json", "r") as conf:
        config = json.loads(conf.read())

    # Atribuir valores
    users_autorizados = config.get('users')
    disp_registados = config.get('dispositivos')

    # Criar Driver para GSM 
    gsm_driver = DriverSIM900("/dev/ttyS0")
    server_com_driver = ComunicarServidor(access_name, access_key)

    # Preparar Driver Keypad
    keypad_driver = KeypadDriver(disp_registados)
    keypad_driver.setup_pins()

    # Ciclo principal
    while True:
        mensagem = gsm_driver.receber_msg()
        if mensagem:
            print(mensagem)
            processar_mensagem = ProcessarMensagem(gsm_driver, users_autorizados, disp_registados, mensagem, server_com_driver) 
            processar_mensagem.interpretar_mensagem()
            print("-" * 30)

    # while True:
    #     keypad_driver.ler_keypad()


if __name__ == '__main__':
    main()


