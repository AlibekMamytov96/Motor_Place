import requests
from bs4 import BeautifulSoup as BS


def get_html(url):
    response = requests.get(url)
    # get, post, put/patch, delete
    return response.text


def get_data(html):
    soup = BS(html, 'lxml')
    catalog = soup.find('div', class_='row mb-3')
    cars = catalog.find_all('div', class_='car col-12 col-sm-6 col-lg-4 col-xl-3 mb-4')
    cars_list = []
    for car in cars:
        try:
            title = car.find('h3', class_='text-truncate h6 mb-1').text.strip()
        except:
            title = 'Title not found'
        try:
            price = car.find('b', class_='float-right').text.strip()
        except:
            price = 'Price not found'
        try:
            img = car.find('div', class_='card-img-top').find('a', class_='d-block').find('img').get('src')
            print(img)
        except:
            img = 'Image not found'

        data = {'title': title, 'price': price, 'image': img}
        cars_list.append(data)
    return cars_list


TOTAL_PAGES = 2


def main():
    data = []
    for page in range(1, TOTAL_PAGES+1):
        url = f'https://turbo.kg/?page={page}#scroll'
        data.extend(get_data(get_html(url)))
    return data