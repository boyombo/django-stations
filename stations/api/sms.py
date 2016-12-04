import requests
from requests.auth import HTTPBasicAuth

url = 'https://api.infobip.com/sms/1/text/single'
USR = 'QRLabs'
PWD = 'pass.p455'


def send_message(to, msg, sender='MedInfo'):
    payload = {
        'from': sender,
        'to': to,
        'text': msg
    }
    requests.post(url, json=payload, auth=HTTPBasicAuth(USR, PWD))
