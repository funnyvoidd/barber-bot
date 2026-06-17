DB_NAME = "barber.db"

from .base import get_db


async def add_appointment(
    user_id: int,
    username: str,
    service: str,
    master: str,
    date_val: str,
    time_val: str
):
    db = await get_db()

    await db.execute(
        """
        INSERT INTO appointments (
            user_id, username, service, master, date, time
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, username, service, master, date_val, time_val)
    )

    await db.commit()
    await db.close()


async def get_all_appointments():
    db = await get_db()
    cursor = await db.execute("SELECT * FROM appointments")
    rows = await cursor.fetchall()
    await db.close()
    return rows


async def get_user_appointments(user_id):
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM appointments WHERE user_id=?",
        (user_id,)
    )
    rows = await cursor.fetchall()
    await db.close()
    return rows