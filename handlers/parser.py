import re
import requests
from aiogram import types
from bs4 import BeautifulSoup
from handlers import main
from handlers.keyboard import post_kb
from aiogram.fsm.context import FSMContext

def get_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


class Information():
    def get_photo(soup: BeautifulSoup) -> [list, types.URLInputFile]:
        photo = soup.find("div", class_="swiper-wrapper").find_all("img")

        list_src_photo = []  # список src фото

        for src in photo:
            list_src_photo.append(src.get("src"))

        if len(list_src_photo) > 10:
            del list_src_photo[10:]

        media_group = []
        for photo_url in list_src_photo:
            media_group.append(types.InputMediaPhoto(media=photo_url))

        first_photo = types.URLInputFile(str(list_src_photo[0]))

        return media_group, first_photo

    def get_tag(soup: BeautifulSoup) -> [int, int, str]:
        # constants to check the list "tags"
        NEED_WORDS_RUSSIAN = ["Количество комнат:", "Общая площадь:",
                              "Этаж:", "Этажность:"]
        NEED_WORDS_UKRAINIAN = ["Кількість кімнат:",
                                "Загальна площа:","Поверх:", "Поверховість:"]
        # parsing tags from the page
        tags = soup.find("ul", class_="css-sfcl1s").find_all("p")
        all_tag_text = []

        for need_word in NEED_WORDS_RUSSIAN:
            for tag in tags:
                if need_word in tag.text:
                    all_tag_text.append(tag.text)
        
        for need_word in NEED_WORDS_UKRAINIAN:
            for tag in tags:
                if need_word in tag.text:
                    all_tag_text.append(tag.text)
        
        count_room = int((re.search(r"\d+", all_tag_text[0])).group())
        count_area = int((re.search(r"\d+", all_tag_text[1])).group())
        flour_have = int((re.search(r"\d+", all_tag_text[2])).group())
        flour_everything = int((re.search(r"\d+", all_tag_text[3])).group())
        flour = f"{flour_have}/{flour_everything}"

        return count_room, count_area, flour
            
    def get_money(soup: BeautifulSoup) -> [str, str]:
        # parsing money from the page
        money = soup.find("h2", text=re.compile(r'.*грн.*'))
    
        if not money:
            money = soup.find("h3", text=re.compile(r'.*грн.*'))

        if not money:
            money = soup.find("h4", text=re.compile(r'.*грн.*'))

        if not money:
            return "Суму не знайдено", "#0грн"
        
        without_space = "".join(money.text.split())
        price = int((re.search(r"\d+", without_space)).group())

        return money.text, get_tags_for_money(price) 

    def get_caption(soup: BeautifulSoup) -> str:
        # parsing caption from the page
        caption_text = soup.find("div", class_="css-1t507yq er34gjf0")

        if not caption_text:
            return "Описание не найдено"

        if len(caption_text.text) > 800:
           return caption_text.text[0:800]

        return caption_text.text
    
    def get_header(soup: BeautifulSoup) -> str | None:
        # parsing caption from the page
        caption_header = soup.find("h1")

        if not caption_header:
            return None

        return caption_header.text

    def create_pieces_caption(soup: BeautifulSoup) -> [str, str, str, str]:
        caption_text = Information.get_caption(soup)
        caption_header = Information.get_header(soup)

        metros_russian = ["Холодная Гора", "Южный вокзал",
                  "Центральный рынок", "Площадь Конституции",
                  "Проспект Гагарина", "Спортивная",
                  "Завод им. Малышева", "Турбоатом",
                  "Дворец Спорта", "Армейская",
                  "Имени А. С. Масельского", "Тракторный завод",
                  "Индустриальная", "Героев Труда",
                  "Студенческая", "Академика Барабашова",
                  "Киевская", "Пушкинская", "Университет",
                  "Исторический музей", "Победа",
                  "Алексеевская", "23 Августа", "Ботанический сад",
                  "Научная", "Госпром", "Архитектора Бекетова", "Защитников Украины",
                  "Метростроителей"]

        metro_ukrainian = ["Холодна Гора", "Південний вокзал",
                  "Центральний ринок", "Площа Конституції",
                  "Проспект Гагаріна", "Спортивна",
                  "Завод ім. Малишева", "Турбоатом",
                  "Палац Спорту", "Армійська",
                  "Імені А. С. Масельського", "Тракторний завод",
                  "Індустріальна", "Героїв Праці",
                  "Студентська", "Академіка Барабашова",
                  "Київська", "Пушкінська", "Університет",
                  "Історичний музей", "Перемога",
                  "Олексіївська", "23 Серпня", "Ботанічний сад",
                  "Наукова", "Держпром", "Архітектора Бекетова", "Захисників України",
                  "Метробудівників"]
        
        name_metro = ""

        for metro in metros_russian:
            if metro in caption_text:
                name_metro = metro
                break
            
        if not name_metro:
            for metro in metro_ukrainian:
                if metro in caption_text:
                    name_metro = metro
                    break

        if name_metro == "":

            for metro in metros_russian:
                if metro in caption_header:
                    name_metro = metro
                    break

            if not name_metro:
                for metro in metro_ukrainian:
                    if metro in caption_header:
                        name_metro = metro
                        break


        count_room, count_area, flour = Information.get_tag(soup)
        money, teg_money = Information.get_money(soup)

        caption_info = (f"🏡{count_room}к кв\n"
            f"🏢Этаж: {flour}\n"
            f"🔑Площадь: {count_area}м2\n"
            f"Ⓜ️Метро: {name_metro}\n")
        caption_money = f"💳️{money}"
        caption_user = (f"Описание: {caption_text}")
        caption_tag = (f"#{count_room}ККВ #{teg_money}")
        caption_communication = (f"\n\nСвязь тут:\n"
            f"Написать ✍️ @realtor_057\n"
            f"Позвонить ☎️ +380996643097")
        
        return caption_info, caption_money, caption_user, caption_tag, caption_communication
    
    def get_full_caption(caption_info, caption_money, caption_user, caption_tag, caption_communication):
        return (f"{caption_info}"
                f"{caption_money}"
                f"\n\n{caption_user}\n\n"
                f"{caption_tag}"
                f"{caption_communication}")
    


# Отримання тегу залежно від ціни
def get_tags_for_money(price):
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
async def get_data(message: types.Message, state: FSMContext):
    soup: BeautifulSoup = get_url(message.text)
    all_photo, first_photo = Information.get_photo(soup)
    (
     caption_info, 
     caption_money, 
     caption_user, 
     caption_tag, 
     caption_communication
    ) = Information.create_pieces_caption(soup)
    
    all_caption = Information.get_full_caption(caption_info, 
                                               caption_money, 
                                               caption_user, 
                                               caption_tag, 
                                               caption_communication)

    # storage of the necessary files
    await state.set_state(main.Caption.control)
    await state.update_data(all_photo=all_photo, first_photo=first_photo,
                            caption_info=caption_info, caption_money=caption_money, caption_user=caption_user,
                            caption_tag=caption_tag, caption_communication=caption_communication)

    await message.answer_photo(caption=all_caption, photo=first_photo, reply_markup=await post_kb())
