import logging
import os
import time

from dotenv import load_dotenv

import requests

from twilio.rest import Client

load_dotenv()


ACCOUNT_SID_TWILIO = os.getenv('ACCOUNT_SID_TWILIO')
TOKEN_TWILIO = os.getenv('TOKEN_TWILIO')
client = Client(ACCOUNT_SID_TWILIO, TOKEN_TWILIO)

TOKEN_VK = os.getenv('TOKEN_VK')
BASE_URL_VK = 'https://api.vk.com'
API_V = '5.92'

NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'v': API_V,
        'access_token': TOKEN_VK,
        'fields': 'online'
    }
    url = '{}/method/users.get'.format(BASE_URL_VK)
    try:
        status = requests.post(url=url, params=params)
        return status.json()['response'][0]['online']
    except Exception:
        logging.exception('Error')


def send_sms(sms_text):
    message = client.messages.create(
        to=NUMBER_TO,
        from_=NUMBER_FROM,
        body=sms_text
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
