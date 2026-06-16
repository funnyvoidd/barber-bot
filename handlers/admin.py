from aiogram import Router, types
from aiogram.filters import Command
from config import ADMIN_ID
from db import get_today_appointments

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Доступ запрещён.")
        return

    appointments = await get_today_appointments()
    if not appointments:
        await message.answer("На сегодня записей нет.")
        return

    text = "📋 Записи на сегодня:\n\n"
    for a in appointments:
        # a = (id, user_id, username, service, master, date, time, created_at)
        text += f"🕐 {a[6]} — {a[3]} (мастер {a[4]}, клиент @{a[2]})\n"

    await message.answer(text)