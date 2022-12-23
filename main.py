import logging

import requests
import telegram

from environs import Env


DEVMAN_URL = 'https://dvmn.org/api/long_polling/'


def get_job_review_status(devman_token, timestamp):
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    payload = {
        'timestamp': timestamp
    }

    response = requests.get(DEVMAN_URL, headers=headers, params=payload)
    response.raise_for_status()

    response_content = response.json()

    return response_content


def main():
    logger = logging.getLogger(__file__)
    logging.basicConfig(level=logging.ERROR)

    env = Env()
    env.read_env()
    devman_token = env.str('DEVMAN_TOKEN')
    telegram_token = env.str('TELEGRAM_TOKEN')

    bot = telegram.Bot(telegram_token)

    updates = bot.get_updates()
    bot.send_message(text='Hi Vlad!', chat_id=533208511)

    # timestamp = None

    # while True:
    #     try:
    #         response_content = get_job_review_status(DEVMAN_URL, devman_token, timestamp)

    #         timestamp = response_content['timestamp_to_request']

    #     except requests.exceptions.ReadTimeout as error:
    #         logger.error(f'Timeout: {error}')
    #         continue

    #     except requests.exceptions.ConnectionError as error:
    #         logger.error(f'ConnectionError: {error}')
    #         continue


if __name__ == '__main__':
    main()