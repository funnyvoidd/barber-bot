from config.settings import ADMIN_ID


async def notify_admin(bot, data: dict, username: str):
    await bot.send_message(
        ADMIN_ID,
        f"🔔 Новая запись!\n\n"
        f"Клиент: @{username}\n"
        f"Услуга: {data['service']}\n"
        f"Мастер: {data['master']}\n"
        f"Дата: {data['date']}\n"
        f"Время: {data['time']}"
    )