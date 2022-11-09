# GSM - SIM900
from modules.gsm.sim900_driver import DriverSIM900 # Driver do sim900
from modules.gsm.processar_mensagem import ProcessarMensagem # Processar SMS

# Server Comunication
from modules.server.atualizar_config import AtualizarConfig # Descarregar / Atualizar config
from modules.server.comunicate_logs import AdicionarLogServidor # Adicionar logs no servidor
from modules.server.receber_servidor import ProcessarServidor

# Keypad driver
from modules.keypad.keypad import KeypadDriver # Driver de teclado


# Generalistas
import multiprocessing
from time import sleep
import json
import sys
import os


# * Funcoes Helpers * #


# Ler creds
def read_creds():
    # Ler ficheiro "creds.json" e carregar com json
    with open('./data/creds.json', "r", encoding='utf-8') as file:
        creds = json.load(file)

    # Retorna nome de acesso e codigo associado
    return creds.get('access_name'), creds.get('access_key')


# Verificar se config existe
def verificar_config(config_driver):
    # Verificar if config.json existe
    if not os.path.exists('./data/config.json'):
       config_driver.descarregar_config()
    
    # Carregar config.json
    with open("./data/config.json", "r") as conf:
        config = json.loads(conf.read())

    return config


# * Funcoes script para serem utilizadas com multiprocessing

def run_verificar_config(config_driver):
    while True:
        if config_driver.verificar_config():
            config = verificar_config(config_driver)
            # Se config for alterada necessario reeinciar script
            os.system("sudo python raspberry.py")
        sleep(2)
            

def run_processar_servidor(processar_servidor):
    print("Receber servidor")
    while True:
        processar_servidor.ler_servidor()
        sleep(2)

def run_ler_teclado(keypad_driver):
    print("Aguardar teclado")
    while True:
         keypad_driver.ler_keypad()
         sleep(1)

def run_ler_gsm(gsm_driver, users_autorizados, disp_registados, logs_endpoint, server_logs_driver, processar_servidor):
    print("Aguardar mensagem")
    while True:
        mensagem = gsm_driver.receber_msg()
        if mensagem:
            processar_mensagem = ProcessarMensagem(gsm_driver, users_autorizados, disp_registados, 
                mensagem, logs_endpoint, server_logs_driver, processar_servidor) 
            processar_mensagem.interpretar_mensagem()
            print("-" * 30)

# * Loop principal do rapsberry

def main():
    # * Constantes
    access_name, access_key = read_creds()
    server_auth = (access_name, access_key)
    
    # * Endpoints
    descarregar_config_endpoint = "http://192.168.1.65:5000/config" # ! Necessario mudar quando online
    logs_endpoint = "http://192.168.1.65:5000/registos/adicionar" # ! Necessario mudar quando online
    status_devices_endpoint = "http://192.168.1.65:5000/status" # ! Necessario mudar quando online
    patch_device_db_endpoint = "http://192.168.1.65:5000/device-patch/" # ! Necessario mudar quando online
    verificar_atualizar_endpoint = "http://192.168.1.65:5000/update-status-config" # ! Necessario mudar quando online

    # * Inicializar Drivers
    
    # Config Driver
    config_driver = AtualizarConfig(access_name, access_key, descarregar_config_endpoint, verificar_atualizar_endpoint)
    config = verificar_config(config_driver)

    # Ler valores de config
    users_autorizados = config.get('users')
    disp_registados = config.get('dispositivos')

    
    # GSM Driver
    gsm_driver = DriverSIM900("/dev/ttyS0")

    # Server
    server_logs_driver = AdicionarLogServidor(access_name, access_key)
    processar_servidor = ProcessarServidor(server_auth, status_devices_endpoint, 
        server_logs_driver, logs_endpoint, patch_device_db_endpoint)

    # Preparar Driver Keypad
    keypad_driver = KeypadDriver(disp_registados, logs_endpoint, server_logs_driver)
    keypad_driver.setup_pins()


    # * Criar processes para raspberry
    process_verificar_config = multiprocessing.Process(target = run_verificar_config, args = [config_driver])
    process_processar_servidor = multiprocessing.Process(target = run_processar_servidor, args = [processar_servidor])
    process_ler_teclado = multiprocessing.Process(target = run_ler_teclado, args = [keypad_driver])
    process_ler_gsm = multiprocessing.Process(target = run_ler_gsm, args = [gsm_driver, users_autorizados, disp_registados, 
        logs_endpoint, server_logs_driver, processar_servidor])

    # * Iniciar processes 
    process_verificar_config.start()
    process_processar_servidor.start()
    process_ler_teclado.start()
    process_ler_gsm.start()
    
    # * Join processes
    process_verificar_config.join()
    process_processar_servidor.join()
    process_ler_teclado.join()
    process_ler_gsm.join()


if __name__ == '__main__':
    main()


