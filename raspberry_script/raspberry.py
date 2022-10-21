from modules.gsm.sim900_driver import GSM_Comunication


gsm = GSM_Comunication("COM3")
saldo = gsm.saldo_cartao()

print(saldo)