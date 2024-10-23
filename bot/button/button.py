from aiogram.types import InlineKeyboardButton, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def menu_button():
    ikb = InlineKeyboardBuilder()
    ikb.add(
        *[
            InlineKeyboardButton(text="✅Promokod", callback_data="promo"),
            InlineKeyboardButton(text="💰Aksiya", callback_data="discount"),
        ]
    )
    ikb.adjust(1, 1)
    return ikb.as_markup()


def promo_button(pege):
    ikb = InlineKeyboardBuilder()
    ikb.add(
        *[
            InlineKeyboardButton(text="⬅️", callback_data=f"product_{pege - 1}"),
            InlineKeyboardButton(text="➡️", callback_data=f"product_{pege + 1}"),
            InlineKeyboardButton(text="Video Qo'llanma", callback_data=f"qullanma"),
            InlineKeyboardButton(text="🔙 Ortga", callback_data=f"back"),
        ]
    )
    ikb.adjust(2, 1, 1)
    return ikb.as_markup()


def discount_button(count):
    ikb = InlineKeyboardBuilder()
    ikb.add(
        *[
            InlineKeyboardButton(text="⬅️", callback_data=f"discount_{count - 1}"),
            InlineKeyboardButton(text="➡️", callback_data=f"discount_{count + 1}"),
            InlineKeyboardButton(text="Video Qo'llanma", callback_data=f"discount1"),
            InlineKeyboardButton(text="🔙 Ortga", callback_data=f"back"),
        ]
    )

    ikb.adjust(2, 1, 1)
    return ikb.as_markup()


def back_button():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text="🔙Ortga", callback_data="back"),
    ])
    return ikb.as_markup()


def instagram_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="Instagram 🔊",
                       web_app=WebAppInfo(url='https://www.instagram.com/pramokod_uz?igsh=MXJscmd0bTVkMzkwOA=='))
    ])

    return rkb.as_markup(resize_keyboard=True)
