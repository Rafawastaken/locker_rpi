"""
    Processar mensagens recebidas pelo GSM
    
    Tipo de mensagens esperadas:
        - SALDO
            -> Responde com mensagen saldo atual

        - ABRIR -> abrir#id_porta#codigo
            -> Abrir porta X
            -> Responde com "porta aberta"
            -> Responde com "porta fechada"

        - CODIGO -> codigo#id_porta#novo_codigo
            -> Altera codigo atual para novo codigo 
            -> Responde com codigo alterdo com sucesso
"""

# Controlar GPIOS 
from modules.ios.control_gpios import ControlarGpios
import RPi.GPIO as GPIO
from time import sleep

class ProcessarMensagem:
    def __init__(self, gsm_driver, utilizadores_registados:list, dispositivos:list, 
        mensagem, log_endpoint:str, server_logs_driver, server_com_driver):
        # Preparar GPIOs
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        # Constantes
        self.log_endpoint = log_endpoint

        # Drivers
        self.gsm_driver = gsm_driver
        self.server_logs_driver = server_logs_driver
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
            nome = device.get('nome').title()
            id_device = device.get('id').lower()
            codigo_device = device.get('codigo')
            pino_device = device.get('pino')

            # validar codigo
            if id_device == device_id_request and codigo_device == codigo_request:  
                # -> Abrir porta
                ControlarGpios.abrir(pino_device)
                # -> Enviar SMS - Porta aberta
                self.gsm_driver.enviar_msg(f"{nome} aberta")
                # -> Enviar LOG
                self.server_logs_driver.adicionar_log(self.remetente, nome + " - Aberta", "GSM", self.log_endpoint)
                
                # -> DELAY
                sleep(10)

                # -> Fechar porta
                ControlarGpios.fechar(pino_device)
                # Enviar SMS - Porta fechada
                self.gsm_driver.enviar_msg(f"{device.get('nome').title()} - Fechada")
                # Enviar LOG
                self.server_logs_driver.adicionar_log(self.remetente, nome + "- Fechada", "GSM", self.log_endpoint)

                return True

        print("ID de porta ou codigo de acesso errado")
        return False

    # Alterar codigo KEYPAD
    def alterar_codigo_keypad(self, id_porta, novo_codigo):
        # Verificar se utilizador se encontra registado
        id_porta = id_porta.lower().replace(" ", "")
        novo_codigo = novo_codigo.replace(" ", "")

        if self.verificar_remetente():
            # Verificar se codigo nao esta a ser utilizado por outra porta
            for dispositivo in self.dispositivos_registados:
                codigo_dispositivo = dispositivo.get('codigo')
                nome_dispositivo = dispositivo.get('nome')
                if novo_codigo == codigo_dispositivo:
                    print(f"Codigo [{novo_codigo}] a ser utilizador por {nome_dispositivo}")
                    return False

            self.server_com_driver.alterar_codigo(id_porta, novo_codigo)
            return True

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
        elif "codigo" in self.conteudo or "código" in self.conteudo:
            try:
                parser = self.conteudo.split("#")
                id_porta = parser[1]
                novo_codigo = parser[2]

                self.alterar_codigo_keypad(id_porta, novo_codigo)
            except Exception as e:
                print(e)
                self.gsm_driver.enviar_msg("Impossivel alterar codigo pretendido")
