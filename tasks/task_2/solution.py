import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from collections import defaultdict
import time

from typing import Dict


def get_category_counts(base_url: str) -> Dict:
    letter_counts = defaultdict(int)
    next_page_url = base_url

    # перебираем страницы пока будет ссылка на следующую
    while next_page_url:
        response = requests.get(next_page_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # находим только основной контент без подкатегорий
        content_div = soup.find('div', id='mw-pages')
        if not content_div:
            break

        # обрабатываем группы
        groups = content_div.find_all('div', class_='mw-category-group')
        for group in groups:
            letter = group.find('h3').text.strip().upper()
            items = group.find_all('a')
            letter_counts[letter] += len(items)

        # проверяем наличие следующей страницы
        next_link = content_div.find('a', string='Следующая страница')
        next_page_url = urljoin(base_url, next_link['href']) if next_link else None

        # для неблокирования википедией запросов
        time.sleep(0.2)

    return letter_counts


def save_to_csv(
    data: Dict,
    filename: str,
    add_zero_counts: bool,
    only_russian_letters: bool,
) -> pd.DataFrame:  # return датафрейма для тестов

    russian_letters = [chr(i) for i in range(1040, 1072)]  # А-Я
    sorted_data = []

    # добавляем русские буквы с нулевыми значениями
    for letter in russian_letters:
        count = data.get(letter, 0)
        if not add_zero_counts and not count:
            continue
        sorted_data.append((letter, count))

    if not only_russian_letters:
        # добавляем латинские символы для латинских названий
        extra_chars = [k for k in data if k not in russian_letters]
        sorted_data += [(k, data[k]) for k in sorted(extra_chars)]

    # записываем данные в .csv файл
    letter_counts = pd.DataFrame(sorted_data)
    letter_counts.columns = ['Буква', 'Количество']
    letter_counts.to_csv(filename, sep=',', encoding='utf-8', index=False)
    return letter_counts


def get_and_write_category_counts(
    url: str,  # ссылка на Вики в разделе категория
    output_file: str,  # путь к итоговому файлу
    add_zero_counts: bool = True,   # добавление русских букв с нулевыми счетчиками
    only_russian_letters: bool = True,   # добавление латинских букв, если они были
):
    return save_to_csv(
        get_category_counts(url),
        output_file,
        add_zero_counts,
        only_russian_letters,
    )


if __name__ == "__main__":
    URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    FILENAME = "beasts.csv"
    get_and_write_category_counts(URL, FILENAME)
    print(f"Данные сохранены в {FILENAME}")
