import logging

import requests
import telegram

from environs import Env


DEVMAN_URL = 'https://dvmn.org/api/long_polling/'


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


def main():
    logger = logging.getLogger(__file__)
    logging.basicConfig(level=logging.ERROR)

    env = Env()
    env.read_env()
    devman_token = env.str('DEVMAN_TOKEN')
    telegram_token = env.str('TELEGRAM_TOKEN')

    bot = telegram.Bot(telegram_token)

    timestamp = None

    while True:
        try:
            response_content = get_job_review_status(DEVMAN_URL, devman_token, timestamp)

            response_status = 'found'
            flag = response_content['status'] == response_status

            if flag:
                new_attempts = response_content['new_attempts'][0]

                timestamp = new_attempts['timestamp']
                lesson_title = new_attempts['lesson_title']
                lesson_url = new_attempts['lesson_url']

                flag = new_attempts['is_negative']

                end_message = 'Преподавателю всё понравилось, можно приступать к следущему уроку!'
                if flag:
                    end_message = 'К сожалению, в работе нашлись ошибки.'
                
                message = (
                    f'У Вас проверили работу «{lesson_title}»\n'
                    f'{end_message}\n'
                    f'Ваша работа: {lesson_url}'
                )

                bot.send_message(text=message, chat_id=533208511)
            else:
                timestamp = response_content['timestamp_to_request']
        
        except requests.exceptions.ReadTimeout as error:
            logger.error(f'Timeout: {error}')
            continue

        except requests.exceptions.ConnectionError as error:
            logger.error(f'ConnectionError: {error}')
            continue


if __name__ == '__main__':
    main()