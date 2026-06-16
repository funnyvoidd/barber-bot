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