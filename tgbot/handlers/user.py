from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hbold

from tgbot.misc.texts import WELCOME_MESSAGE, ACCEPTANCE_MESSAGE, START_REQUEST_MESSAGE, SHARE_CONTACT
from tgbot.services.setting_default_commands import set_user_commands


async def user_start(message: Message, state: FSMContext):
    await message.reply(hbold(WELCOME_MESSAGE))
    await message.answer(hbold(ACCEPTANCE_MESSAGE))
    await message.answer(START_REQUEST_MESSAGE, reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(SHARE_CONTACT, request_contact=True)
            ]
        ],
        resize_keyboard=True,
    ))
    await state.finish()
    await set_user_commands(message.bot, message.from_user.id)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
