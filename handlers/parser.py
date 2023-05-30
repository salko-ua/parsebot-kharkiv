import re

import requests
from aiogram import types
from bs4 import BeautifulSoup

from create_bot import bot


async def get_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


# Отримую фото
async def get_photo(soup: BeautifulSoup):
    photo = soup.find("div", class_="swiper-wrapper").find_all("img")

    list_src_photo = []  # список src фото
    for src in photo:
        list_src_photo.append(src.get("src"))

    if len(list_src_photo) > 10:
        del list_src_photo[10:]

    media_group = []
    for photo_url in list_src_photo:
        media_group.append(types.InputMediaPhoto(media=photo_url))

    return media_group


# Отримую опис
async def get_caption(soup: BeautifulSoup):
    # Знаходження опису (теги на олх)
    caption = soup.find("ul", class_="css-sfcl1s").find_all("p")  # TODO do not use css
    list_words_caption = {}
    need = [
        "Количество комнат:",
        "Общая площадь:",
        "Этаж:",
        "Этажность:",
        "Кількість кімнат:",
        "Загальна площа:",
        "Поверх:",
        "Поверховість:",
    ]
    for capt in caption:
        if need[0] in capt.text or need[4] in capt.text:
            list_words_caption[1] = capt.text
        elif need[1] in capt.text or need[5] in capt.text:
            list_words_caption[2] = capt.text
        elif need[2] in capt.text or need[6] in capt.text:
            list_words_caption[3] = capt.text
        elif need[3] in capt.text or need[7] in capt.text:
            list_words_caption[4] = capt.text

    # Отримую число з рядка
    count_room = int((re.search(r"\d+", list_words_caption[1])).group())
    count_area = int((re.search(r"\d+", list_words_caption[2])).group())
    flour_have = int((re.search(r"\d+", list_words_caption[3])).group())
    floor_everything = int((re.search(r"\d+", list_words_caption[4])).group())
    flour = f"{flour_have}/{floor_everything}"

    # Знаходження грошей
    money = soup.find("h3").text

    without_space = "".join(money.split())
    find_money_int = int((re.search(r"\d+", without_space)).group())
    get_tegs_money = await tegs_select(find_money_int)

    # Знаходження опису на olx
    caption_text = soup.find("div", class_="css-bgzo2k er34gjf0").text  # TODO do not use css

    if len(caption_text) > 800:
        caption_text = caption_text[0:800]

    # Опис альбому
    album_caption = f"""
🏡{count_room}к кв
🏢Этаж:{flour}
🔑Площадь:{count_area}м2
Ⓜ️Метро:
👉Адрес:
💳️{money}

Описание : {caption_text}

#{count_room}ККВ #{get_tegs_money}

Связь тут:
Написать ✍️ @realtor_057 
Позвонить ☎️ +380996643097
"""

    return album_caption


# Отримання тегу залежно від ціни
async def tegs_select(price):
    if 0 <= price <= 1999:
        return "0-2000грн"
    elif 2000 <= price <= 4999:
        return "20005000грн"
    elif 5000 <= price <= 6999:
        return "50007000грн"
    elif 7000 <= price <= 8999:
        return "70009000грн"
    elif 9000 <= price <= 11999:
        return "900012000грн"
    elif 12000 <= price <= 13999:
        return "1200014000грн"
    elif 14000 <= price <= 14999:
        return "1400015000грн"
    elif price >= 15000:
        return "Выше15000грн"


# Отримання всіх даних і запуск надсилання
async def get_data(message: types.Message):
    soup: BeautifulSoup = await get_url(message.text)

    media_group = await get_photo(soup)
    album_caption = await get_caption(soup)

    await send_data(message, media_group, album_caption)


# Надсилання
async def send_data(message: types.Message, media_group, album_caption):
    media_messages = await bot.send_media_group(message.chat.id, media=media_group)

    await bot.edit_message_caption(
        chat_id=media_messages[0].chat.id,
        message_id=media_messages[0].message_id,
        caption=album_caption,
    )
