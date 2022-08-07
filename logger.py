import logging
import os

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
handler = logging.FileHandler(
    os.path.join('logs/bot.log'),
    encoding='utf-8'
)
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
