import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config


class BotAdminFilter(BoundFilter):
    key = 'is_bot_admin'

    def __init__(self, is_bot_admin: typing.Optional[bool] = None):
        self.is_bot_admin = is_bot_admin

    async def check(self, obj):
        if self.is_bot_admin is None:
            return False
        config: Config = obj.bot.get('config')

        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_bot_admin
