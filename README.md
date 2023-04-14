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

LOGGER_BOT_TOKEN='super_secret'
```

## Run

```bash
python3 main.py
```

- When checking the work, the bot sends you the following message:
![screen](/pictures/screen.PNG)

## Deploy with ubuntu

- Let's create a bot.service file in the /etc/systemd/system directory:
```bash
sudo touch /etc/systemd/system/devman_bot.service
```

- Edit devman_bot.service file:
```bash
sudo nano /etc/systemd/system/devman_bot.service
```

- Fill it with the following content:
```bash
[Service]
ExecStart='path_to_interpreter' 'path_to_executable_file'
Restart=always

[Install]
WantedBy=multi-user.target
```

- Execute commands:
```bash
# daemons reload
sudo systemctl daemon-reload

# enable daemon devman_bot
sudo systemctl enable devman_bot

# start daemon devman_bot
sudo systemctl start devman_bot

# check status
sudo systemctl status devman_bot

# check process status
# grep + executable file
ps -aux | grep main.py
```

## Deploy with Docker

- Docker must be installed on the system. Help [here](https://docs.docker.com/engine/install/).

- Go to project :
```bash
cd sending_notifications/
```
- Collect the image:
```
sudo docker build -t bot .
```

- Run container:
```
sudo docker run --restart=always -d --env-file .env bot
```

- Check if container exists:
```bash
sudo docker ps
# You will see

CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS     NAMES
1234567890     bot       "/bin/sh -c 'python3…"   11 minutes ago   Up 10 minutes             name
```