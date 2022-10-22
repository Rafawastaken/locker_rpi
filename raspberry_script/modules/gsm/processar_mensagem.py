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

    def interpretar_mensagem(self):
        print("Verificar mensagem recebida")
        # Processar pedido de estado de cartão
        if self.conteudo == "saldo":
            saldo_atual = self.gsm_driver.saldo_cartao() # Obtem saldo do cartao
            self.gsm_driver.enviar_msg(saldo_atual) # Envia mensagem com saldo

        # Processar pedido para controlar portas
        elif "abrir" in self.conteudo:
            porta_selecionada = self.conteudo.split("#")[-1]    
            # * Codigo para acionar relé * 
            self.gsm_driver.enviar_msg(f"Porta {porta_selecionada} aberta")
            # * Codigo para desacionar relé 
            self.gsm_driver.enviar_msg(f"Porta {porta_selecionada} fechada")

        # Processar pedido para altearar codigo de keypad
        elif "codigo" in self.conteudo:
            try:
                parser = self.conteudo.split("#")
                codigo_antigo = parser[1]
                codigo_novo = parser[2]

                # * Adicionar codigo para processar creds e alterar data*

                self.gsm_driver.enviar_msg(f"Codigo da porta X alterado de {codigo_antigo} para {codigo_novo}")
            except Exception as e:
                print(e)
                # self.gsm_driver.enviar_msg("Impossivel alterar codigo pretendido")
