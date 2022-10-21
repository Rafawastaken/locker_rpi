from curses import keyname
from modules.gsm.sim900_driver import GSM_Comunication
import json

def read_creds():
    # Ler ficheiro "creds.json" e carregar com json
    with open('data/creds.json', "r", encoding='utf-8') as file:
        creds = json.load(file)

    api = creds['api']
    gsm = creds['gsm']
    keypad = creds['keypad']

    return api, gsm, keypad

def verificar_rementente(rementente): pass


def processar_mensagem(gsm, msg):
    remetente = msg.get('remetente')
    data = msg.get('data')
    hora = msg.get('hora')
    conteudo = msg.get('conteudo').replace(" ", "")[:-1].lower()

    # Mostrar mensagem
    print("-" * 30)
    print(f"Mensagem recebida:\nRemetente: {remetente}\nData: {data}\nHora: {hora}\nConteudo: {conteudo}")
    print("-" * 30)

    # Verificar conteudo de mensagem e agir
    if conteudo.lower == "saldo":
        gsm.saldo_cartao()


def main():
    api, gsm, keypad = read_creds()
    gsm = GSM_Comunication("COM3", gsm['destinatario'])

    while True:
        mensagem = gsm.receber_msg()
        if mensagem: processar_mensagem(gsm, mensagem)

if __name__ == '__main__':
    main()


