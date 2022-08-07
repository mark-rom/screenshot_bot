import asyncio
from datetime import datetime
from functools import wraps
from pathlib import Path
from re import split
from time import gmtime, time
from typing import Callable, Optional, Tuple, Union

import requests as r
from pyppeteer import launch
from pyppeteer.errors import PageError, TimeoutError
from requests.exceptions import ConnectionError, SSLError

from screens.exceptions import ScreenshotError

MEDIA_DIR = Path(__file__).resolve().parent.parent / 'media'


def evaluation_time(func: Callable) -> tuple():
    """Simple decorator to measure the execution time of func.

    Args:
        func (Callable): function must return tuple.

    Returns:
        tuple: unpacked return of func, execution time in seconds.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):

        start_time = time()
        f = await func(*args, **kwargs)
        end_time = time()

        duration = gmtime(end_time - start_time)
        seconds = duration.tm_sec + duration.tm_min * 60

        return *f, seconds

    return wrapper


def check_link(link: str) -> str:
    """Verifies if given link has http or https URI scheme. If not sets one.

    Args:
        link (str): Website's URL like 'google.com' or 'http://google.com'.

    Returns:
        str: Website's URL like 'http://google.com'.
    """

    if not link.startswith(('http://', 'https://')):
        https_link = f'https://{link}'
        try:
            r.head(https_link)

        except SSLError:
            return f'http://{link}'

        except ConnectionError:
            msg = 'Страница не найдена'
            raise ScreenshotError(msg)

        return https_link

    return link


def get_file_name(link: str, tg_user: Optional[str] = None) -> str:
    """Creates name for screenshot with current date, websites domain and user_id.

    Args:
        link (str): Website's URL with http or https schema.
        tg_user (Optional[str], optional): If given adds telegram user_id
        to screenshots's name. Defaults to None.

    Returns:
        str: screenshots's name in format date_userid_domain.
        Default date_domain.
    """

    date = datetime.now().date()
    domain = split(r'http.?:\/\/([\da-z\.-]+\.[a-z\.]{2,6})*\/?', link)[1]

    if tg_user:
        return f'{date}_{tg_user}_{domain}.png'
    return f'{date}_{domain}.png'


@evaluation_time
async def take_screenshot(
    website: str, tg_user: Optional[str] = None
) -> Tuple[Union[bytes, str], str, str]:
    """Takes screenshot of given website and saves it to media/ dir.

    Args:
        website (str): URL of existing website.
        tg_user (Optional[str], optional): Telegram uses ir. Defaults to None.

    Returns:
        Tuple[Union[bytes, str], str, str]: A Tuple of byte-type image,
        website URL, website_title.
    """

    browser = await launch(
        executablePath='/usr/bin/google-chrome-stable',
        headless=True,
        args=['--no-sandbox']
    )
    page = await browser.newPage()
    website = check_link(website)

    try:
        await page.goto(website, dict(timeout=30000))

    except PageError:
        msg = 'Ошибка при загрузке страницы'
        raise ScreenshotError(msg)

    except TimeoutError:
        msg = 'Превышено время ожидания ответа'
        raise ScreenshotError(msg)

    screenshot = await page.screenshot(
        {'path': MEDIA_DIR / get_file_name(website, tg_user)}
    )
    page_title = await page.title()

    await browser.close()

    return screenshot, website, page_title


if __name__ == '__main__':
    asyncio.run(take_screenshot('https://google.com'))
