"""
    Driver para controlar SIM900 - GSM_Comunication
    ...
    Driver possui funcoes para:
        - Enviar mensagem
        - Ler última mensagem
        - Ler saldo de cartão -> Envia mensagem para destinatario com saldo
    ...
"""

from time import sleep
import serial
import sys

# Driver para SIM900
class DriverSIM900:
    # port -> porta serial utilizada
    def __init__(self, port, baudrate = 9600, timeout = 1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.max_recursions = 0

        # GSM Serial Driver
        self.gsm = serial.Serial(
            port = self.port, 
            baudrate = self.baudrate, 
            timeout = self.timeout) 

        # Setup Text Mode
        self.gsm.write('AT+CMFG=1\r'.encode())


    # Self enviar mensagem com estado do gsm / fechadura
    def enviar_msg(self, mensagem):
            print(f"Enviar mensagem: '{mensagem}' para {self.destinatario}")
            self.gsm.write(f'AT+CMGS="{self.destinatario}"\r'.encode())
            sleep(1)
            self.gsm.write((mensagem + chr(26)+ "\r").encode())
            sleep(1)

            return "Mensagem enviada com sucesso"


    # Funcao para receber o saldo atual do cartão
    def saldo_cartao(self):
        print("Verificar saldo do cartão", end = "\r")
        self.resp = self.gsm.read(1000).decode()
        self.gsm.write('AT+CUSD=1,"*111#",15\r'.encode())
        attempts = 0

        while 'EUR' not in self.resp:
            if attempts >= 3: 
                # 10 Tentativas por recursion
                print(f"Aguardar saldo - {self.max_recursions}", end = '\r')
                
                # Maximo de 3 recursions permitidas
                self.max_recursions = self.max_recursions + 1
                if attempts >= 5:
                    return "Impossivel de obter saldo tente novamente mais tarde"
    
                #  Recursion para pobter saldoç
                self.saldo_cartao()

            self.resp = self.gsm.read(1000).decode()
            attempts = attempts + 1

        # String manip. para isolar saldo da msg
        self.saldo = self.resp.split("\n")[2][1:]   
        
        # Recursion para certificar que saldo está contido
        if "EUR" not in self.saldo: self.saldo_cartao()

        self.max_recursions = 0 # Recursions reset
        return self.saldo


    # Funcao que aguarda receber mensagem e retorna o seu conteudo
    def receber_msg(self):         
        print("Aguardar mensagem...")
        self.gsm.write('AT+CNMI=1,2,0,0,0\r'.encode())
        self.resp = self.gsm.read(1000).decode()

        while True:
            self.resp = self.gsm.read(100).decode()
            if self.resp and 'ERROR' not in self.resp:
                try:
                    # Mensagem RAW                
                    self.msg_raw = self.resp.split("\n")             
                    
                    # Header de msg_raw 
                    self.header = self.msg_raw[1].replace('"', '').split(",")

                    # String manip. para isolar remetente e data
                    self.rementente = self.header[0].split(":")[1].replace(" ", "") # Quem enviou mensagem
                    self.destinatario = self.rementente # Destinatario da mensagem mesmo que remetente

                    self.data = self.header[2]
                    self.hora = self.header[3].split("+")[0]

                    # Conteudo mensagem
                    self.content = self.msg_raw[2]
                    
                    # Return
                    self.msg_clean = {
                        "remetente":self.rementente,
                        "destinatario":self.destinatario,
                        "data":self.data,
                        "hora":self.hora,
                        "conteudo":self.content
                    }

                    return self.msg_clean

                except IndexError:
                    continue

                except KeyboardInterrupt:
                    sys.exit(1) 

                except Exception as e:
                    print(e)