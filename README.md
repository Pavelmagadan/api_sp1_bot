# Telegram-bot проверки статуса домашней работы

## Описание проекта
Бот-асcистент используется для оповещения об изменения статуса домашней работы через мессенджер Telegram.
Для мониторинга статуса ДР бот опрашивает API Яндекс.Практикум.

## Действия для развертывания приложения
1. Установите зависимости: `pip install -r requirements.txt`.
2. Добавите файл `api_sp1_bot/.env` и заполните в нем настройки:
```
TELEGRAM_TOKEN = <telegram_token>
TELEGRAM_CHAT_ID = <telegram_chat_id>
PRAKTIKUM_TOKEN = <yandex_prakticum_token>
```
3. Запустите файл `api_sp1_bot/homework.py`.
