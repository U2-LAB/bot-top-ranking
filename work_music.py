import requests

from bs4 import BeautifulSoup as BS
from progress.bar import Bar
import random

# CHARTS_URL = r'https://megapesni.com/online/'
CHARTS_URL = r'https://megapesni.com/rock_chart.html'
MAIN_URL = r'https://megapesni.com'
OK_STATUS_CODE = 200


def get_links(count_music):
    response = requests.get(CHARTS_URL)
    if response.status_code != OK_STATUS_CODE:
        return []
    page = BS(response.text, 'html.parser')
    download_links_a = page.find_all('a', class_='popular-download-link')
    random.shuffle(download_links_a)
    links = []
    titles = []

    for link in download_links_a[:count_music]:
        response = requests.get(MAIN_URL + str(link.get('href')))
        if response.status_code != OK_STATUS_CODE:
            continue
        download_page = BS(response.text, 'html.parser')
        links.append(download_page.find('a', class_='song-author-btn song-author-btn--download').get('href'))
        title = download_page.find('h1', class_='music-title').text
        titles.append(title)
    return links, titles


def download_music_link(music_link):
    link = MAIN_URL + music_link
    req= requests.get(link, stream=True)
    if req.status_code == OK_STATUS_CODE:
        with open('song.mp3', 'wb') as mp3:
            mp3.write(req.content)
