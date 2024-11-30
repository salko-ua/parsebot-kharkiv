from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.handlers.dictionaries import subway_paths

async def post_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = [
        "Змінити опис ✏️",
        "Додати тег 🧷",
        "Додати метро Ⓜ️",
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
        "Додати тег 🧷",
        "Додати метро Ⓜ️",
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


async def subway_path_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = ["Зелена 🟢", "Синя 🔵",
                "Червона 🔴", "🔙 Назад"]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)

async def get_subway_stantion_names_by_color(color) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = subway_paths[color]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(3).as_markup(resize_keyboard=True)



