from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo
from sqlalchemy import select, func

from bot.button.button import promo_button, menu_button, back_button
from bot.state import MenuState
from db.models import session, Promo

menu_router = Router()


@menu_router.callback_query(F.data == "promo", MenuState.menu)
async def promo(callback_query: CallbackQuery, state: FSMContext):
    try:
        query_min = select(func.min(Promo.id))
        min_id = session.execute(query_min).scalars().first()
        query_title = select(Promo.title).where(Promo.id == min_id)
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Promo.dictionary).where(Promo.id == min_id)
        dictionary = session.execute(query_dictionary).scalars().first()
        query_photo = select(Promo.photo).where(Promo.id == min_id)
        photo = session.execute(query_photo).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        pege = min_id
        await state.update_data({"pege": pege})
        media = InputMediaPhoto(media=photo, caption=caption)
        await callback_query.message.edit_media(media=media, reply_markup=promo_button(pege))
        await state.set_state(MenuState.promo)

    except Exception as e:
        pass


@menu_router.callback_query(F.data.startswith('product_'))
async def product_menu(callback: CallbackQuery, state: FSMContext):
    pege = int(callback.data.split("_")[-1])
    query_max = select(func.max(Promo.id))
    max_id = session.execute(query_max).scalars().first()
    query_min = select(func.min(Promo.id))
    min_id = session.execute(query_min).scalars().first()
    if pege <= max_id and pege >= min_id:
        query_title = select(Promo.title).where(Promo.id == pege)
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Promo.dictionary).where(Promo.id == pege)
        dictionary = session.execute(query_dictionary).scalars().first()
        query_photo = select(Promo.photo).where(Promo.id == pege)
        photo = session.execute(query_photo).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        await state.update_data({"pege": pege})
        photo = InputMediaPhoto(media=photo, caption=caption)
        await callback.message.edit_media(media=photo, reply_markup=promo_button(pege))
        await state.set_state(MenuState.promo)
    elif pege < min_id:
        pege = max_id
        query_title = select(Promo.title).where(Promo.id == pege)
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Promo.dictionary).where(Promo.id == pege)
        dictionary = session.execute(query_dictionary).scalars().first()
        query_photo = select(Promo.photo).where(Promo.id == pege)
        photo = session.execute(query_photo).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        await state.update_data({"pege": pege})
        photo = InputMediaPhoto(media=photo, caption=caption)
        await callback.message.edit_media(media=photo, reply_markup=promo_button(pege))
        await state.set_state(MenuState.promo)
    elif pege > max_id:
        pege = min_id
        query_title = select(Promo.title).where(Promo.id == pege)
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Promo.dictionary).where(Promo.id == pege)
        dictionary = session.execute(query_dictionary).scalars().first()
        query_photo = select(Promo.photo).where(Promo.id == pege)
        photo = session.execute(query_photo).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        await state.update_data({"pege": pege})
        photo = InputMediaPhoto(media=photo, caption=caption)
        await callback.message.edit_media(media=photo, reply_markup=promo_button(pege))
        await state.set_state(MenuState.promo)


@menu_router.callback_query(F.data == "qullanma", MenuState.promo)
async def qullanma_menu(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        query_video = select(Promo.video).where(Promo.id == data['pege'])
        video = session.execute(query_video).scalars().first()
        query_title = select(Promo.title).where(Promo.id == data['pege'])
        title = session.execute(query_title).scalars().first()
        query_dictionary = select(Promo.dictionary).where(Promo.id == data['pege'])
        dictionary = session.execute(query_dictionary).scalars().first()
        caption = f"{html.bold(title)}\n{dictionary}\n"

        media = InputMediaVideo(media=video, caption=caption)
        await callback.message.edit_media(media=media, reply_markup=back_button())
        await state.set_state(MenuState.video)
    except Exception as e:
        pass


@menu_router.callback_query(F.data == "back", MenuState.video)
async def back(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pege = data['pege']
    query_title = select(Promo.title).where(Promo.id == pege)
    title = session.execute(query_title).scalars().first()
    query_dictionary = select(Promo.dictionary).where(Promo.id == pege)
    dictionary = session.execute(query_dictionary).scalars().first()
    query_photo = select(Promo.photo).where(Promo.id == pege)
    photo = session.execute(query_photo).scalars().first()
    caption = f"{html.bold(title)}\n{dictionary}\n"

    await state.update_data({"pege": pege})
    media = InputMediaPhoto(media=photo, caption=caption)
    await call.message.edit_media(media=media, reply_markup=promo_button(pege))
    await state.set_state(MenuState.promo)


@menu_router.callback_query(F.data == "back", MenuState.promo)
async def back(callback_query: CallbackQuery, state: FSMContext):
    try:
        photo = InputMediaPhoto(media="https://t.me/reklamakanaln1mln/14")
        await callback_query.message.edit_media(media=photo,
                                                reply_markup=menu_button())
        await state.clear()
        await state.set_state(MenuState.menu)
    except Exception as e:
        pass
