# Sending notifications

Get verification notification from bot.

## How to install

- Сlone this repository:
```bash
git clone git@github.com:MaxHC-vlop/sending_notifications.git
```
- You must have python3.9 (or higher) installed.

- Create a virtual environment on directory project:
```bash
python3 -m venv env
 ```
- Start the virtual environment:
```bash
. env/bin/activate
```
- Then use pip to install dependencies:
```bash
pip install -r requirements.txt
```
Create `DEVMAN_TOKEN`, `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID` variables in `.env` file given by [BotFather](https://t.me/BotFather) and [Devman](https://dvmn.org/api/docs/) also provide telegram chat id:

```
DEVMAN_TOKEN='super_secret'

TELEGRAM_TOKEN='super_secret'

TELEGRAM_CHAT_ID='your_chat_id'
```

## Run

```bash
python3 main.py
```

- When checking the work, the bot sends you the following message:
![screen](/pictures/screen.PNG)