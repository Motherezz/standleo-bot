from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 Играть"), KeyboardButton(text="🏆 Лидеры")],
            [KeyboardButton(text="👤 Мой профиль"), KeyboardButton(text="🛒 Магазин")],
            [KeyboardButton(text="🎁 Ежедневка"), KeyboardButton(text="📸 Отправить скрин")]
        ],
        resize_keyboard=True
    )
    return kb

def formats_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1v1", callback_data="format_1v1"),
            InlineKeyboardButton(text="2v2", callback_data="format_2v2"),
        ],
        [
            InlineKeyboardButton(text="3v3", callback_data="format_3v3"),
            InlineKeyboardButton(text="5v5", callback_data="format_5v5"),
        ],
        [InlineKeyboardButton(text="« Назад", callback_data="back_main")]
    ])
    return kb

def maps_kb(format_: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Sandstone", callback_data=f"map_{format_}_Sandstone")],
        [InlineKeyboardButton(text="Rust", callback_data=f"map_{format_}_Rust")],
        [InlineKeyboardButton(text="Province", callback_data=f"map_{format_}_Province")],
        [InlineKeyboardButton(text="« Назад", callback_data="back_formats")]
    ])
    return kb

def lobby_kb(lobby_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Присоединиться", callback_data=f"join_{lobby_id}"),
            InlineKeyboardButton(text="❌ Выйти", callback_data=f"leave_{lobby_id}"),
        ]
    ])
    return kb

def admin_screen_kb(user_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить победу", callback_data=f"approve_{user_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{user_id}"),
        ]
    ])
    return kb
