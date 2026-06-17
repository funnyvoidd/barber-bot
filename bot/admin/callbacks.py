from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query()
async def fallback(callback: CallbackQuery):
    await callback.answer("⚠️ Действие не найдено", show_alert=True)