"""
    Class para controlar GPIOs
        Prints devem ser substituidos por GPIOS. 

"""
from time import sleep

class ControlarGpios:
    def abrir_porta(self, port:int):
        try:
            print(f"Porta: {port} -> Aberta")
            return True
        except Exception as e:
            print(e)
            return False

    def fechar_porta(self, port:int):
        try:
            print(f"Porta: {port} -> Fechada")
            return True
        except Exception as e:
            print(e)
            return False