from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import get_all_appointments, get_today_appointments
from datetime import date, timedelta

router = Router()


def bookings_menu():
    kb = InlineKeyboardBuilder()

    kb.button(text="📆 Сегодня", callback_data="admin:bookings:today")
    kb.button(text="📆 Завтра", callback_data="admin:bookings:tomorrow")
    kb.button(text="📅 Все", callback_data="admin:bookings:all")
    kb.button(text="🔙 Назад", callback_data="admin:back")

    kb.adjust(2)
    return kb.as_markup()


@router.callback_query(F.data == "admin:bookings")
async def open_bookings(callback: CallbackQuery):
    await callback.message.edit_text(
        "📅 <b>Выберите период</b>",
        reply_markup=bookings_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin:bookings:"))
async def show_bookings(callback: CallbackQuery):
    mode = callback.data.split(":")[-1]

    if mode == "today":
        appointments = await get_today_appointments()

    elif mode == "tomorrow":
        target = (date.today() + timedelta(days=1)).isoformat()
        appointments = await get_all_appointments()
        appointments = [a for a in appointments if a[5] == target]

    else:
        appointments = await get_all_appointments()

    if not appointments:
        await callback.message.edit_text("📭 Записей нет")
        await callback.answer()
        return

    text = "📅 <b>Записи</b>\n\n"

    for a in appointments:
        text += (
            f"#{a[0]} | {a[5]} {a[6]}\n"
            f"💈 {a[3]} | 👤 @{a[2]}\n"
            f"✂️ {a[4]}\n\n"
        )

    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 Назад", callback_data="admin:bookings")
    kb.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()