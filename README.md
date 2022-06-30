# numbers_testtask

Привет, меня зовут Стас! И это приложения создано в рамках тестового задания для компании Numbers.
Данное приложение умеет получать курсы валют, получать данные из таблиц Google Sheet API,
отправлять уведомления в телеграмм бот и отображать заказы из таблицы на своем сервере по адерсу <localhost:3000>.

Требования:
1. Docker ([install](https://docs.docker.com/engine/install/))
2. Docker-compose ([install](https://docs.docker.com/compose/install/))

Запуск приложения:
Сначала скачайте репозиторий приложения на локальную машину
```bash
git clone git@github.com:stanbychkov/numbers_testtask.git
````
Потом создайте файл .env в главном руте репозитория со следующими переменными и заполните поля, где есть <>:
````
#Django
DJANGO_SECRET_KEY='p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs'
DJANGO_DEBUG=False
#Domain
DOMAIN_NAME=127.0.0.1
#Postgresql
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=<postgres_username>
POSTGRES_PASSWORD=<postgres_password>
DJANGO_DATABASE_HOST=db
DJANGO_DATABASE_PORT=5432
#Telegram
TELEGRAM_API_KEY=<TELEGRAM_API_KEY>
CHAT_ID=<CHAT_ID>
#Django User
DJANGO_ADMIN_USER=admin
DJANGO_ADMIN_EMAIL=admin@example.com
DJANGO_ADMIN_PASSWORD=admin_password
#Google Sheet
SAMPLE_SPREADSHEET_ID='1SLbizHI5rPssH3Gwdm6g04-S5c7HDpvv9X5Gz4r8xoU'
SPREADSHEET_SIZE='Лист1!A1:D20000'
SERVICE_ACCOUNT_FILE='keys.json'
````
Для использования уведомлений через телеграм бот, нужно получить TELEGRAM API KEY 
через @BotFather и получить CHAT_ID пользователя, который будет получать уведомления.

В GOOGLE SHEET API нужно получить ключи для использования и сохранить данный файл 
в главном руте репозитория под названием <keys.json>. Для получения ключей можно
воспользоваться этой [инструкцией](https://uproof.pro/13-kak-poluchit-klyuch-fajl-dlya-rabotyi-s-api-google-tablicz).

Запустите данную команду в терминале, находясь в главном руте репозитория:
```bash
docker-compose up --build
````

Так же при создании контейнеров создается суперпользователь (login=admin, password=admin_password).
Его данные можно использовать для [админки Django](127.0.0.1/admin).