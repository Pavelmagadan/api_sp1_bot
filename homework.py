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

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    hw_verdict = {
        'rejected': (
            f'У вас проверили работу "{homework_name}"!\n\n'
            'К сожалению в работе нашлись ошибки.'
        ),
        'reviewing': (
            f'Работу "{homework_name}" взяли на ревью!'
        ),
        'approved': (
            f'У вас проверили работу "{homework_name}"!\n\n'
            'Ревьюеру всё понравилось, можно приступать '
            'к следующему уроку.'
        )
    }
    homework_status = homework.get('status')
    verdict = hw_verdict.get(homework_status)
    if not (homework_name and verdict):
        logging.warning(
            'функция parse_homework_status вызвана с '
            'homework_name или verdict равным None'
        )
        return 'Статус вашей работы изменился!'
    return verdict


def get_homework_statuses(current_timestamp):
    # url нужно задавать здесь для прохождения тестов
    url = (
        'https://praktikum.yandex.ru/api/user_api/'
        'homework_statuses/'
    )
    param = {'from_date': current_timestamp}
    header = {'Authorization': f'OAuth  {PRAKTIKUM_TOKEN}'}
    try:
        homework_statuses = requests.get(
            url,
            params=param,
            headers=header
        )
        return homework_statuses.json()
    except Exception:
        logging.exception(
            'Возникла ошибка при обращении к API YaPraktikum'
        )
        return {}


def send_message(message, bot_client):
    return bot_client.send_message(CHAT_ID, message)


def main():
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
    logging.debug('Запуск бота')
    send_message(
        'Бот в работе',
        bot
    )
    current_timestamp = int(time.time())
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                massage = parse_homework_status(
                    new_homework.get('homeworks')[0]
                )
                send_message(
                    massage,
                    bot
                )
                logging.info('Отправлено сообщение')
            current_timestamp = new_homework.get(
                'current_date',
                current_timestamp
            )
            time.sleep(300)
        except Exception:
            logging.exception(
                'Бот столкнулся с ошибкой'
            )
            send_message(
                'Бот столкнулся с ошибкой',
                bot
            )
            time.sleep(5)


if __name__ == '__main__':
    main()
