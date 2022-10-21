from time import sleep
import serial
import sys

# Driver para SIM900
class GSM_Comunication:
    # port -> porta serial utilizada
    def __init__(self, port, baudrate = 9600, timeout = 1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        # GSM Serial Driver
        self.gsm = serial.Serial(
            port = self.port, 
            baudrate = self.baudrate, 
            timeout = self.timeout) 

        # Setup Text
        self.gsm.write('AT+CMFG=1\r'.encode())

    # Self enviar mensagem com estado do gsm / fechadura
    def enviar_msg(self, mensagem):
            # Enviar "mensagem" para número
            pass

    # Funcao para receber o saldo atual do cartão
    def saldo_cartao(self):
        print("Saldo do cartão")
        self.gsm.write('AT+CUSD=1,"*111#",15\r'.encode())
        self.resp = self.gsm.read(1000).decode()
        self.attempts = 0

        while 'EUR' not in self.resp:
            if self.attempts == 10: 
                return "Impossivel de obter saldo, tente novamente"
            self.resp = self.gsm.read(1000).decode()

        # String manip. para isolar saldo da msg
        self.saldo = self.resp.split("\n")[2][1:]   
    
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
                    self.rementente = self.header[0].split(":")[1].replace(" ", "")
                    self.data = self.header[2]
                    self.hora = self.header[3].split("+")[0]

                    # Conteudo mensagem
                    self.content = self.msg_raw[2]
                    
                    # Return
                    self.msg_clean = {
                        "remetente":self.rementente,
                        "data":self.data,
                        "hora":self.hora,
                        "conteudo":self.content
                    }

                    return self.msg_clean

                except Exception as e:
                    self.notificar_erro()

                except KeyboardInterrupt:
                    sys.exit(1) # break while True
