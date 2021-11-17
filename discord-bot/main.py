from bot import MyBot
from config import bot_token


if __name__ == '__main__':
    bot = MyBot()
    bot.run(bot_token)
