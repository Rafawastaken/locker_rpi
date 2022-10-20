from modules.gsm import GSM_Comunication

gsm = GSM_Comunication("COM3")
while True:
    nova_mensagem = gsm.receber_msg()
    print(nova_mensagem.get('conteudo'))
    print(nova_mensagem.get('remetente'))