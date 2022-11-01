"""
    Class para controlar GPIOs
        Prints devem ser substituidos por GPIOS. 

"""
from time import sleep
# import RPi.GPIO as GPIO

class ControlarGpios:
    def __init__(self):
        pass
    #     GPIO.setwarnings(False)
    #     GPIO.setmode(GPIO.BOARD)

    # def ligar(self, pino:int):
    #     GPIO.setup(pino, GPIO.OUT, initial=GPIO.LOW)
    #     GPIO.output(pino, GPIO.HIGH)
    #     print("LIGAOD", str(pino))

    # def desligar(self, pino):
    #     GPIO.setup(pino, GPIO.OUT, initial=GPIO.LOW)
    #     GPIO.output(pino, GPIO.LOW)
    #     print("DESLIGADO", str(pino))