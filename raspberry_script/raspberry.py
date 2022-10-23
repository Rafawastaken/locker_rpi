from modules.gsm.sim900_driver import DriverSIM900
from modules.gsm.processar_mensagem import ProcessarMensagem
import json

# Ler creds
def read_creds():
    # Ler ficheiro "creds.json" e carregar com json
    with open('data/creds.json', "r", encoding='utf-8') as file:
        creds = json.load(file)

    api = creds['api']
    gsm = creds['gsm']
    keypad = creds['keypad']

    return api, gsm, keypad

def main():
    api, gsm, keypad = read_creds()
    
    gsm_creds = gsm['destinatario']
    gsm_driver = DriverSIM900("COM3", gsm_creds)

    while True:
        mensagem = gsm_driver.receber_msg()
        if mensagem: 
            ProcessarMensagem(gsm_driver, gsm_creds, mensagem)
            print("-" * 30)
    

if __name__ == '__main__':
    main()


