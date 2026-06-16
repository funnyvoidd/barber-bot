# BarberBot — телеграм-бот для записи в барбершоп

Бот позволяет клиентам записаться на услугу в барбершоп, а администратору — просматривать все записи.

## Возможности
- Выбор услуги, мастера, даты и времени
- Сохранение записи в базу данных (SQLite)
- Уведомление администратора о новой записи
- Админ-панель (`/admin`) — просмотр записей на сегодня

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/funnyvoidd/barber-bot.git
   cd barber-bot
   ```
   
2. Установите зависимости:
```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Создайте файл ```.env```:
* BOT_TOKEN — получите у @BotFather
* ADMIN_ID — ваш Telegram ID (можно узнать у @userinfobot)

4. Запустите бота:
```bash
python bot.py
```