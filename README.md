# screenshot_bot

### Описание: ###

Тестовое задание от True Positive Team.

Этот телеграм-бот получает сообщение со ссылкой на сайт и отпрвляет в ответ скриншот этого сайта.

## Установка и запуск ##

### Клонируйте репозиторий: ###
    git clone git@github.com:mark-rom/screenshot_bot.git

### Перейдите в репозиторий в командной строке: ###
    cd screenshot_bot/

### Создайте файл .env и заполните его: ###
    touch .env
Структура заполнения .env файла представлена в файле example_env

### Запустите docker-compose в detach-режиме: ###
    docker-compose up -d
Перед выполнением команды убедитесь, что на машине работает приложение Docker.
____

## Технологии ##
- Python 3.7
- Python-telegram-bot 20.0a2
- PostgreSQL
- SQLAlchemy
- Docker
- Docker-compose
____