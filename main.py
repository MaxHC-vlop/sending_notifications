import logging
import time

import requests
import telegram

from environs import Env


DEVMAN_URL = 'https://dvmn.org/api/long_polling/'

SLEEP_TIME = 10


def get_job_review_status(url, devman_token, timestamp):
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    payload = {
        'timestamp': timestamp
    }

    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()

    response_content = response.json()

    return response_content



def make_message(attempt):
    timestamp = attempt['timestamp']
    lesson_title = attempt['lesson_title']
    lesson_url = attempt['lesson_url']

    review_flag = attempt['is_negative']

    end_message = 'Преподавателю всё понравилось, можно приступать к следущему уроку!'

    if review_flag:
        end_message = 'К сожалению, в работе нашлись ошибки.'
    
    message = (
        f'У Вас проверили работу «{lesson_title}»\n'
        f'{end_message}\n'
        f'Ваша работа: {lesson_url}'
    )

    return message


def main():
    logger = logging.getLogger(__file__)
    logging.basicConfig(level=logging.ERROR)

    env = Env()
    env.read_env()
    devman_token = env.str('DEVMAN_TOKEN')
    telegram_token = env.str('TELEGRAM_TOKEN')
    chat_id = env.str('TELEGRAM_CHAT_ID')

    bot = telegram.Bot(telegram_token)

    timestamp = None

    while True:
        try:
            response_content = get_job_review_status(DEVMAN_URL, devman_token, timestamp)

            response_status = 'found'
            response_flag = response_content['status'] == response_status

            if response_flag:
                attempts = response_content['new_attempts']

                for attempt in attempts:
                    message = make_message(attempt)
                    bot.send_message(text=message, chat_id=chat_id)

            if not response_flag:
                timestamp = response_content['timestamp_to_request']
        
        except requests.exceptions.ReadTimeout as error:
            logger.error(f'Timeout: {error}')
            continue

        except requests.exceptions.ConnectionError as error:
            logger.error(f'ConnectionError: {error}')
            time.sleep(SLEEP_TIME)
            continue

        except requests.exceptions.HTTPError as error:
            logger.error(f'HTTPError: {error}')
            continue

        except telegram.error.NetworkError as error:
            logger.error(f'telegram.NetworkError: {error}')
            time.sleep(SLEEP_TIME)
            continue


if __name__ == '__main__':
    main()