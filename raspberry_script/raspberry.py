from modules.gsm.sim900_driver import GSM_Comunication
import json


def main():
    creds = json.load("creds.json")
    print(creds)

if __name__ == '__main__':
    main()


