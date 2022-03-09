from aiogram.utils.markdown import hcode, hbold, hitalic, hunderline

SELECTED_REGION = 'Львівської області'
DOUBLE_NEW_LINE = '\n\n'

WELCOME_MESSAGE = 'Вас вітає чат-бот служби "102" поліції {region}!'.format(region=SELECTED_REGION)
ACCEPTANCE_MESSAGE = (
    '👮 Ваше звернення буде доступно та адресується виключно працівникам поліції.'
    '\n\n'
    '✔ Ви надаєте згоду на обробку персональних даних працівниками поліції у службових цілях'
)
OR_CANCEL = 'Або натисніть /cancel щоб скасувати звернення.'

START_REQUEST_MESSAGE = (
        hbold('Якщо хочете оформити заявку зараз - натисніть кнопку "Поділитися контактом"') +
        DOUBLE_NEW_LINE +
        '<i><b>Якщо:</b></i>'
        '\n' +
        hitalic('- бачите пересування ворогів, підозрілі предмети - повідомляйте до телеграм боту: @stop_russian_war_bot') +
        '\n'
)
SHARE_CONTACT = '📱 Поділитися контактом'
WRONG_CONTACT_MESSAGE = 'Вам необхідно надіслати ваш контакт, а не чужий.'
PHONE_REGISTERED = 'Номер {phone_number} зареєстровано.' + DOUBLE_NEW_LINE
FULL_NAME_INSTRUCTION = (
        'Тепер введіть ПІБ Заявника, або скористайтесь кнопками, щоб надіслати один із запропонованих варіантів' +
        DOUBLE_NEW_LINE +
        'Приклад ' + hcode('Телеграмченко Анастасія Сергіївна') +
        DOUBLE_NEW_LINE + OR_CANCEL
)
WRONG_NUMBER_MESSAGE = (
    'Неправильно набраний номер, введіть правильний номер '
    'мобільного телефону або натисніть далі щоб продовжити з цим, або Скасувати'
)
NEXT = 'Далі'
CANCEL = '❌ Скасувати'
CANCELLED = 'Скасовано'
FULL_NAME_REGISTERED = 'ПІБ: {full_name} зареєстровано.' + DOUBLE_NEW_LINE
ADDRESS_INSTRUCTION = (
        'Тепер введіть ' + hbold('Адресу пригоди (події)') +
        DOUBLE_NEW_LINE +
        'Приклад ' + hcode('Район, Населений пункт, Вулиця, Будинок, Квартира') +
        DOUBLE_NEW_LINE + OR_CANCEL
)

ADDRESS_REGISTERED = 'Адресу: {address} зареєстровано.' + DOUBLE_NEW_LINE

GEOLOCATION_INSTRUCTION = (
        'Тепер надішліть ' + hbold('геолокацію для уточнення адреси') +
        DOUBLE_NEW_LINE + OR_CANCEL
)

SEND_LOCATION = '🌎 Надіслати геолокацію'
SKIP = '❌ Пропустити'
INVALID_LOCATION_MESSAGE = 'Ви надіслали не геолокацію. Будь ласка натисніть кнопку нижче, щоб надіслати геолокацію'

HELP_REASONS = [
    "Злочин проти життя та здоров'я",
    "Злочин проти власності/майна",
    "Раптова смерть",
    "Викрадення авто",
    "ДТП з травмованими",
    "Інша подія",
]

NO_LOCATION_MESSAGE = 'Геолокацію не надіслано.'

DESCRIPTION_INSTRUCTION = (
        'Тепер виберіть ' + hbold('короткий опис події, що сталася') +
        DOUBLE_NEW_LINE + OR_CANCEL
)
LOCATION_REGISTERED = 'Геолокацію зареєстровано.'
DESCRIPTION_REGISTERED = 'Опис події: {description} зареєстровано.' + DOUBLE_NEW_LINE

PHOTO_INSTRUCTION = 'Прикріпіть фото, або натисніть кнопку ' + hbold("Пропустити")
DESCRIPTION_REGISTERED_2 = 'Коментар/опис події був добавлен.'
NEED_HELP_INSTRUCTION = 'Потребуєте швидкої медичної допомоги'
YES_HELP = '✔ Потребує швидкої медичної допомоги'
NO_HELP = '❌ Не потребує швидкої медичної допомоги'

PHOTO_NO_DOCUMENT_ERROR = (
        '⚠️ Надішліть будь ласка фотографію, ' + hunderline('не документ') + ' або натисніть кнопку Пропустити'
)
SKIPPED_PHOTO = 'Відправку фото пропущено.'
PHOTO_REGISTERED = 'Фото зареєстровано.'

ADD_COMMENT_MORE = (
        'Бажаєте добавити коментар/опис події? '
        'Введіть в наступному повідомленні або натисніть Пропустити.' +
        DOUBLE_NEW_LINE
)
SAVE = '✅ Зберегти'
ADDED_COMMENT = 'Ваш коментар: {comment}. '
IS_BEING_REGISTERED = 'Реєструю ...'
FINISH_REQUEST = (
        'За вашим повідомленням буде забезпечено відповідне реагування нарядами поліції.' +
        DOUBLE_NEW_LINE +
        'Для того, щоб зареєструвати ще одне звернення, натисніть /start'
)
