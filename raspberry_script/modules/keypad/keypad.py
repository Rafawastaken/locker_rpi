import RPi.GPIO as GPIO
import time

from modules.ios.control_gpios import ControlarGpios

class KeypadDriver:
    def __init__(self, dispositivos:list, logs_endpoint:str, server_com):
        # Server communication setup
        self.logs_endpoint = logs_endpoint
        self.server_com_driver = server_com

        # Linhas Teclado
        self.L1 = 29 # 5
        self.L2 = 31 # 6
        self.L3 = 33 # 13
        self.L4 = 35 # 19

        # Colunas Teclado
        self.C1 = 32 # 12
        self.C2 = 36 # 16
        self.C3 = 38 # 20

        # helpers
        self.keypadPressed = -1
        self.input = ""
        self.dispositivos = dispositivos


    def setup_pins(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)

            GPIO.setup(self.L1, GPIO.OUT)
            GPIO.setup(self.L2, GPIO.OUT)
            GPIO.setup(self.L3, GPIO.OUT)
            GPIO.setup(self.L4, GPIO.OUT)

            GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

            GPIO.add_event_detect(self.C1, GPIO.RISING, callback=self.keypadCallback)
            GPIO.add_event_detect(self.C2, GPIO.RISING, callback=self.keypadCallback)
            GPIO.add_event_detect(self.C3, GPIO.RISING, callback=self.keypadCallback)
        except Exception as e:
            print(e)


    def keypadCallback(self, channel):
        if self.keypadPressed == -1:
            self.keypadPressed = channel


    def setAllLines(self, state):
        GPIO.output(self.L1, state)
        GPIO.output(self.L2, state)
        GPIO.output(self.L3, state)
        GPIO.output(self.L4, state)

   
    def checkSpecialKeys(self):
        pressed = False

        GPIO.output(self.L4, GPIO.HIGH)

        if (GPIO.input(self.C3) == 1):
            print("Input reset!");
            pressed = True

        GPIO.output(self.L4, GPIO.LOW)
        GPIO.output(self.L4, GPIO.HIGH)

        if (not pressed and GPIO.input(self.C1) == 1):
            for dispositivo in self.dispositivos:

                # Verificar se codigo introduzido corresponde com codigo de portas
                if self.input == dispositivo.get("codigo"):
                    print(f"Abrir {dispositivo.get('nome')}")

                    # Controlar GPIO - Abrir 
                    ControlarGpios.abrir(dispositivo.get('pino'))

                    # Adicionar log
                    self.server_com_driver.adicionar_log(f"{dispositivo.get('nome')}", dispositivo.get("nome") + " - Aberta", "Código", self.logs_endpoint)

                    time.sleep(5)

                    print(f"Fechar {dispositivo.get('nome')}")

                    # Controlar GPIO - Fechar
                    ControlarGpios.fechar(dispositivo.get('pino'))
                    
                    # Adicionar log
                    self.server_com_driver.adicionar_log(f"{dispositivo.get('nome')}",  dispositivo.get("nome") + " - Fechada", "Código", self.logs_endpoint)
                    

                    print("-" * 30)
                    break
                else:
                    print(f"Codigo errado {dispositivo.get('id')}")
            pressed = True

        GPIO.output(self.L4, GPIO.LOW)

        if pressed:
            self.input = ""

        return pressed


    def readLine(self, line, characters):
        GPIO.output(line, GPIO.HIGH)

        if(GPIO.input(self.C1) == 1):
            self.input = self.input + characters[0]
            print(self.input)

        if(GPIO.input(self.C2) == 1):
            self.input = self.input + characters[1]
            print(self.input)

        if(GPIO.input(self.C3) == 1):
            self.input = self.input + characters[2]
            print(self.input)

        GPIO.output(line, GPIO.LOW)


    def ler_keypad(self):
        if self.keypadPressed != -1:
            self.setAllLines(GPIO.HIGH)
            if GPIO.input(self.keypadPressed) == 0:
                self.keypadPressed = -1
            else:
                time.sleep(0.1)
        else:
            if not self.checkSpecialKeys():
                self.readLine(self.L1, ["7","8","9"])
                self.readLine(self.L2, ["4","5","6"])
                self.readLine(self.L3, ["1","2","3"])
                self.readLine(self.L4, ["*","0","#"])
                time.sleep(0.1)
            else:
                time.sleep(0.1)