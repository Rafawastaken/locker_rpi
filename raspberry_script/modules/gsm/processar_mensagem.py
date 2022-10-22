"""
    Processar mensagens recebidas pelo GSM
    
    Tipo de mensagens esperadas:
        - SALDO
            -> Responde com mensagen saldo atual

        - ABRIR -> abrir#1
            -> Abrir porta X
            -> Responde com "porta aberta"
            -> Responde com "porta fechada"

        - CODIGO -> codigo#codigo_antigo#novo_codigo
            -> Altera codigo atual para novo codigo 
            -> Responde com codigo alterdo com sucesso
"""
# Controlar GPIOS 
from modules.ios.control_gpios import ControlarGpios
from time import sleep

class ProcessarMensagem:
    def __init__(self, gsm_driver, creds, mensagem):
        # Drivers
        self.gsm_driver = gsm_driver
        self.gpio_driver = ControlarGpios()

        # creds
        self.creds = creds

        # Conteudo de mensagem
        self.remetente = mensagem.get("remetente")
        self.data = mensagem.get("data")
        self.hora = mensagem.get("hora")
        self.conteudo = mensagem.get("conteudo")

        # Limpar strings
        self.remetente = self.remetente.replace(" ", "")[:-1]
        self.creds = self.creds.replace(" ", "")[:-1]
        self.conteudo = self.conteudo.replace(" ", "")[:-1] .lower()      
        
        if self.verificar_remetente():
            self.interpretar_mensagem()

    def verificar_remetente(self):
        if self.remetente != self.creds:
            print("Numero de rementente nao reconhecido, ignorar")
            return False
        print("Numero de remetente reconhecido")
        return True

    # Enviar mensagme com saldo do cartao
    def comunicar_saldo(self, saldo_atual):
        self.gsm_driver.enviar_msg(saldo_atual) # Envia mensagem com saldo

    # Abrir e Fechar porta por SMS 
    def controlar_porta_gsm(self, porta_selecionada):
        # Abrir porta
        porta_aberta = self.gpio_driver.abrir_porta(porta_selecionada)
        
        if porta_aberta:
            self.gsm_driver.enviar_msg(f"Porta {porta_selecionada} aberta")
        else:
            print(f"Ocorreu erro ao abrir a porta: {porta_selecionada}")
            return False
        
        # Delay para manter porta aberta
        sleep(10) 

        # Fechar porta
        porta_fechada = self.gpio_driver.fechar_porta(porta_selecionada)
        if porta_fechada:
            self.gsm_driver.enviar_msg(f"Porta {porta_selecionada} fechada")
        else:
            print(f"Ocorreu erro ao abrir a porta: {porta_selecionada}")

    # Alterar codigo KEYPAD
    def alterar_codigo_keypad(self, codigo_antigo, codigo_novo):
        # * Adicionar codigo para processar creds e alterar data*
        self.gsm_driver.enviar_msg(f"Codigo da porta X alterado de {codigo_antigo} para {codigo_novo}")

    # Interpretar pedido de mensagme
    def interpretar_mensagem(self):
        print("Verificar mensagem recebida")
        # Processar pedido de estado de cartão
        if self.conteudo == "saldo":
            saldo_atual = self.gsm_driver.saldo_cartao() # Obtem saldo do cartao
            self.comunicar_saldo(saldo_atual)

        # Processar pedido para controlar portas
        elif "abrir" in self.conteudo:
            porta_selecionada = int(self.conteudo.split("#")[-1])
            self.controlar_porta_gsm(porta_selecionada)
            
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
