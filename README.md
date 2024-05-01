# screenshot_bot

### Description: ###

Test assignment for True Positive Team.

This Telegram bot receives a message with a link to a website and responds with a screenshot of that website.

The bot is available to work in both private and group chats. To work in group chats, the bot needs to be granted permission to read messages:
1. Go to the dialogue with the @BotFather bot.
2. Select your bot from the list.
3. Choose the "Bot Settings" button.
4. Select the "Group Privacy" button and click "Disable."
____

## Installation and Launch ##

#### Clone the repository: ####
    git clone git@github.com:mark-rom/screenshot_bot.git

#### Navigate to the repository in the command line: ####
    cd screenshot_bot/

#### Create a .env file and fill it: ####
    touch .env
The structure for filling the .env file is presented in the example_env file.

#### Run docker-compose in detached mode: ####
    docker-compose up -d
Before executing the command, make sure that Docker is running on the machine.
____

## Technologies ##
- Python 3.10
- Python-telegram-bot 20.0a2
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose
