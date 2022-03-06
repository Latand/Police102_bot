from datetime import datetime

import pytz
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.markdown import hcode, hbold, hlink

from tgbot.infrastructure.google_sheets import ExcelForm, write_to_sheet
from tgbot.infrastructure.telegraph.abstract import FileUploader
from tgbot.misc.functions import location_url_gmaps
from tgbot.misc.states import Form
import tgbot.misc.texts


async def accept_phone_contact(message: types.Message, state: FSMContext):
    if message.contact.user_id != message.from_user.id:
        await message.reply(tgbot.misc.texts.WRONG_CONTACT_MESSAGE)
        return
    phone_number = message.contact.phone_number
    full_name = f'{message.contact.first_name} {message.contact.last_name}'
    await state.update_data(phone_number=phone_number)

    await message.reply(
        tgbot.misc.texts.PHONE_REGISTERED.format(phone_number=hcode(phone_number)) +
        tgbot.misc.texts.FULL_NAME_INSTRUCTION,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(full_name)
                ],
                [
                    KeyboardButton(message.from_user.full_name)
                ],
            ],
            resize_keyboard=True,
        ))
    await Form.FullName.set()


async def accept_phone_text(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)

    await message.reply(
        tgbot.misc.texts.PHONE_REGISTERED.format(phone_number=hcode(phone_number)) +
        tgbot.misc.texts.FULL_NAME_INSTRUCTION,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(message.from_user.full_name)
                ],
            ],
            resize_keyboard=True,
        ))
    await Form.FullName.set()


async def wrong_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    await message.reply(tgbot.misc.texts.WRONG_NUMBER_MESSAGE,
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[
                                [
                                    KeyboardButton(tgbot.misc.texts.NEXT)
                                ],
                                [
                                    KeyboardButton(tgbot.misc.texts.CANCEL)
                                ],
                            ],
                            resize_keyboard=True,
                        ))


async def cancel(message: types.Message, state: FSMContext):
    await message.reply(tgbot.misc.texts.CANCELLED, reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def process_wrong_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_number = data.get('phone_number')

    await message.reply(
        tgbot.misc.texts.PHONE_REGISTERED.format(phone_number=hcode(phone_number)) +
        tgbot.misc.texts.FULL_NAME_INSTRUCTION,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(message.from_user.full_name)
                ],
            ],
            resize_keyboard=True,
        ))
    await Form.FullName.set()


async def process_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)

    await message.reply(
        tgbot.misc.texts.FULL_NAME_REGISTERED.format(full_name=hcode(full_name)) +
        tgbot.misc.texts.ADDRESS_INSTRUCTION,
        reply_markup=ReplyKeyboardRemove()
    )
    await Form.Address.set()


async def process_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)

    await message.reply(
        tgbot.misc.texts.ADDRESS_REGISTERED.format(address=hcode(address)) +
        tgbot.misc.texts.GEOLOCATION_INSTRUCTION,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(tgbot.misc.texts.SEND_LOCATION, request_location=True)],
                [KeyboardButton(tgbot.misc.texts.SKIP)],
            ], resize_keyboard=True
        )
    )
    await Form.Geolocation.set()


async def no_geolocation(message: types.Message):
    await message.reply(tgbot.misc.texts.INVALID_LOCATION_MESSAGE)


async def skip_geolocation(message: types.Message, state: FSMContext):
    await state.update_data(geolocation='-')

    await message.reply(
        tgbot.misc.texts.NO_LOCATION_MESSAGE +
        '\n\n' +
        tgbot.misc.texts.DESCRIPTION_INSTRUCTION,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text)] for text in tgbot.misc.texts.HELP_REASONS
            ]
        )
    )
    await Form.Description.set()


async def process_geolocation(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    geolocation = location_url_gmaps(latitude, longitude)
    await state.update_data(geolocation=geolocation)

    await message.reply(
        hlink(tgbot.misc.texts.LOCATION_REGISTERED, geolocation) +
        '\n\n' +
        tgbot.misc.texts.DESCRIPTION_INSTRUCTION,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text)] for text in tgbot.misc.texts.HELP_REASONS
            ]
        )
    )
    await Form.Description.set()


async def process_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)

    await message.reply(
        tgbot.misc.texts.DESCRIPTION_REGISTERED.format(description=hcode(description)) +
        tgbot.misc.texts.PHOTO_INSTRUCTION,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[
                KeyboardButton('❌ Пропустити')
            ]],
            resize_keyboard=True
        )
    )
    await Form.Photo.set()


async def process_no_photo_text(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await message.reply(
        tgbot.misc.texts.DESCRIPTION_REGISTERED_2 +
        '\n\n' +
        tgbot.misc.texts.NEED_HELP_INSTRUCTION,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(tgbot.misc.texts.YES_HELP),
                ],
                [
                    KeyboardButton(tgbot.misc.texts.NO_HELP),
                ]
            ],
            resize_keyboard=True
        )
    )
    await Form.UrgentStatus.set()


async def process_else_no_photo(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text, photo='-')
    await message.reply(tgbot.misc.texts.PHOTO_NO_DOCUMENT_ERROR)


async def process_cancel_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo='-')

    await message.reply(
        tgbot.misc.texts.SKIPPED_PHOTO +
        '\n\n' +
        tgbot.misc.texts.NEED_HELP_INSTRUCTION,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(tgbot.misc.texts.YES_HELP),
                ],
                [
                    KeyboardButton(tgbot.misc.texts.NO_HELP),
                ]
            ],
            resize_keyboard=True
        )
    )
    await Form.UrgentStatus.set()


async def process_photo(message: types.Message, state: FSMContext, file_uploader: FileUploader):
    photo = message.photo[-1]
    await message.bot.send_chat_action(message.chat.id, 'upload_photo')
    uploaded_photo = await file_uploader.upload_photo(photo)
    await state.update_data(photo=uploaded_photo.link)

    await message.reply(
        tgbot.misc.texts.PHOTO_REGISTERED +
        '\n\n' +
        tgbot.misc.texts.NEED_HELP_INSTRUCTION,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(tgbot.misc.texts.YES_HELP),
                ],
                [
                    KeyboardButton(tgbot.misc.texts.NO_HELP),
                ]
            ],
            resize_keyboard=True
        )
    )
    await Form.UrgentStatus.set()


async def process_urgent_status(message: types.Message, state: FSMContext, google_client, config):
    urgent_status = message.text
    await state.update_data(urgent_status=urgent_status)
    data = await state.get_data()
    comment = data.get('comment')
    buttons = [
        [
            KeyboardButton(tgbot.misc.texts.SKIP)
        ]
    ]
    text = tgbot.misc.texts.ADD_COMMENT_MORE

    if comment:
        buttons.append(
            [
                KeyboardButton(tgbot.misc.texts.SAVE)
            ]
        )
        text += tgbot.misc.texts.ADDED_COMMENT.format(comment=hbold(comment))

    await message.reply(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True
        )
    )
    await Form.Comment.set()


async def process_comment(message: types.Message, state: FSMContext, google_client, config):
    await message.reply(tgbot.misc.texts.IS_BEING_REGISTERED, reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()

    if message.text == tgbot.misc.texts.SAVE:
        comment = data.get('comment') or '-'
    elif message.text == tgbot.misc.texts.SKIP:
        comment = '-'
    else:
        comment = message.text

    form = ExcelForm(
        phone_number=data.get('phone_number'),
        full_name=data.get('full_name'),
        geolocation=data.get('geolocation'),
        address=data.get('address'),
        description=data.get('description'),
        urgent_status=data.get('urgent_status'),
        photo=data.get('photo'),
        comment=comment,
        time=datetime.now(tz=pytz.timezone('Europe/Kiev')).strftime('%d/%m/%Y %X')
    )
    await write_to_sheet(
        google_client,
        excel_form=form,
        sheet_id=config.misc.sheet_id
    )
    await message.answer(tgbot.misc.texts.FINISH_REQUEST)
    await state.finish()


def register_submit_form(dp: Dispatcher):
    dp.register_message_handler(
        accept_phone_contact, content_types=types.ContentType.CONTACT,
        state='*'
    )
    dp.register_message_handler(cancel, text=tgbot.misc.texts.CANCEL, state='*')
    # dp.register_message_handler(
    #     accept_phone_text, regexp=r'^(?:\+?38)?(((\(0\d{2}\))|(\d{3}))[ \-\.]?\d{3}[ \-\.]?\d{2,3}[ \-\.]?\d{2,3})$'
    # )
    # dp.register_message_handler(wrong_number)
    # dp.register_message_handler(process_wrong_phone, text='Далі')
    dp.register_message_handler(cancel, Command('cancel'), state='*')
    dp.register_message_handler(process_full_name, state=Form.FullName)
    dp.register_message_handler(process_address, state=Form.Address)
    dp.register_message_handler(process_geolocation, state=Form.Geolocation, content_types=types.ContentType.LOCATION)
    dp.register_message_handler(skip_geolocation, text=tgbot.misc.texts.SKIP, state=Form.Geolocation)
    dp.register_message_handler(no_geolocation, state=Form.Geolocation, content_types=types.ContentType.ANY)
    dp.register_message_handler(process_description, state=Form.Description)
    dp.register_message_handler(process_photo, state=Form.Photo, content_types=types.ContentType.PHOTO)
    dp.register_message_handler(process_cancel_photo, text=tgbot.misc.texts.SKIP, state=Form.Photo)
    dp.register_message_handler(process_no_photo_text, state=Form.Photo)
    dp.register_message_handler(process_else_no_photo, state=Form.Photo, content_types=types.ContentType.ANY)
    dp.register_message_handler(process_urgent_status, state=Form.UrgentStatus)
    dp.register_message_handler(process_comment, state=Form.Comment)
