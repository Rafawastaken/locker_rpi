"""
    Processar mensagens recebidas pelo GSM
    
    Tipo de mensagens esperadas:
        - SALDO
            -> Responde com mensagen saldo atual

        - ABRIR -> abrir#nome porta#codigo
            -> Abrir porta X
            -> Responde com "porta aberta"
            -> Responde com "porta fechada"

        - CODIGO -> codigo#codigo_antigo#novo_codigo
            -> Altera codigo atual para novo codigo 
            -> Responde com codigo alterdo com sucesso
"""

# Controlar GPIOS 
from modules.ios.control_gpios import ControlarGpios
import RPi.GPIO as GPIO
from time import sleep

class ProcessarMensagem:
    def __init__(self, gsm_driver, utilizadores_registados:list, dispositivos:list, mensagem, server_com_driver):
        # Preparar GPIOs
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        # Drivers
        self.gsm_driver = gsm_driver
        self.server_com_driver = server_com_driver

        # utilizadores registados
        self.utilizadores_registados = utilizadores_registados
        self.lista_contactos_autorizados = []
        for utilizador in self.utilizadores_registados:
            self.lista_contactos_autorizados.append(utilizador.get('contacto'))

        # dispositivos registados
        self.dispositivos_registados = dispositivos

        # Conteudo de mensagem
        self.remetente = mensagem.get("remetente")
        self.destinatario = mensagem.get("destinatario")
        self.data = mensagem.get("data")
        self.hora = mensagem.get("hora")
        self.conteudo = mensagem.get("conteudo")

        # Limpar strings
        self.remetente = self.remetente.replace(" ", "")
        self.conteudo = self.conteudo.replace(" ", "")[:-1] .lower()


    # Verificar se remente esta presente na lista de utilizadores registados
    def verificar_remetente(self):
        if self.remetente not in self.lista_contactos_autorizados:
            print("Numero de rementente nao reconhecido, ignorar")
            return False
        print("Numero de remetente reconhecido")
        return True

    
    # Enviar mensagme com saldo do cartao
    def comunicar_saldo(self):
        if self.verificar_remetente():
            print("Verificar saldo de cartao")
            saldo_atual = self.gsm_driver.saldo_cartao() # Obtem saldo do cartao
            self.gsm_driver.enviar_msg(saldo_atual) # Envia mensagem com saldo
            return f"Saldo: {saldo_atual} -> Mensagem enviada com sucesso."


    # Abrir e Fechar porta por SMS 
    def controlar_porta_gsm(self):      
        self.conteudo = self.conteudo.split("#")
        device_id_request = self.conteudo[1].lower().replace(" ", "")
        codigo_request = str(self.conteudo[2]).replace(" ", "")
        
        for device in self.dispositivos_registados:
            nome_device = device.get('nome')
            id_device = device.get('id').lower()
            codigo_device = device.get('codigo')
            pino_device = device.get('pino')

            # validar codigo
            if id_device == device_id_request and codigo_device == codigo_request:    
                endpoint = "http://192.168.1.65:5000/registos/adicionar"

                # Encontrar dispositivo   

                # -> Abrir porta
                ControlarGpios.ligar(pino_device)
                # -> Enviar SMS - Porta aberta
                self.gsm_driver.enviar_msg(f"{device.get('nome').title()} aberta")
                # -> Enviar LOG
                self.server_com_driver.adicionar_log(self.remetente, device.get("nome").title(), "GSM", endpoint)
                
                # -> DELAY
                sleep(10)

                # -> Fechar porta
                ControlarGpios.desligar(pino_device)
                # Enviar SMS - Porta fechada
                self.gsm_driver.enviar_msg(f"{device.get('nome').title()} fechada")
                # Enviar LOG
                self.server_com_driver.adicionar_log(self.remetente, device.get("nome").title(), "GSM", endpoint)
                return True

        print("ID de porta ou codigo de acesso errado")
        return False

    # Alterar codigo KEYPAD
    def alterar_codigo_keypad(self, codigo_antigo, codigo_novo):
        # Verificar se utilizador se encontra registado
        if self.verificar_remetente():
            # * Adicionar codigo para processar creds e alterar data *
            self.gsm_driver.enviar_msg(f"Codigo da porta X alterado de {codigo_antigo} para {codigo_novo}")


    # Interpretar pedido de mensagme
    def interpretar_mensagem(self):
        print("Verificar mensagem recebida")

        # Processar pedido de estado de cartão
        if self.conteudo == "saldo":
            self.comunicar_saldo()

        # Processar pedido para controlar portas
        elif "abrir" in self.conteudo:
            self.controlar_porta_gsm()
            
        # Processar pedido para altearar codigo de keypad
        elif "codigo" in self.conteudo:
            try:
                parser = self.conteudo.split("#")
                codigo_antigo = parser[1]
                codigo_novo = parser[2]

                self.alterar_codigo_keypad(codigo_antigo, codigo_novo)
            except Exception as e:
                print(e)
                self.gsm_driver.enviar_msg("Impossivel alterar codigo pretendido")
