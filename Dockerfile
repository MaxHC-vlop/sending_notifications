FROM python:3.9-alpine

RUN adduser --disabled-password bot-user

USER bot-user

WORKDIR /home/devman_bot

COPY requirements.txt home/devman_bot/requirements.txt
COPY .env home/devman_bot/.env
COPY main.py home/devman_bot/main.py

RUN pip install -r home/devman_bot/requirements.txt

CMD python3.9 home/devman_bot/main.py