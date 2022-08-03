import os

from dotenv import load_dotenv
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          filters)

from screens.screenshot import get_screenshot

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


async def send_dummy_message(update, context):

    link = update.message.text

    text = 'Запрос принят к обработке'
    # log.error(f'Введена нечисловая строка: {query}')
    dummy = await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text
    )

    screen_bytes, website, page_title, ev_time = await get_screenshot(link, tg_user=update.effective_user.id)

    await context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=dummy.message_id
    )
    await context.bot.send_photo(
        photo=screen_bytes,
        caption=f'{page_title}\n\nВеб-сайт: {website}\n\nВремя обработки: {ev_time} сек.',
        chat_id=update.effective_chat.id,
    )


def check_tokens():
    if not BOT_TOKEN:
        # log.critical(
        #     'Переменная окружения TG_TOKEN не задана. Бот выключен'
        # )
        return False

    return True


start_handler = CommandHandler('start', start)
get_screen = MessageHandler(
    filters.TEXT,
    send_dummy_message
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
