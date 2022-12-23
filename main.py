import time

import requests

from environs import Env


DEVMAN_URL = 'https://dvmn.org/api/long_polling/'


def main():
    env = Env()
    env.read_env()
    devman_token = env.str('DEVMAN_TOKEN')

    headers = {'Authorization': f'Token {devman_token}'}
    payload = {'timestamp': 100}

    while True:
        response = requests.get(DEVMAN_URL, headers=headers)
        response.raise_for_status()
    
        print(response.json())


if __name__ == '__main__':
    main()