from aiogram.fsm.state import StatesGroup, State


class MenuState(StatesGroup):
    menu = State()
    promo=State()
    discount=State()
    video=State()