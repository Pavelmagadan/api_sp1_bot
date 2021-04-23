import logging
import os
import time
from logging.handlers import RotatingFileHandler

import requests
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    handlers=[
        RotatingFileHandler(
            'homework_logger.log',
            encoding='UTF-8',
            maxBytes=5000000,
            backupCount=2
        )
    ]
)

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):
    homework_name = homework['homework_name']
    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    elif homework['status'] == 'reviewing:':
        verdict = 'Работу взяли на ревью.'
    else:
        verdict = (
            'Ревьюеру всё понравилось, можно приступать '
            'к следующему уроку.'
        )
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    param = {'from_date': current_timestamp}
    header = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    homework_statuses = requests.get(url, params=param, headers=header)
    return homework_statuses.json()


def send_message(message, bot_client):
    return bot_client.send_message(CHAT_ID, message)


def main():
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
    logging.debug('Запуск бота')
    current_timestamp = int(time.time())
    print(current_timestamp)
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(new_homework.get('homeworks')[0]),
                    bot
                )
                logging.info('Отправлено сообщение')
            current_timestamp = new_homework.get(
                'current_date',
                current_timestamp
            )
            print(current_timestamp)
            time.sleep(300)

        except Exception as e:
            logging.error(
                f'Бот столкнулся с ошибкой: {e.__class__.__name__}: {e}'
            )
            send_message(
                f'Бот столкнулся с ошибкой: {e.__class__.__name__}: {e}',
                bot
            )
            time.sleep(5)


if __name__ == '__main__':
    main()
