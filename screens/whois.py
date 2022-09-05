from re import split
from typing import Dict

import asyncio
import aiohttp

from .exceptions import WHOISError


WHOIS_URL = 'http://ip-api.com/json/'
WHOIS_FIELDS = '?fields=status,continent,country,city,isp,org,query'


async def get_whois(domain: str) -> Dict:
    """Makes get request to get WHOIS information of given website.

    Args:
        domain (str): Website without scheme, e.g. www.google.com

    Returns:
        Dict: Responce with WHOIS data. Has next fields: status, continent,
        country, city, isp, org, query.
    """
    session = aiohttp.ClientSession()

    try:
        responce = await session.get(WHOIS_URL+domain+WHOIS_FIELDS)
    except aiohttp.ClientError:
        msg = f'Сайт "{WHOIS_URL}" недоступен'
        raise WHOISError(msg)

    session.close()

    return await responce.json()


async def parce_whois(website: str) -> str:
    """Recieves full website URL and returns string with WHOIS data of website.

    Args:
        website (str): URL with scheme.

    Returns:
        str: String of WHOIS data with description. The data are IP-address,
        Continent, Country,  City, Internet Service Provider and Owner
        of given website.
    """

    clear_domain = split(
        r'http.?:\/\/([\da-z\.-]+\.[a-z\.]{2,6})*\/?',
        website
    )[1]
    responce = await get_whois(clear_domain)

    status = responce['status']

    if not status == 'success':
        return 'Не удалось получить информацию, status !=  success'

    return '''IP: {}\n\nКонтинент: {}\nСтрана: {}\nГород: {}\n
Провайдер: {}\nОрганизация: {}'''.format(
        responce.get('query'), responce.get('continent'),
        responce.get('country'), responce.get('city'),
        responce.get('isp'), responce.get('org')
    )


async def main():
    print(await parce_whois('https://www.google.com'))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
