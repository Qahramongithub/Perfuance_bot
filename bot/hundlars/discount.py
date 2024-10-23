from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, CallbackQuery, InputMediaVideo
from sqlalchemy import select, func

from bot.button.button import discount_button, menu_button, back_button
from bot.state import MenuState
from db.models import session, Aksiya

discount_router = Router()


@discount_router.callback_query(F.data == "discount", MenuState.menu)
async def discount_callback(call: CallbackQuery, state: FSMContext):
    try:
        query_min = select(func.min(Aksiya.id))
        min_id = session.execute(query_min).scalars().first()
        query_title = select(Aksiya.title).where(Aksiya.id == min_id)
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Aksiya.dictionary).where(Aksiya.id == min_id)
        dictionary = session.execute(query_dictionary).scalars().first()
        query_photo = select(Aksiya.photo).where(Aksiya.id == min_id)
        photo = session.execute(query_photo).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        pege = min_id
        await state.update_data({"pege": pege})
        media = InputMediaPhoto(media=photo, caption=caption)
        await call.message.edit_media(media=media, reply_markup=discount_button(pege))
        await state.set_state(MenuState.discount)

    except Exception as e:
        pass


@discount_router.callback_query(F.data.startswith("discount_"))
async def discount(callback: CallbackQuery, state: FSMContext):
    pege = int(callback.data.split("_")[-1])
    query_max = select(func.max(Aksiya.id))
    max_id = session.execute(query_max).scalars().first()
    query_min = select(func.min(Aksiya.id))
    min_id = session.execute(query_min).scalars().first()
    if pege <= max_id and pege >= min_id:
        query_title = select(Aksiya.title).where(Aksiya.id == pege)
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Aksiya.dictionary).where(Aksiya.id == pege)
        dictionary = session.execute(query_dictionary).scalars().first()
        query_photo = select(Aksiya.photo).where(Aksiya.id == pege)
        photo = session.execute(query_photo).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        await state.update_data({"pege": pege})
        photo = InputMediaPhoto(media=photo, caption=caption)
        await callback.message.edit_media(media=photo, reply_markup=discount_button(pege))
        await state.set_state(MenuState.discount)
    elif pege < min_id:
        pege = max_id
        query_title = select(Aksiya.title).where(Aksiya.id == pege)
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Aksiya.dictionary).where(Aksiya.id == pege)
        dictionary = session.execute(query_dictionary).scalars().first()
        query_photo = select(Aksiya.photo).where(Aksiya.id == pege)
        photo = session.execute(query_photo).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        await state.update_data({"pege": pege})
        photo = InputMediaPhoto(media=photo, caption=caption)
        await callback.message.edit_media(media=photo, reply_markup=discount_button(pege))
        await state.set_state(MenuState.discount)
    elif pege > max_id:
        pege = min_id
        query_title = select(Aksiya.title).where(Aksiya.id == pege)
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Aksiya.dictionary).where(Aksiya.id == pege)
        dictionary = session.execute(query_dictionary).scalars().first()
        query_photo = select(Aksiya.photo).where(Aksiya.id == pege)
        photo = session.execute(query_photo).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        await state.update_data({"pege": pege})
        photo = InputMediaPhoto(media=photo, caption=caption)
        await callback.message.edit_media(media=photo, reply_markup=discount_button(pege))
        await state.set_state(MenuState.discount)


@discount_router.callback_query(F.data == "discount1", MenuState.discount)
async def qullanma_menu(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        query_video = select(Aksiya.video).where(Aksiya.id == data['pege'])
        video = session.execute(query_video).scalars().first()
        query_title = select(Aksiya.title).where(Aksiya.id == data['pege'])
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Aksiya.dictionary).where(Aksiya.id == data['pege'])
        dictionary = session.execute(query_dictionary).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        media = InputMediaVideo(media=video, caption=caption)
        await callback.message.edit_media(media=media, reply_markup=back_button())
        await state.set_state(MenuState.discount)
    except Exception as e:
        pass


@discount_router.callback_query(F.data == "back", MenuState.discount)
async def back_callback(call: CallbackQuery, state: FSMContext):
    try:
        photo = InputMediaPhoto(media="https://t.me/reklamakanaln1mln/14")
        await call.message.edit_media(media=photo,
                                      reply_markup=menu_button())
        await state.clear()
        await state.set_state(MenuState.menu)
    except Exception as e:
        pass
