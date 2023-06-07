import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
# -----------------------------------------------------------
"""
##############: Changelog
##############: Version 1.25
##############: Created at https://t.me/Krauf_7802
*
*
*
$ Изменен метод парсинга данных на страницах.
$ Улучшен код.
*
*
*
"""
# -----------------------------------------------------------

# Получение информации от пользователя
s = input("Тематика тг канала для парсинга: ")

base_url = "https://tgramsearch.com"
channel_data = []

# Конструктор url
url = f"https://tgramsearch.com/search?query={s}&page=1"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Поиск самого большого числа по страницам
pager_div = soup.find('div', {'class': 'tg-pager-wrapper'})
pager_items = pager_div.find_all('li', {'class': 'tg-pager-li'})
num_pages = max(int(item.text) for item in pager_items if item.text.isdigit())

# Основной цикл скрипта 
for page in tqdm(range(1, num_pages + 1), desc="Processing:>", unit="page"):
    # Конструкция url по полученным данным по найденному max числу
    url = f"https://tgramsearch.com/search?query={s}&page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    channel_divs = soup.find_all('div', {'class': 'tg-channel-wrapper', 'class': 'is-list'})
    
    # Основной цикл парсинга
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

# Сохранение данных в json файл
with open(f"{s}.json", "w", encoding="utf-8") as f:
    json.dump(channel_data, f, ensure_ascii=False, indent=4)
