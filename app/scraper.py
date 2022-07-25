# Import main modules
import re
import json
from time import sleep
from pprint import pprint
from itertools import zip_longest

# Import selenium and webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Import modules for scraping
from bs4 import BeautifulSoup

# WebDriver service
SERVICE = Service(ChromeDriverManager().install())

# Chrome options
OPTIONS = Options()
OPTIONS.add_argument('disable-notifications')
OPTIONS.add_argument('--disable-infobars')
OPTIONS.add_argument('start-maximized')
OPTIONS.add_argument('disable-infobars')


def scraper(search: str, url: str='https://lista.mercadolivre.com.br/'):
    # Removing white spaces
    search = re.sub(r'\s+', '-', search)
    full_url = f'{url}{search}'
    
    # Browser
    browser = webdriver.Chrome(service=SERVICE, options=OPTIONS)
    
    # Getting the HTML from selenium
    browser.get(full_url)
    sleep(5)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    
    # Making soup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Finding elements
    li = soup.find_all('li', class_='ui-search-layout__item')
    # Finding <a> tag
    a = [x.find('a', class_='ui-search-result__content') for x in li]
    # Getting the links
    links = [x['href'] for x in a]
    # Getting title of the products
    title = [x['title'] for x in a]
    # Getting price of the products
    price = [x.find('span', class_='price-tag-fraction').string for x in a]
    
    info = {
        x: {
            'title': y,
            'link': z,
            'price': f'R$ {a}'
        } for x, y, z, a in zip_longest(range(len(title)), title, links, price)
    }
    
    # Close chrome
    browser.quit()

    return info


if __name__ == '__main__':
    product = input('Digite o nome do produto: ')
    # Saving the info in a JSON file
    with open('produtos.json', 'w', encoding='utf8') as json_file:
        json.dump(scraper('tv'), json_file)
