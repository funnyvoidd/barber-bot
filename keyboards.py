from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📋 Сегодня",
        callback_data="admin_today"
    )

    builder.button(
        text="📅 Все записи",
        callback_data="admin_all"
    )

    builder.button(
        text="👨‍💼 Мастера",
        callback_data="admin_masters"
    )

    builder.button(
        text="📊 Статистика",
        callback_data="admin_stats"
    )

    builder.adjust(1)

    return builder.as_markup()

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Записаться")],
            [KeyboardButton(text="📋 Мои записи")],
            [KeyboardButton(text="❌ Отменить запись")],
            [KeyboardButton(text="ℹ️ О нас")],
            [KeyboardButton(text="📍 Контакты")]
        ],
        resize_keyboard=True
    )

def cancel_appointments_keyboard(appointments):
    builder = InlineKeyboardBuilder()

    for appointment in appointments:
        builder.button(
            text=f"❌ {appointment[5]} {appointment[6]}",
            callback_data=f"cancel_{appointment[0]}"
        )

    builder.adjust(1)

    return builder.as_markup()

def services_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💈 Стрижка машинкой")],
            [KeyboardButton(text="✂️ Стрижка ножницами")],
            [KeyboardButton(text="🧔 Стрижка + борода")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

def masters_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Алексей")],
            [KeyboardButton(text="Дмитрий")],
            [KeyboardButton(text="Артём")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

def date_menu():
    # Здесь будет простая кнопка "Сегодня" + выбор даты
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Сегодня")],
            [KeyboardButton(text="Завтра")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

def time_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="10:00")],
            [KeyboardButton(text="12:00")],
            [KeyboardButton(text="14:00")],
            [KeyboardButton(text="16:00")],
            [KeyboardButton(text="18:00")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )