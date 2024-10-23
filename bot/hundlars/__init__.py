from aiogram import Dispatcher

from bot.hundlars.discount import discount_router
from bot.hundlars.menu import menu_router
from bot.hundlars.start import start_router

dp = Dispatcher()
dp.include_routers(
    start_router,
    menu_router,
    discount_router
)