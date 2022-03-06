# Ukrainian Police Bot

## Описание
Бот создавался для того, чтобы сделать возможным подачу обращений в Полицию Украины (вместо звонка по номеру 102), в какой-либо из областей. 
Бот собирает данные от пользователей и передает их полиции области.
Данные бот сохраняет в Google-таблицах.

## Установка
1. Раздобудьте файл `config.json`:
   1. (Создать) Войти в аккаунт Google.
   2. Зайти в консоль - [console.cloud.google.com](https://console.cloud.google.com/).
   3. Создать новый проект (не важно как назовете),
   4. Включить работу с Google Sheets - [console.cloud.google.com/marketplace...](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com?q=search&referrer=search).
   5. Включить работу с Google Drive API - [console.cloud.google.com/apis/api/drive...](https://console.cloud.google.com/apis/api/drive.googleapis.com/overview).
   6. Взять Данные для доступа к АПИ - [console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials).
       1. Создать Service Account - "Ввести данные"
       2. Зайти в аккаунт и создать ключ - "скачать JSON"
2. Закиньте файл `config.json` в папку `tgbot`.
3. Создайте файл в Google Sheets, сохраните его ID:
   1. Скопируйте ссылку на файл: `https://docs.google.com/spreadsheets/d/1xOuB3TMfLluUOsZssvJ-eiy-ymvmAzTked5qMVmUSWc/edit#gid=0`.
   2. В ней между `/d/` и `/edit` содержится текст - это и есть ID: `1xOuB3TMfLluUOsZssvJ-eiy-ymvmAzTked5qMVmUSWc`. Запомните его.
4. Придумайте пароль для Redis, какой-то длинный и сложный.
5. Получите токен для своего бота в [@Botfather](https://t.me/botfather).
6. Получите ID своего аккаунта (для айди админа) в боте [@ShowJsonBot](https://t.me/ShowJsonBot).
7. Загрузите все файлы на Сервер (ОС - Ubuntu/Fedora).
8. (Не обязательно) Измените текст под тот, что вам больше нравится, в файле `tgbot/misc/texts.py`.
9. Запустите установку бота командой `sh install-fedora.sh` ИЛИ `sh install-ubuntu.sh`.
10. Введите те данные, что раздобыли ранее.