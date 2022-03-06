curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
dnf install -y docker-compose
systemctl start docker
echo "Введите пароль для временной базы данных Redis, Пример: oigurgnv2j3o4igoi2132j3rtoi4ng"
read REDIS_PASSWORD
echo "Пришлите Токен Бота, Пример: 5048102218:AACYKyPlsMa2AfCnxk0KAHNiFgNR9w7GdsI"
read BOT_TOKEN
echo "Пришлите ID файла гугл таблиц, Пример: 1ZssvAzTked5qsJ-eTMfimB3LluUOMVmUy-ymxOuvSWc"
read SHEET_ID
echo "Пришлите ID Администратора бота, Пример: 939495558"
read ADMINS
echo "Введите название города на латинице в нижнем регистре, Пример: lviv"
read CITY

echo "BOT_CONTAINER_NAME=${CITY}102_bot
BOT_IMAGE_NAME=${CITY}102_bot
BOT_NAME=${CITY}102_bot
USE_REDIS=True

REDIS_PASSWORD=${REDIS_PASSWORD}
ADMINS=${ADMINS}
SHEET_ID=${SHEET_ID}
BOT_TOKEN=${BOT_TOKEN}" >> .env
docker-compose up