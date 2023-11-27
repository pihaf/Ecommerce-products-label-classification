from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_lazy_load_products(URL):
    # Set up Selenium
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    service = Service(r'C:\Users\DEll\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Specify the path to your ChromeDriver executable
    driver = webdriver.Chrome(service=service, options=options)

    # Load the page using Selenium
    driver.get(URL)

    # # Find the product divs
    # product_divs = driver.find_elements(By.CSS_SELECTOR, '.CatalogProducts__Wrapper-sc-1hmhz3p-0.fSXJZx .name h3')

    # Find the product divs
    product_divs = driver.find_elements(By.CSS_SELECTOR, '.ProductList__NewWrapper-sc-1dl80l2-0.jXFjHV .name h3')

    # Extract the product names
    products = [div.text.strip() for div in product_divs]

    # Print the product names
    print(products)

    # Write the products to a file
    with open('./tiki/product_list.txt', 'a', encoding='utf-8') as file:
        for product in products:
            file.write(product + '\n')

    print('Done')
    # Quit the driver
    driver.quit()

def get_products(URL):
    headers = []
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
    product_div = soup.find('div', 'ProductList__NewWrapper-sc-1dl80l2-0 jXFjHV')
    h3 = product_div.find_all('h3')
    products = []
    for name in h3:
        products.append(name.text.strip())

    print(products)

get_lazy_load_products('https://tiki.vn/dien-thoai-smartphone/c1795')




    
