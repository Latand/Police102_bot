from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hbold

from tgbot.services.setting_default_commands import set_user_commands


async def user_start(message: Message, state: FSMContext):
    await message.reply(hbold('Вас вітає чат-бот служби "102" поліції Львівської області!'))
    await message.answer(hbold('👮 Ваше звернення буде доступно та адресується виключно працівникам поліції.'
                               '\n\n'
                               '✔ Ви надаєте згоду на обробку персональних даних працівниками поліції у службових цілях'))
    await message.answer('''
<b>Якщо хочете оформити заявку зараз - введіть свій номер телефону або натисніть кнопку "Поділитися контактом"</b>

<b><i>Приклад повідомлення:</i></b>
<pre>
0981234567
+380981234567
</pre>

<b><i>Якщо:</i></b>
<i>- бачите пересування ворогів, підозрілі предмети - повідомляйте до телеграм боту:
Знайден Ворог (@znaydenvorogbot);

- для повідомлення підрозділів Національної Поліції України про особливі позначки на дорогах та контролю за 
пересуваннями загарбницьких сил РФ - Народный месник (@ukraine_avanger_bot);

- снаряди, що не розірвались - Тарас бот (@bomb_found_bot);</i>
''', reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton('📱 Поділитися контактом', request_contact=True)
            ]
        ],
        resize_keyboard=True,
    ))
    await state.finish()
    await set_user_commands(message.bot, message.from_user.id)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
