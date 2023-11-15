from aiogram import F, Router, types
from aiogram.filters import Command
from create_bot import bot
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import re

from handlers.parser import get_data, Information
from handlers.keyboard import post_kb, tags_kb, utilities_kb

router = Router()

class Caption(StatesGroup):
    control = State()
    edit_caption = State()
    edit_tags = State()

# ===========================start============================
@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        f"Вітаю {message.from_user.full_name}! 👏\n"
        "Цей бот призначений для швидкого парсингу і створення постів у telegram з OLX.ua\n"
        "Приємного користування 😁",
        disable_web_page_preview=True)

@router.message(F.text.startswith("https://www.olx.ua/"))
async def main(message: types.Message, state: FSMContext):
    try:
        await get_data(message, state)
    except:
        await message.answer(
            f"Виникла помилка ❌\nСторінку не вдалося обробити\n",
            reply_markup=types.ReplyKeyboardRemove(),
        )

@router.callback_query(F.data == "Змінити опис ✏️", Caption.control)
async def edit_caption(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    caption_user = data["caption_user"]
    await query.message.delete()
    await query.message.answer(f"Ось текст який ви можете редагувати: \n{caption_user}")
    await state.set_state(Caption.edit_caption)
    
@router.callback_query(F.data == "Змінити теги 🧷", Caption.control)
async def edit_caption(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=await tags_kb())
    await state.set_state(Caption.edit_tags)

@router.callback_query(F.data == "🔙 Назад", Caption.edit_tags)
async def tags_baks(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=await post_kb())
    await state.set_state(Caption.control)

@router.callback_query(Caption.edit_tags)
async def tags_baks(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Caption.control)

    data = await state.get_data()
    tags = data["caption_tag"]

    tags = tags + f' #{query.data} '

    await state.update_data(caption_tag=tags)

    caption_info = data["caption_info"]
    caption_money = data["caption_money"]
    caption_user = data["caption_user"]
    caption_communication = data["caption_communication"]
    full_caption = Information.get_full_caption(caption_info, caption_money, 
                                                caption_user, tags, caption_communication)
            
    await query.message.edit_caption(caption=full_caption, reply_markup=await post_kb())



@router.callback_query(F.data == "Репост в канал ▶️", Caption.control)
async def repost_to_channel(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    media_group = data["all_photo"]
    caption_info = data["caption_info"]
    caption_money = data["caption_money"]
    caption_user = data["caption_user"]
    caption_tag = data["caption_tag"]
    caption_communication = data["caption_communication"]
    full_caption = Information.get_full_caption(caption_info, caption_money, caption_user, caption_tag, caption_communication)

    await state.clear()
    await query.message.edit_reply_markup(reply_markup=None)

    media_messages = await bot.send_media_group(-1001489053011, media=media_group)
    await bot.edit_message_caption(chat_id=-1001489053011, message_id=media_messages[0].message_id,caption=full_caption)



@router.callback_query(F.data == "➕➖ ком послуги", Caption.control)
@router.callback_query(F.data == "➕➖ лічильники", Caption.control)
@router.callback_query(F.data == "➕➖ світло", Caption.control)
async def utilities(query: types.CallbackQuery, state: FSMContext):
    async def is_utilities(text) -> str:
        pattern_utilities = r'\+ком послуги'
        pattern_counter = r'\+лічильник'
        pattern_light = r'\+світло'

        if re.search(pattern_utilities, text, re.IGNORECASE):
            return "utilities"
        elif re.search(pattern_counter, text, re.IGNORECASE):
            return "counter"
        elif re.search(pattern_light, text, re.IGNORECASE):
            return "light"
        else:
            return ""

    async def delete_utilities(query: types.CallbackQuery, value: str, price: str, state: FSMContext):
        money: str = re.sub(value, '', price, flags=re.IGNORECASE)
        await state.update_data(caption_money=money)
        caption_info = data["caption_info"]
        caption_user = data["caption_user"]
        caption_tag = data["caption_tag"]
        caption_communication = data["caption_communication"]
        full_caption = Information.get_full_caption(caption_info, money, 
                                                    caption_user, caption_tag, caption_communication)
        
        await query.message.edit_caption(caption=full_caption, reply_markup=await post_kb())

    async def add_utilities(query: types.CallbackQuery, pattern: str, money: str, state: FSMContext):
        money: str = money + pattern
        await state.update_data(caption_money=money)
        caption_info = data["caption_info"]
        caption_user = data["caption_user"]
        caption_tag = data["caption_tag"]
        caption_communication = data["caption_communication"]
        full_caption = Information.get_full_caption(caption_info, money, 
                                                    caption_user, caption_tag, caption_communication)
      
        await query.message.edit_caption(caption=full_caption, reply_markup=await utilities_kb(query.data))

    # geting caption money
    data = await state.get_data()
    money = data["caption_money"]
    
    # cheking exists utilitie
    utilitie = await is_utilities(money)

    if not utilitie:
        if query.data == "➕➖ ком послуги":
            pattern_utilities = '+ком послуги'
            await add_utilities(query, pattern_utilities, money, state)

        if query.data == "➕➖ лічильники":
            pattern_counter = '+лічильник'
            await add_utilities(query, pattern_counter, money, state)
        
        if query.data == "➕➖ світло":
            pattern_light = '+світло'
            await add_utilities(query, pattern_light, money, state)

    if utilitie:
        if utilitie == "utilities":
            pattern_utilities = r'\+ком послуги'
            await delete_utilities(query, pattern_utilities, money, state)
            
        if utilitie == "counter":
            pattern_counter = r'\+лічильник'
            await delete_utilities(query, pattern_counter, money, state)
    
        if utilitie == "light":
            pattern_light =  r'\+світло'
            await delete_utilities(query, pattern_light, money, state)  

@router.message(Caption.edit_caption)
async def edit_caption_completed(message: types.Message, state: FSMContext):
    await state.update_data(caption_user=message.text) # caption user (Update data after get data)
    data = await state.get_data()
    first_photo = data["first_photo"]
    caption_info = data["caption_info"]
    caption_money = data["caption_money"]
    caption_user = data["caption_user"]
    caption_tag = data["caption_tag"]
    caption_communication = data["caption_communication"]
    await message.delete()
    await state.set_state(Caption.control)
    
    full_caption = Information.get_full_caption(caption_info, caption_money, caption_user, caption_tag, caption_communication)

    await message.answer_photo(caption=full_caption, photo=first_photo, reply_markup=await post_kb())

@router.message()
async def all_message(message: types.Message):
    await message.answer(
        "🔴 Вибачте, але мені потрібне тільки посилання на сторінку olx.ua з нерухомістю.\n"
        "У форматі https://www.olx.ua/...",
        disable_web_page_preview=True,
    )