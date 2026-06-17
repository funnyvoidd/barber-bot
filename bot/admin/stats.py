from aiogram import Router, F
from aiogram.types import CallbackQuery

from db import get_statistics
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "admin:stats")
async def stats(callback: CallbackQuery):
    total, master = await get_statistics()

    text = f"📊 <b>Статистика</b>\n\nВсего записей: {total}\n"

    if master:
        text += f"\n👨‍💼 Топ мастер: {master[0]} ({master[1]})"

    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 Назад", callback_data="admin:back")

    await callback.message.edit_text(
        text,
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()