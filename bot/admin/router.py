from aiogram import Router

from .dashboard import router as dashboard_router
from .bookings import router as bookings_router
from .stats import router as stats_router
from .callbacks import router as fallback_router

admin_router = Router()

admin_router.include_router(dashboard_router)
admin_router.include_router(bookings_router)
admin_router.include_router(stats_router)
admin_router.include_router(fallback_router)