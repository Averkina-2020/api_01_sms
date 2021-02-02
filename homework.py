import os
import time

from dotenv import load_dotenv

import requests

from twilio.rest import Client

load_dotenv()


account_sid_twilio = os.getenv('ACCOUNT_SID_TWILIO')
token_twilio = os.getenv('TOKEN_TWILIO')
client = Client(account_sid_twilio, token_twilio)

token_vk = os.getenv('TOKEN_VK')
BASE_URL_VK = 'https://api.vk.com/method/users.get'
API_V = '5.92'

number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')


def get_status(user_id):
    params = {
        'user_id': user_id,
        'v': API_V,
        'access_token': token_vk,
        'fields': 'online'
    }
    status = requests.post(BASE_URL_VK, params=params)
    return status.json()['response'][0]['online']


def sms_sender(sms_text):
    message = client.messages.create(
        to=number_to,
        from_=number_from,
        body=sms_text
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
