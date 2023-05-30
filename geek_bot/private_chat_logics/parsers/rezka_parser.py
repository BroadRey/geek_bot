from typing import List

import requests
from bs4 import BeautifulSoup

URL = 'https://rezka.ag/films/'
HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/110.0.0.0 Safari/537.36',
}


def get_html(url: str) -> requests.Response:
    response = requests.get(url, headers=HEADERS)
    return response


def get_data(html: str) -> List[dict[str, str]]:
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='b-content__inline_item')
    parsed_data = []

    for item in items:
        film_description = item.find(
            'div', class_='b-content__inline_item-link').find('div').string.split(', ')
        parsed_data.append(
            {
                'img': item.find('img').get('src'),
                'url': item.find('div', class_='b-content__inline_item-link').find('a').get('href'),
                'title': item.find('div', class_='b-content__inline_item-link').find('a').getText(),
                "year": film_description[0],
                "country": film_description[1],
                "genre": film_description[2],
            }
        )

    return parsed_data


def parse_rezka() -> List[dict[str, str]]:
    html = get_html(URL)
    if html.status_code != 200:
        raise Exception(f"Incorrect status code: {html.status_code}!")
    return get_data(html.text)
