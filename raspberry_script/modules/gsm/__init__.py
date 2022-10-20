from time import sleep
import serial
import sys

class GSM_Comunication:
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

    def notificar_erro(self):
        # ! Codigo para enviar SMS com erro
        print("Erro ao processar modulo gsm...")

    def saldo_cartao(self):
        self.gsm.write('AT+CUSD=1,"*111#",15\r'.encode())
        self.resp = self.gsm.read(1000).decode()
        self.attempts = 0

        while 'EUR' not in self.resp:
            if self.attempts == 10: 
                return "Impossivel de obter saldo, tente novamente"
            self.resp = self.gsm.read(1000).decode()

        self.saldo = self.resp.split("\n")[2][1:]   
            
        return self.saldo

    def receber_msg(self):         
        print("Aguardar mensagem...")
        self.gsm.write('AT+CNMI=1,2,0,0,0\r'.encode())
        self.resp = self.gsm.read(1000).decode()

        while True:
            self.resp = self.gsm.read(100).decode()
            error = False
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
                    print(e)
                    self.notificar_erro()

                except KeyboardInterrupt:
                    # Evitar ficar preso em while True
                    sys.exit(1)