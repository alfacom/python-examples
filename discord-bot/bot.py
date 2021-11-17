import asyncio
from typing import Optional, Tuple

import discord
import inflect
from config import logger


class MyBot(discord.Client):
    def __init__(self) -> None:
        super().__init__()
        self.p = inflect.engine()

    async def on_ready(self) -> None:
        logger.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message) -> None:
        if message.author.id == self.user.id:
            return

        message.content, is_for_bot = self.get_content_without_tag(message)

        if not message.channel.type.name == 'private' and not is_for_bot:
            return

        logger.debug(message)
        if message.content.startswith('count to'):
            n = await self.find_n(message)
            await self.count_to_n(message, n)

    async def count_to_n(self, message: discord.Message, n: int) -> None:
        for i in range(1, n + 1):
            res = await message.reply(self.p.number_to_words(i))
            logger.debug(res)
            await asyncio.sleep(1)

    @staticmethod
    async def find_n(message: discord.Message) -> Optional[int]:
        _, _, range_end, *_ = message.content.split()
        try:
            range_end = int(range_end)
        except ValueError as e:
            res = await message.reply("Sorry, I can't figure out to what number I should count.")
            logger.debug(res)
            logger.error(message.content, exc_info=e)
            return 0
        else:
            return range_end

    def get_content_without_tag(self, message: discord.Message) -> Tuple[str, bool]:
        tagged_for_bot = False
        if not message.channel.type.name == 'private':
            role_id = '<@&{0}>'.format(message.guild.self_role.id)
            if message.content.startswith(role_id):
                tagged_for_bot = True
                return message.content.replace(role_id, '').strip(), tagged_for_bot

            bot_id = '<@!{0}>'.format(self.user.id)
            if message.content.startswith(bot_id):
                tagged_for_bot = True
                return message.content.replace(bot_id, '').strip(), tagged_for_bot

        return message.content, tagged_for_bot
