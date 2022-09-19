import requests
import json

file = open("creds.json")
data = json.load(file)

auth = ( 
    data['username'],
    data['password']
)


r = requests.get('http://127.0.0.1:5000/devices_status', auth = auth)
print(r.status_code, r.text)