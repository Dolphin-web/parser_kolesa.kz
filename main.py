import requests
import json
import os
import unicodedata
from bs4 import BeautifulSoup 
import operator

URL = 'https://kolesa.kz/cars/' 
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36','accept': '*/*'}
HOST = 'https://kolesa.kz/'
FILE = str(os.path.abspath(os.getcwd())) + '/file.json'

def get_html(url, params=None):
#получение html структуры сайта
	r = requests.get(url, headers=HEADERS, params=params)
	return r

def get_pages_count(html):
# колличество страниц для парсинга
	return int(5)

def get_content(html):
#получение данных объявления
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='a-elem')
	cars = []
	for item in items:
		cars.append({
			'title': item.find('span', class_='a-el-info-title').find_next('a').get_text(strip=True),
			'price': ''.join(filter(str.isdigit, item.find('span', class_='price').get_text())),
			'public_date': item.find('span', class_='date').get_text(strip=True),
			'link': HOST + item.find('a').get('href'),
			'city': item.find('div', class_='list-region').get_text(strip=True),
			})
	return cars

def save_file(items, path):
#сохранение в формате json с поддержкой кириллицы
	with open(path, 'w', encoding ='utf-8', newline='') as file:
		json.dump(items, file, sort_keys=False, indent=3, ensure_ascii=False, separators=(',', ': '))

def parse():
	html = get_html(URL)
	if html.status_code == 200:
		cars = []
		pages_count = get_pages_count(html.text)
		for page in range(1, pages_count + 1):
			print(f'Парсинг страницы {page} из {pages_count}')
			html = get_html(URL, params = {'page' : page})
			cars.extend(get_content(html.text))		
		save_file(cars, FILE)
		print(f'Получено {len(cars)} автомобилей')
		os.startfile(FILE)
	else:
		print('Error')

parse()
