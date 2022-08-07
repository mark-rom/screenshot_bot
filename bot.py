import os
from datetime import datetime as dt

from dotenv import load_dotenv
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          filters)

from logger import logger as log
from screens.exceptions import ScreenshotError
from screens.models import Statistics, session
from screens.screenshot import take_screenshot

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


async def start(update, context):
    text = """
    Привет! Я делаю скриншоты веб-страниц по ссылкам которые вы пришлете.
    Чтобы начать работу, пришлите мне любую ссылку, например wikipedia.org
    """

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text
        )


async def send_message(update, context):

    link = update.message.text

    text = 'Запрос принят к обработке'
    dummy = await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text,
        reply_to_message_id=update.message.message_id
    )

    new_stat = Statistics(
            user_id=update.effective_user.id,
            website=link,
            date=dt.now().date()
        )

    try:
        screen_bytes, website, page_title, ev_time = await take_screenshot(
            link, tg_user=update.effective_user.id
        )
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=dummy.message_id
        )
        await context.bot.send_photo(
            photo=screen_bytes,
            caption='{}\n\nВеб-сайт: {}\n\nВремя обработки: {} сек.'.format(
                page_title, website, ev_time
            ),
            chat_id=update.effective_chat.id,
        )

        log.info(f'Успешный запрос к {website}')
        new_stat.success = True

    except ScreenshotError as e:
        log.error(e)
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id, text=e.args[0],
            message_id=dummy.message_id
        )
        new_stat.success = False

    except Exception as e:
        log.exception(e)

    finally:
        session.add(new_stat)
        session.commit()


def check_tokens():
    if not BOT_TOKEN:
        log.critical(
            'Переменная окружения BOT_TOKEN не задана. Бот выключен'
        )
        return False

    return True


start_handler = CommandHandler('start', start)
get_screen = MessageHandler(
    filters.Regex(r'.*?([\da-z\.-]+\.[a-z\.]{2,6})*\/?'),
    send_message
)


def main():
    if not check_tokens():
        return
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(start_handler)
    application.add_handler(get_screen)
    application.run_polling()


if __name__ == '__main__':
    main()
