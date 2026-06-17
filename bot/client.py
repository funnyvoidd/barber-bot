from aiogram.fsm.context import FSMContext
from bot.states import BookingState
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery

from keyboards import (
    main_menu,
    services_menu,
    masters_menu,
    date_menu,
    time_menu,
    cancel_appointments_keyboard
)

from db import (
    get_user_appointments,
    delete_user_appointment
)

from services.booking_service import create_booking
from services.notifications import notify_admin
from utils.booking_text import build_booking_text

router = Router()


# ======================
# START
# ======================
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "💈 Добро пожаловать в BarberBot!\n"
        "Я помогу записаться на стрижку в «Blade».\n"
        "Выберите действие:",
        reply_markup=main_menu()
    )


# ======================
# BOOKING FLOW
# ======================
@router.message(F.text == "📅 Записаться")
async def choose_service(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "Выберите услугу:",
        reply_markup=services_menu()
    )

    await state.set_state(BookingState.choosing_service)


@router.message(
    BookingState.choosing_service,
    F.text.in_({"💈 Стрижка машинкой", "✂️ Стрижка ножницами", "🧔 Стрижка + борода"})
)
async def choose_master(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)

    await message.answer(
        "Выберите мастера:",
        reply_markup=masters_menu()
    )

    await state.set_state(BookingState.choosing_master)


@router.message(
    BookingState.choosing_master,
    F.text.in_({"Алексей", "Дмитрий", "Артём"})
)
async def choose_date(message: types.Message, state: FSMContext):
    await state.update_data(master=message.text)

    await message.answer(
        "Выберите дату:",
        reply_markup=date_menu()
    )

    await state.set_state(BookingState.choosing_date)


@router.message(
    BookingState.choosing_date,
    F.text.in_({"Сегодня", "Завтра"})
)
async def choose_time(message: types.Message, state: FSMContext):
    from datetime import date, timedelta

    d = date.today() if message.text == "Сегодня" else date.today() + timedelta(days=1)

    await state.update_data(date=d.isoformat())

    await message.answer(
        "Выберите время:",
        reply_markup=time_menu()
    )

    await state.set_state(BookingState.choosing_time)


@router.message(
    BookingState.choosing_time,
    F.text.in_({"10:00", "12:00", "14:00", "16:00", "18:00"})
)
async def ask_confirm(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)

    data = await state.get_data()

    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Подтвердить", callback_data="booking:confirm")
    kb.button(text="❌ Отмена", callback_data="booking:cancel")

    await message.answer(
        build_booking_text(data),
        reply_markup=kb.as_markup()
    )

    await state.set_state(BookingState.confirm)


# ======================
# CONFIRM / CANCEL
# ======================
@router.callback_query(F.data == "booking:confirm")
async def confirm_booking(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    user_id = callback.from_user.id
    username = callback.from_user.username or callback.from_user.full_name

    ok = await create_booking(data, user_id, username)

    if not ok:
        await callback.message.edit_text("⛔ Это время уже занято")
        await callback.answer()
        return

    await notify_admin(callback.bot, data, username)

    await state.clear()

    await callback.message.edit_text("✅ Запись подтверждена")
    await callback.answer()


@router.callback_query(F.data == "booking:cancel")
async def cancel_booking(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text("❌ Запись отменена")
    await callback.answer()


# ======================
# USER FEATURES
# ======================
@router.message(F.text == "🔙 Назад")
async def go_back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню:", reply_markup=main_menu())


@router.message(F.text == "📋 Мои записи")
async def my_bookings(message: types.Message):

    appointments = await get_user_appointments(message.from_user.id)

    if not appointments:
        await message.answer("У вас нет активных записей.")
        return

    text = "📋 Ваши записи:\n\n"

    for a in appointments:
        text += f"#{a[0]}\n{a[3]}\nМастер: {a[4]}\n{a[5]} {a[6]}\n\n"

    await message.answer(text)


@router.message(F.text == "❌ Отменить запись")
async def cancel_menu(message: types.Message):

    appointments = await get_user_appointments(message.from_user.id)

    if not appointments:
        await message.answer("У вас нет записей.")
        return

    await message.answer(
        "Выберите запись для отмены:",
        reply_markup=cancel_appointments_keyboard(appointments)
    )


@router.callback_query(F.data.startswith("cancel_"))
async def cancel_appointment_callback(callback: CallbackQuery):

    appointment_id = int(callback.data.split("_")[1])

    await delete_user_appointment(appointment_id, callback.from_user.id)

    await callback.message.edit_text("✅ Запись отменена.")
    await callback.answer()


# ======================
# INFO
# ======================
@router.message(F.text == "ℹ️ О нас")
async def about(message: types.Message):
    await message.answer(
        "Blade Barbershop — стильные стрижки с 2018 года. Работаем ежедневно с 10:00 до 20:00."
    )


@router.message(F.text == "📍 Контакты")
async def contacts(message: types.Message):
    await message.answer(
        "📍 Белград, ул. Кнез Михаилова 52\n📞 +381 11 123 45 67"
    )