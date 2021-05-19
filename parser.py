import requests
from bs4 import BeautifulSoup
import csv


URL = 'https://www.asos.com/ru/women/kostyumy-i-kombinezony/cat/?cid=7618&ctaref=hp|ww|prime|feature|3|category|jumpsuits'
# имитация пользователя на сайте
HEADERS = {
    # network -> headers
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
    'accept': '*/*'
}
# HOST = 'https://www.asos.com'
FILE = 'asos_clothes.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    # определение количества страниц, для парсинга
    # pagination = soup.find_all(tag_name, class_=name)
    # print(pagination)
    # if pagination:
    #     return int(pagination[-1].get_text())
    # else:
    #     return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    # список элементов, которые нужно парсить
    items = soup.find_all('article', class_='_2qG85dG')

    # фильтрация и упорядочение требуемых элементов
    clothes = []
    for item in items:
        clothes.append({
            'title': item.find('div', class_='_3J74XsK').get_text(strip=True),
            'link': item.find('a', class_='_3TqU78D').get('href'),
            'price_rub': item.find('span', class_='_16nzq18').get_text(),
        })
    return clothes


def save_file(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Цена в рублях'])
        for item in items:
            print(item)
            writer.writerow([item['title'], item['link'], item['price_rub']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        clothes = []
        # количество страниц
        # pages_count = get_pages_count(html.text)
        for page in range(1, 8):
            print(f'Парсинг страницы {page} из {8}...')
            html = get_html(URL, params={'page': page})
            clothes.extend(get_content(html.text))
            # clothes = get_content(html.text)
        save_file(clothes, FILE)
        print(f'Получено {len(clothes)} вида одежы')
    else:
        print('error')


parse()
