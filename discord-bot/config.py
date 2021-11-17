import logging
from logging import handlers
from pathlib import Path

logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)

logfile = Path('discord.log')
handler = handlers.RotatingFileHandler(filename=logfile, maxBytes=1024 ** 2, backupCount=5, encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot_token = ''
