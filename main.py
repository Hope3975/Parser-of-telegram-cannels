import requests
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
text = "БиржаGIF и Video733IT588SMM3857Telegram3560Авто и мото3145Авторский блог2747Азартные игры443Азербайджанские каналы28Анекдоты52Аниме600Армянские каналы69Афиша196Белорусские каналы339Бизнес и финансы8395Блогеры15971Военное216Все подряд21290Гороскоп3173Грузинские каналы32Даркнет1186Дизайн1752Для мужчин286Для родителей3084ЕГЭ и экзамены5634Здоровье3730Игры7640Инстаграм1407Искусство2756Казахстанские каналы214Каталог142Киргизские каналы44Коронавирус228Криптовалюты7993Кулинария4257Лайфхаки107Лингвистика2253Литература3259Магазин9394Медицина2934Мобайл1184Мода и красота8121Молдавские каналы40Музыка8883Наука и технологии5250Недвижимость502Новости21945Образование7969Однострочные153Подкасты77Подслушано184Политика7617Пошлое 18+16672Природа и животные2451Прогнозы и ставки6249Прокси10Психология6284Путешествия5956Разное147253Региональные1464Религия3478Рукоделие1157Сервисы103Сливы481Спорт4916Стикеры37Строительство и ремонт2313Таджикские каналы38Удаленная работа3864Узбекские каналы972Украинские каналы1703ФЕМ-ЛГБТ-БЛМ134Фильмы и сериалы6710Фото7736Халява и скидки1048Цитаты5946Чаты36168Шок-контент858Экология91Экономика4808Юмор8129Юриспруденция1477"
split_text = re.split(r'(\d+)', text)
text_array = [split_text[i] + split_text[i + 1] for i in range(0, len(split_text) - 1, 2)]
print(f"Пример тематик для поиска: {text_array}")
s = input("Тематика тг канала для парсинга: ")
url = f"https://tgramsearch.com/search?query={s}"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
pager_div = soup.find('div', {'class': 'tg-pager-wrapper'})
pager_items = pager_div.find_all('li', {'class': 'tg-pager-li'})
links = []
for item in pager_items:
    a_tag = item.find('a')
    if a_tag:
        href = a_tag.get('href')
        links.append("https://tgramsearch.com" + href)
base_url = "https://tgramsearch.com"
channel_data = []
for link in tqdm(links, desc="Processing links", unit="link"):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    channel_divs = soup.find_all('div', {'class': 'tg-channel-wrapper', 'class': 'is-list'})
    for channel in channel_divs:
        tg_channel_link = channel.find("div", class_="tg-channel-link")
        if tg_channel_link:
            a_tag = tg_channel_link.find("a")
            if a_tag:
                href = a_tag["href"]
                full_url = base_url + href
                response = requests.get(full_url)
                soup = BeautifulSoup(response.text, "html.parser")
                tg_channel_more = soup.find("div", class_="tg-channel-more")
                a_tag = tg_channel_more.find("a", class_="app") if tg_channel_more else None
                url_tg = a_tag["href"] if a_tag else None
                tg_channel_description = soup.find("div", class_="tg-channel-description")
                tg_channel_user = soup.find("div", class_="tg-channel-user")
                tg_user_count = tg_channel_user.find("span", class_="tg-user-count") if tg_channel_user else None
                if url_tg:
                    channel_data.append({
                        "url_tg": url_tg,
                        "description": tg_channel_description.text.strip() if tg_channel_description else None,
                        "subscribe": tg_user_count.text.strip() if tg_user_count else None
                    })
with open(f"{s}.json", "w", encoding="utf-8") as f:
    json.dump(channel_data, f, ensure_ascii=False, indent=4)