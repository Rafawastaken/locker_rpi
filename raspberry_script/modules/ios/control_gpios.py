"""
    Class para controlar GPIOs
        Prints devem ser substituidos por GPIOS. 

"""
from time import sleep
import RPi.GPIO as GPIO

class ControlarGpios:

    def ligar(pino:int):
        GPIO.setup(pino, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(pino, GPIO.HIGH)

    def desligar(pino:int):
        GPIO.setup(pino, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(pino, GPIO.LOW)