from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, video
from aiogram import Router, html,F
from sqlalchemy import select, func

from db.models import Promo, session

admin_router = Router()


@admin_router.message(F.text)
async def admin(message: Message, state: FSMContext):
    try:
        query_min = select(func.min(Promo.id))
        min_id = session.execute(query_min).scalars().first()
        query_title = select(Promo.title).where(Promo.id == min_id)
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Promo.dictionary).where(Promo.id == min_id)
        dictionary = session.execute(query_dictionary).scalars().first()
        query_photo = select(Promo.photo).where(Promo.id == min_id)
        photo = session.execute(query_photo).scalars().first()
        query_video = select(Promo.video).where(Promo.id == min_id)
        video = session.execute(query_video).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        if photo:
            await message.answer_photo(photo, caption=caption)

        if video:
            await message.answer_video(video, caption=caption)

    except Exception as e:
        await message.delete()
