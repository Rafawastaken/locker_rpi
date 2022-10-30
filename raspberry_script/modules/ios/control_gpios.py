"""
    Class para controlar GPIOs
        Prints devem ser substituidos por GPIOS. 

"""
from time import sleep

class ControlarGpios:
    def controlar_pin(self, pino:int, estado:bool):
        if estado:
            print(f"Porta aberta {pino}")
        if not estado:
            print(f"Porta fechada {pino}")