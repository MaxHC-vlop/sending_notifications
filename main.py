import logging
import time

from textwrap import dedent

import requests
import telegram

from environs import Env


DEVMAN_URL = 'https://dvmn.org/api/long_polling/'

SLEEP_TIME = 10

logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def make_message(attempt):
    lesson_title = attempt['lesson_title']
    lesson_url = attempt['lesson_url']

    review_flag = attempt['is_negative']

    end_message = 'Преподавателю всё понравилось, можно приступать к следущему уроку!'

    if review_flag:
        end_message = 'К сожалению, в работе нашлись ошибки.'
    
    message = f'''\
        У Вас проверили работу «{lesson_title}».
        {end_message}
        Ваша работа: {lesson_url}
    '''

    message = dedent(message)

    return message


def main():
    logging.basicConfig(
        level=logging.DEBUG,
    )

    env = Env()
    env.read_env()
    devman_token = env.str('DEVMAN_TOKEN')
    telegram_token = env.str('TELEGRAM_TOKEN')
    logger_bot_token = env.str('LOGGER_BOT_TOKEN')
    chat_id = env.str('TELEGRAM_CHAT_ID')

    bot = telegram.Bot(telegram_token)
    logger_bot = telegram.Bot(logger_bot_token)
    logger.addHandler(TelegramLogsHandler(logger_bot, chat_id))
    logger.info('Бот запущен')

    timestamp = None

    while True:
        try:
            x = 1 / 0
            headers = {
                'Authorization': f'Token {devman_token}'
            }
            payload = {
                'timestamp': timestamp
            }

            response = requests.get(DEVMAN_URL, headers=headers, params=payload)
            response.raise_for_status()

            review_content = response.json()

            if review_content['status'] == 'found':
                attempts = review_content['new_attempts']
                timestamp = review_content['last_attempt_timestamp']

                for attempt in attempts:
                    message = make_message(attempt)
                    bot.send_message(text=message, chat_id=chat_id)

            else:
                timestamp = review_content['timestamp_to_request']
        
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

        except Exception as error:
            logger.info('Бот упал с ошибкой:')
            logger.exception(error)

            break


if __name__ == '__main__':
    main()