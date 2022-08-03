import requests as r
from requests.exceptions import SSLError
from re import split as splt
import time as t
from datetime import timedelta
from functools import wraps


def get_scheme(schemeless_link):
    https_link = f'https://{schemeless_link}'

    try:
        r.head(https_link)
    except SSLError:
        return f'http://{schemeless_link}'

    return https_link


def get_title(link):
    response = r.get(link)

    return splt(r'<title>(.*?)<\/title>', response.text)[1]


def my_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = t.time()
        f = func(*args, **kwargs)
        end_time = t.time()
        duration = t.gmtime(end_time - start_time)
        seconds = duration.tm_sec + duration.tm_min * 60
        return *f, seconds
    return wrapper


@my_dec
def foo():
    t1 = 'example'
    t2 = 'example1'
    t.sleep(1)
    return t2, t1


if __name__ == '__main__':
    # k, k1, k2 = foo()
    print(foo())
