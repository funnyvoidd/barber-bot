import aiosqlite
from datetime import date

DB_NAME = "barber.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            service TEXT,
            master TEXT,
            date TEXT,
            time TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        await db.commit()

async def add_appointment(user_id: int, username: str, service: str, master: str, date_val: str, time_val: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO appointments (user_id, username, service, master, date, time) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, username, service, master, date_val, time_val)
        )
        await db.commit()

async def get_today_appointments():
    today = date.today().isoformat()
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM appointments WHERE date=? ORDER BY time",
            (today,)
        )
        rows = await cursor.fetchall()
    return rows

async def is_slot_busy(master: str, date_val: str, time_val: str):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT id
            FROM appointments
            WHERE master = ?
            AND date = ?
            AND time = ?
            """,
            (master, date_val, time_val)
        )

        result = await cursor.fetchone()
        return result is not None


async def get_user_appointments(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT *
            FROM appointments
            WHERE user_id = ?
            ORDER BY date, time
            """,
            (user_id,)
        )

        return await cursor.fetchall()


async def delete_user_appointment(
    appointment_id: int,
    user_id: int
):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            DELETE FROM appointments
            WHERE id = ?
            AND user_id = ?
            """,
            (
                appointment_id,
                user_id
            )
        )

        await db.commit()


async def get_all_appointments():
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM appointments
            ORDER BY date, time
            """
        )

        return await cursor.fetchall()

async def get_statistics():
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM appointments
            """
        )

        total = (await cursor.fetchone())[0]

        cursor = await db.execute(
            """
            SELECT master, COUNT(*)
            FROM appointments
            GROUP BY master
            ORDER BY COUNT(*) DESC
            LIMIT 1
            """
        )

        master = await cursor.fetchone()

        return total, master