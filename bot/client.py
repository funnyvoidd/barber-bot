from aiogram.fsm.context import FSMContext
from bot.states import BookingState
from aiogram import Router, F, types
from aiogram.filters import Command
from keyboards import main_menu, services_menu, masters_menu, date_menu, time_menu
from db import add_appointment

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"💈 Добро пожаловать в BarberBot!\n"
        f"Я помогу записаться на стрижку в «Blade».\n"
        f"Выберите действие:",
        reply_markup=main_menu()
    )

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
    F.text.in_(
        {
            "💈 Стрижка машинкой",
            "✂️ Стрижка ножницами",
            "🧔 Стрижка + борода"
        }
    )
)
async def choose_master(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(service=message.text)

    await message.answer(
        "Выберите мастера:",
        reply_markup=masters_menu()
    )

    await state.set_state(
        BookingState.choosing_master
    )

@router.message(
    BookingState.choosing_master,
    F.text.in_({"Алексей", "Дмитрий", "Артём"})
)
async def choose_date(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(master=message.text)

    await message.answer(
        "Выберите дату:",
        reply_markup=date_menu()
    )

    await state.set_state(
        BookingState.choosing_date
    )

@router.message(
    BookingState.choosing_date,
    F.text.in_({"Сегодня", "Завтра"})
)
async def choose_time(
    message: types.Message,
    state: FSMContext
):
    from datetime import date, timedelta

    if message.text == "Сегодня":
        d = date.today().isoformat()
    else:
        d = (
            date.today() + timedelta(days=1)
        ).isoformat()

    await state.update_data(date=d)

    await message.answer(
        "Выберите время:",
        reply_markup=time_menu()
    )

    await state.set_state(
        BookingState.choosing_time
    )

@router.message(F.text.in_({"10:00", "12:00", "14:00", "16:00", "18:00"}))
async def confirm_booking(
    message: types.Message,
    state: FSMContext
):
    data = await state.get_data()
    data["time"] = message.text
    data["user_id"] = message.from_user.id
    data["username"] = message.from_user.username or message.from_user.full_name

    # Асинхронная запись в БД
    await add_appointment(
        user_id=data["user_id"],
        username=data["username"],
        service=data["service"],
        master=data["master"],
        date_val=data["date"],
        time_val=data["time"]
    )

    await message.answer(
        f"✅ Запись подтверждена!\n\n"
        f"Услуга: {data['service']}\n"
        f"Мастер: {data['master']}\n"
        f"Дата: {data['date']}\n"
        f"Время: {data['time']}\n\n"
        f"Ждём вас!",
        reply_markup=main_menu()
    )

    # Уведомление администратору
    from config.settings import ADMIN_ID
    await message.bot.send_message(
        ADMIN_ID,
        f"🔔 Новая запись!\n\n"
        f"Клиент: @{data['username']}\n"
        f"Услуга: {data['service']}\n"
        f"Мастер: {data['master']}\n"
        f"Дата: {data['date']}\n"
        f"Время: {data['time']}"
    )

    await state.clear()

@router.message(F.text == "🔙 Назад")
async def go_back(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu())

@router.message(F.text == "ℹ️ О нас")
async def about(message: types.Message):
    await message.answer("Blade Barbershop — стильные стрижки с 2018 года. Работаем ежедневно с 10:00 до 20:00.")

@router.message(F.text == "📍 Контакты")
async def contacts(message: types.Message):
    await message.answer("📍 Белград, ул. Кнез Михаилова 52\n📞 +381 11 123 45 67")