import requests
from requests.auth import HTTPBasicAuth

url = 'https://api.infobip.com/sms/1/text/single'
USR = 'VBookin'
PWD = 'Happy1234'


def send_message(to, msg, sender='VBookin'):
    payload = {
        'from': sender,
        'to': to,
        'text': msg
    }
    requests.post(url, json=payload, auth=HTTPBasicAuth(USR, PWD))
