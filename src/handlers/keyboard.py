from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def post_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = [
        "Змінити опис ✏️",
        "Змінити теги 🧷",
        "➕➖ ком послуги",
        "➕➖ лічильники",
        "➕➖ світло",
        "Репост в канал ▶️"
    ]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)

async def utilities_kb(name) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = [
        "Змінити опис ✏️",
        "Змінити теги 🧷",
        name,
        "Репост в канал ▶️"
    ]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)

async def tags_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = ["Салтовка", "Центр", 
                "Алексеевка", "ПавловоПоле ",
                "Одесская", "ХолГора", 
                "НовыеДома", "ХТЗ",
                "🔙 Назад"]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2, 2, 2, 2, 1).as_markup(resize_keyboard=True)
