from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.settings import ADMIN_ID

router = Router()


def admin_menu():
    kb = InlineKeyboardBuilder()

    kb.button(text="📅 Записи", callback_data="admin:bookings")
    kb.button(text="📊 Статистика", callback_data="admin:stats")
    kb.button(text="🔎 Поиск", callback_data="admin:search")

    kb.adjust(2)
    return kb.as_markup()


@router.message(Command("admin"))
async def admin_start(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Доступ запрещён.")
        return

    await message.answer(
        "🧠 <b>Admin Dashboard</b>",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin:back")
async def back(callback: CallbackQuery):
    await callback.message.edit_text(
        "🧠 Admin Dashboard",
        reply_markup=admin_menu()
    )
    await callback.answer()