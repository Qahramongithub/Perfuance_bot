from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select, insert

from bot.button.button import instagram_button, menu_button
from bot.state import MenuState
from db.models import User, session

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    query = select(User.id).where(User.user_id == message.from_user.id)
    user = session.execute(query).scalars().first()

    if not user:
        new_user = insert(User).values(
            user_id=message.from_user.id,
            full_name=message.from_user.full_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )
        session.execute(new_user)
        session.commit()
    await message.answer(html.bold(f"<i> {message.from_user.full_name}</i>"), reply_markup=instagram_button())
    await message.answer_photo(photo="https://t.me/reklamakanaln1mln/14",
                               reply_markup=menu_button())
    await state.set_state(MenuState.menu)


@start_router.message()
async def message_handler(message: Message, state: FSMContext) -> None:
    await message.delete()
