from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Записаться")],
            [KeyboardButton(text="ℹ️ О нас"), KeyboardButton(text="📍 Контакты")]
        ],
        resize_keyboard=True
    )

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