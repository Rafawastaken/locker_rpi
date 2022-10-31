"""
    Class para controlar GPIOs
        Prints devem ser substituidos por GPIOS. 

"""
from time import sleep

class ControlarGpios:
    def ligar(self, pino:int):
        print("LIGAOD", str(pino))

    def desligar(self, pino):
        print("DESLIGADO", str(pino))