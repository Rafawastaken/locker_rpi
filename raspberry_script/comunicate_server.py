from time import sleep
import requests
import RPi.GPIO as GPIO

def toggle(pin, status): 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    if status:
        GPIO.output(pin, GPIO.HIGH)
    GPIO.output(pin, GPIO.LOW) 
    

def get_status():
    r = requests.get('http://127.0.0.1:5000/devices_status')
    response = r.json()
    return response

def main():
    while True:
        response = get_status()
        for device in response:
            pino = device.get("pin")
            status = device.get("estado")
            toggle(pino, status)


if __name__ == '__main__':
    main()

