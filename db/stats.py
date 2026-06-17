from .base import get_db


async def get_statistics():
    db = await get_db()

    total = (await db.execute_fetchone(
        "SELECT COUNT(*) FROM appointments"
    ))[0]

    master = await db.execute_fetchone(
        """
        SELECT master, COUNT(*)
        FROM appointments
        GROUP BY master
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """
    )

    await db.close()
    return total, master