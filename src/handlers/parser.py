import re
import requests
from aiogram import types
from aiogram.utils.media_group import MediaGroupBuilder
from bs4 import BeautifulSoup
from src.handlers import main
from src.handlers.keyboard import post_kb
from aiogram.fsm.context import FSMContext


def get_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_photo(
    soup: BeautifulSoup, caption: str
) -> [MediaGroupBuilder, types.URLInputFile]:
    photo = soup.find("div", class_="swiper-wrapper").find_all("img")

    list_src_photo = []

    for src in photo:
        list_src_photo.append(src.get("src"))

    if len(list_src_photo) > 10:
        del list_src_photo[10:]

    media_group = MediaGroupBuilder(caption=caption)
    for photo_url in list_src_photo:
        media_group.add_photo(media=photo_url)

    first_photo = types.URLInputFile(str(list_src_photo[0]))

    return media_group, first_photo


def get_tag(soup: BeautifulSoup) -> [int, int, str]:
    # constants to check the list "tags"
    NEED_WORDS_RUSSIAN = ["Количество комнат:", "Общая площадь:", "Этаж:", "Этажность:"]
    NEED_WORDS_UKRAINIAN = [
        "Кількість кімнат:",
        "Загальна площа:",
        "Поверх:",
        "Поверховість:",
    ]
    # parsing tags from the page
    tags = soup.find("ul", class_="css-rn93um").find_all("p")
    all_tag_text = []

    for need_word in NEED_WORDS_RUSSIAN:
        for tag in tags:
            if need_word in tag.text:
                all_tag_text.append(tag.text)

    for need_word in NEED_WORDS_UKRAINIAN:
        for tag in tags:
            if need_word in tag.text:
                all_tag_text.append(tag.text)

    print(all_tag_text)
    try:
        count_room = int((re.search(r"\d+", all_tag_text[0])).group())
    except:
        count_room = " "
    try:
        count_area = int((re.search(r"\d+", all_tag_text[1])).group())
    except:
        count_area = " "
    try:
        flour_have = int((re.search(r"\d+", all_tag_text[2])).group())
    except:
        flour_have = " "
    try:
        flour_everything = int((re.search(r"\d+", all_tag_text[3])).group())
    except:
        flour_everything = " "
    flour = f"{flour_have}/{flour_everything}"

    return count_room, count_area, flour


def get_money(soup: BeautifulSoup) -> [str, str]:
    # parsing money from the page
    money = soup.find("h2", text=re.compile(r".*грн.*"))

    if not money:
        money = soup.find("h3", text=re.compile(r".*грн.*"))

    if not money:
        money = soup.find("h4", text=re.compile(r".*грн.*"))

    if not money:
        return "Суму не знайдено", "#0грн"

    without_space = "".join(money.text.split())
    price = int((re.search(r"\d+", without_space)).group())

    return price, get_tags_for_money(price)


def get_caption(soup: BeautifulSoup) -> str:
    # parsing caption from the page
    caption_text = soup.find("div", class_="css-1o924a9")

    if not caption_text:
        return "Опис не знайдено. Повідомте розробника про помилку."

    if len(caption_text.text) > 800:
        return caption_text.text[0:800]

    return caption_text.text


def get_header(soup: BeautifulSoup) -> str | None:
    # parsing caption from the page
    caption_header = soup.find("h4", class_="css-1kc83jo")

    if not caption_header:
        return "Заголовок не знайдено. Повідомте розробника про помилку."

    return caption_header.text


def delete_words(text: str, words_to_remove: list) -> str:
    # Використовуємо регулярний вираз для визначення слова з можливими крапками
    pattern = re.compile(
        r"\b(?:" + "|".join(map(re.escape, words_to_remove)) + r")\b", re.IGNORECASE
    )
    print(text)

    # Замінюємо відповідні слова на порожні рядки
    result = pattern.sub("", text)
    print(result)

    return result


def create_pieces_caption(soup: BeautifulSoup) -> [str, str, str, str]:
    words = [
        "Від",
        "От",
        "я собственник",
        "я власнник",
        "посредников",
        "своя",
        "свою",
        "риелтор",
        "риелторов",
        "агентство",
        "агент",
        "маклер",
        "посредник",
        "личную",
        "хозяин",
        "собственник",
        "собственника",
        "хозяина",
        "хозяйка",
        "без комиссии",
        "агента",
        "агентства",
        "собственников",
        "посередників",
        "своя",
        "свою",
        "ріелтор",
        "ріелторів",
        "агентство",
        "агент",
        "маклер",
        "посередник",
        "посередник",
        "особисту",
        "власник",
        "власника",
        "власників",
        "хазяїнахазяйка",
        "хазяйка",
        "особисту",
        "без комісії",
        "Без рієлторів",
        "комісій",
        "Без риелторов",
        "комисий",
        "комісіЇ",
        "комисии",
    ]
    caption_text = delete_words(get_caption(soup), words)
    caption_header = delete_words(get_header(soup), words)

    metros_russian = [
        "Холодная Гора",
        "Южный вокзал",
        "Центральный рынок",
        "Площадь Конституции",
        "Гагарина",
        "Спортивная",
        "Малышева",
        "Турбоатом",
        "Дворец Спорта",
        "Армейская",
        "Масельского",
        "Тракторный завод",
        "Индустриальная",
        "Героев Труда",
        "Студенческая",
        "Барабашова",
        "Киевская",
        "Пушкинская",
        "Университет",
        "Исторический музей",
        "Победа",
        "Алексеевская",
        "23 Августа",
        "Ботанический сад",
        "Научная",
        "Госпром",
        "Архитектора Бекетова",
        "Защитников Украины",
        "Метростроителей",
        "Павлова",
    ]

    metro_ukrainian = [
        "Холодна Гора",
        "Південний вокзал",
        "Центральний ринок",
        "Площа Конституції",
        "Гагаріна",
        "Спортивна",
        "Малишева",
        "Турбоатом",
        "Палац Спорту",
        "Армійська",
        "Масельського",
        "Тракторний завод",
        "Індустріальна",
        "Героїв Праці",
        "Студентська",
        "Барабашова",
        "Київська",
        "Пушкінська",
        "Університет",
        "Історичний музей",
        "Перемога",
        "Олексіївська",
        "23 Серпня",
        "Ботанічний сад",
        "Наукова",
        "Держпром",
        "Архітектора Бекетова",
        "Захисників України",
        "Метробудівників",
        "Павлова",
    ]

    name_metro = ""
    print(name_metro)
    for metro in metros_russian:
        print(metro, metro in caption_text)
        if metro.lower() in caption_text.lower():
            name_metro = metro
            break

    if not name_metro:
        print(metro, metro in caption_text)
        for metro in metro_ukrainian:
            if metro.lower() in caption_text.lower():
                name_metro = metro
                break

    for metro in metros_russian:
        print(metro, caption_header, metro in caption_header)
        if metro.lower() in caption_header.lower():
            name_metro = metro
            break

    if not name_metro:
        print(metro, caption_header, metro in caption_header)
        for metro in metro_ukrainian:
            if metro.lower() in caption_header.lower():
                name_metro = metro
                break
    print(name_metro)

    count_room, count_area, flour = get_tag(soup)
    money, teg_money = get_money(soup)

    caption_info = (
        f"🏡{count_room}к кв\n"
        f"🏢Поверх: {flour}\n"
        f"🔑Площа: {count_area}м2\n"
        f"Ⓜ️Метро: {name_metro}\n"
    )
    caption_money = f"💳️{money} грн"
    caption_user = f"{caption_header}\n\nОпис: {caption_text}"
    caption_tag = f"#{count_room}ККВ #{teg_money}"
    caption_communication = (
        f"\n\nЗв'язок тут:\n" f"Написати ✍️ @realtor_057\n" f"Подзвонити ☎️ +380996643097"
    )

    return caption_info, caption_money, caption_user, caption_tag, caption_communication


def get_full_caption(
    caption_info, caption_money, caption_user, caption_tag, caption_communication
):
    return (
        f"{caption_info}"
        f"{caption_money}"
        f"\n\n{caption_user}\n\n"
        f"{caption_tag}"
        f"{caption_communication}"
    )


# Отримання тегу залежно від ціни
def get_tags_for_money(price):
    if 2000 <= price <= 5000:
        return "20005000грн"
    elif 5000 <= price <= 7000:
        return "50007000грн"
    elif 7000 <= price <= 9000:
        return "70009000грн"
    elif 9000 <= price <= 12000:
        return "900012000грн"
    elif 12000 <= price <= 14000:
        return "1200014000грн"
    elif 14000 <= price <= 15000:
        return "1400015000грн"
    elif price >= 15000:
        return "Выше15000грн"


# Отримання всіх даних і запуск надсилання
async def get_data(message: types.Message, state: FSMContext):
    soup: BeautifulSoup = get_url(message.text)
    (caption_info, caption_money, caption_user, caption_tag, caption_communication) = (
        create_pieces_caption(soup)
    )

    all_caption = get_full_caption(
        caption_info, caption_money, caption_user, caption_tag, caption_communication
    )
    all_photo, first_photo = get_photo(soup, all_caption)
    # storage of the necessary files

    await state.set_state(main.Caption.control)
    await state.update_data(
        all_photo=all_photo,
        first_photo=first_photo,
        caption_info=caption_info,
        caption_money=caption_money,
        caption_user=caption_user,
        caption_tag=caption_tag,
        caption_communication=caption_communication,
    )

    await message.answer_photo(
        caption=all_caption, photo=first_photo, reply_markup=await post_kb()
    )
