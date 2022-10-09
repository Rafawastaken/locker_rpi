import time
import serial

port = serial.Serial(port = "COM3", baudrate=9600, timeout=1)

port.write('AT+CUSD=1,"*111#",15\r'.encode())

rcv = port.read(1000)
print(rcv.decode())

time.sleep(1)

def saldo_cartao(gsm):
    gsm.write('AT+CUSD=1,"*111#",15\r'.encode())
    resp = gsm.read(1000).decode()

    while "EUR" not in resp:
        resp = gsm.read(1000).decode()
        if x == 10: return "impossivel obter saldo, tente novamente"

        time.sleep(1)
        x = x + 1

    return resp.split("\n")[2][1:]

saldo = saldo_cartao(port)
print(saldo)