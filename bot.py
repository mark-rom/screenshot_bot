import os
from datetime import datetime as dt

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, MessageHandler, filters)

from logger import logger as log
from screens.exceptions import ScreenshotError, WHOISError
from screens.models import Statistics, User, get_or_create, session
from screens.screenshot import take_screenshot
from screens.whois import parce_whois

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


async def start(update, context):

    text = """
    Привет! Я делаю скриншоты веб-страниц по ссылкам, которые вы пришлете.
    Чтобы начать работу, пришлите мне любую ссылку, например wikipedia.org
    """

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text,
        reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(
                    text='Добавить бота в ваш чат',
                    url='http://t.me/{}?startgroup=true'.format(
                        context.bot.bot.username
                    )
                )]]
            )
        )


async def send_screenshot(update, context):

    link = update.message.text

    text = 'Запрос принят к обработке'
    dummy = await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text,
        reply_to_message_id=update.message.message_id
    )
    user_instance = get_or_create(
        session, User, tg_id=update.effective_user.id
    )
    new_stat = Statistics(
            user_id=user_instance.id,
            website=link,
            date=dt.now(),
            success=False
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
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(
                    'Подробнее', callback_data=f'{website}'
                )]]
            )
        )

        log.info(f'Успешный запрос к {website}')
        new_stat.success = True

    except ScreenshotError as e:
        log.error(e)
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id, text=e.args[0],
            message_id=dummy.message_id
        )

    except Exception as e:
        log.exception(e)
        text = 'Произошла ошибка. Попробуйте сделать запрос позже'
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id, text=text,
            message_id=dummy.message_id
        )

    finally:
        session.add(new_stat)
        session.commit()


async def whois_button(update, context):

    whois = 'Не удалось получить IP-адрес указанного сайта'
    query = update.callback_query

    try:
        whois = await parce_whois(query.data)

    except WHOISError as e:
        log.error(e)

    except Exception as e:
        log.exception(e)

    await query.answer(text=whois, show_alert=True)


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
    send_screenshot
)
callback_query_answ = CallbackQueryHandler(whois_button)


def main():

    if not check_tokens():
        return
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(start_handler)
    application.add_handler(get_screen)
    application.add_handler(callback_query_answ)
    application.run_polling()


if __name__ == '__main__':
    main()
