from curses import baudrate
import serial

ser = serial.Serial("COM3", baudrate = 9600, timeout = 1)
ser.write("AT\r".encode())
print(ser.read())