import aiosqlite

DB_NAME = "barber.db"


async def get_db():
    return await aiosqlite.connect(DB_NAME)