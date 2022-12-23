import logging

import requests

from environs import Env


DEVMAN_URL = 'https://dvmn.org/api/long_polling/'


def main():
    logger = logging.getLogger(__file__)
    logging.basicConfig(level=logging.ERROR)

    env = Env()
    env.read_env()
    devman_token = env.str('DEVMAN_TOKEN')

    headers = {'Authorization': f'Token {devman_token}'}
    payload = {'timestamp': 100}

    while True:
        try:
            response = requests.get(DEVMAN_URL, headers=headers)
            response.raise_for_status()

            print(response.json())
        except requests.exceptions.ReadTimeout as error:
            logger.error(f'Timeout: {error}')


if __name__ == '__main__':
    main()