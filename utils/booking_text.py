def build_booking_text(data: dict) -> str:
    return (
        "📋 Подтвердите запись:\n\n"
        f"💈 Услуга: {data['service']}\n"
        f"👤 Мастер: {data['master']}\n"
        f"📅 Дата: {data['date']}\n"
        f"⏰ Время: {data['time']}\n"
    )