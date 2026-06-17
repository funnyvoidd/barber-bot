from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from config.settings import ADMIN_ID
from db import get_all_appointments, get_statistics
from keyboards import admin_keyboard

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Доступ запрещён.")
        return

    await message.answer(
        "🔧 Панель администратора",
        reply_markup=admin_keyboard()
    )

@router.callback_query(
    F.data == "admin_all"
)
async def show_all(
    callback: CallbackQuery
):
    appointments = await get_all_appointments()

    if not appointments:
        await callback.message.answer(
            "Записей нет."
        )
        return

    text = "📅 Все записи\n\n"

    for a in appointments:
        text += (
            f"#{a[0]}\n"
            f"{a[5]} {a[6]}\n"
            f"{a[3]}\n"
            f"{a[4]}\n"
            f"@{a[2]}\n\n"
        )

    await callback.message.answer(text)
    await callback.answer()

@router.callback_query(
    F.data == "admin_stats"
)
async def show_stats(
    callback: CallbackQuery
):
    total, master = await get_statistics()

    text = (
        f"📊 Статистика\n\n"
        f"Всего записей: {total}\n"
    )

    if master:
        text += (
            f"Популярный мастер: "
            f"{master[0]} ({master[1]})"
        )

    await callback.message.answer(text)

    await callback.answer()