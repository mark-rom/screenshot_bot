import asyncio
from functools import wraps
import re
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Optional, Union
import time as t

import requests as r
from PIL import Image
from pyppeteer import launch
from requests.exceptions import SSLError


MEDIA_DIR = Path(__file__).resolve().parent.parent / 'media'


def evaluation_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = t.time()
        f = await func(*args, **kwargs)
        end_time = t.time()
        duration = t.gmtime(end_time - start_time)
        seconds = duration.tm_sec + duration.tm_min * 60
        return *f, seconds
    return wrapper


def get_scheme(schemeless_link: str) -> str:
    https_link = f'https://{schemeless_link}'

    try:
        r.head(https_link)
    except SSLError:
        return f'http://{schemeless_link}'

    return https_link


async def check_link(link: str) -> str:
    """Verifies if link has http or https URI scheme. If not set one.

    Args:
        link (str): link to website like 'google.com' or 'http://google.com'

    Returns:
        str: link to website like 'http://google.com'
    """
    if not link.startswith(('http://', 'https://')):
        return get_scheme(link)

    return link


async def take_screenshot(website: str) -> Union[bytes, str]:

    browser = await launch()

    page = await browser.newPage()
    responce = await page.goto(website)
    page_title = re.split(r'<title>(.*?)<\/title>', await responce.text())[1]
    bytes_screen = await page.screenshot(
        {MEDIA_DIR: 'example.png', 'fullPage': True}
    )

    await browser.close()

    return bytes_screen, page_title


def get_file_name(link: str, tg_user: Optional[str] = None) -> str:
    # returns filename
    # параметры: дата запроса + user_id пользователя тг + домен из url запроса
    # 'http.?:\/\/w{3}?\.([\da-z\.-]+\.[a-z\.]{2,6})*\/?' - убирает www. из URL

    date = datetime.now().date()
    domain = re.split(r'http.?:\/\/([\da-z\.-]+\.[a-z\.]{2,6})*\/?', link)[1]

    if tg_user:
        return f'{date}_{tg_user}_{domain}'
    return f'{date}_{domain}'


def save_screenshot(byte_screenshot: Union[bytes, str], filename: str):
    img = BytesIO(byte_screenshot)
    img = Image.open(img)
    img.save(MEDIA_DIR / f'{filename}.png')


@evaluation_time
async def get_screenshot(link: str, tg_user: Optional[str] = None) -> None:

    link = await check_link(link)
    filename = get_file_name(link, tg_user)
    screenshot, page_title = await take_screenshot(link)
    save_screenshot(screenshot, filename)

    return screenshot, link, page_title


if __name__ == '__main__':
    asyncio.run(get_screenshot('http://google.com'))
