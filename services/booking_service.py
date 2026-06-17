from db import add_appointment, is_slot_busy


async def create_booking(data: dict, user_id: int, username: str) -> bool:
    busy = await is_slot_busy(
        data["master"],
        data["date"],
        data["time"]
    )

    if busy:
        return False

    await add_appointment(
        user_id=user_id,
        username=username,
        service=data["service"],
        master=data["master"],
        date_val=data["date"],
        time_val=data["time"]
    )

    return True