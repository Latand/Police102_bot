curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
dnf install -y docker-compose
systemctl start docker
echo "Введите пароль для временной базы данных Redis"
read REDIS_PASSWORD
echo "Пришлите Токен Бота"
read BOT_TOKEN
echo "Пришлите ID файла гугл таблиц"
read SHEET_ID
echo "Пришлите ID Администратора бота"
read ADMINS

echo "BOT_CONTAINER_NAME=lviv102_bot
BOT_IMAGE_NAME=lviv102_bot
BOT_NAME=Lviv102_bot
USE_REDIS=True

REDIS_PASSWORD=${REDIS_PASSWORD}
ADMINS=${ADMINS}
SHEET_ID=${SHEET_ID}
BOT_TOKEN=${BOT_TOKEN}" >> .env
docker-compose up