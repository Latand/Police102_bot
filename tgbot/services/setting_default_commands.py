from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_user_commands(bot: Bot, chat_id: int):
    commands = [BotCommand('start', 'Надіслати звернення')]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeChat(chat_id),
    )
