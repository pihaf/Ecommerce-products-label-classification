import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

URLs =['https://vatgia.com/433/mobile.html', 'https://vatgia.com/846/server-may-chu.html']
labels = ['Mobile', 'Server (Máy chủ)']

for URL, label in zip(URLs, labels):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', 'name')
    products = []
    temp_labels = []
    for div in divs:
        a = div.find('a')
        if a is not None:
            products.append(a.text.strip())
            temp_labels.append(label)

    df = pd.DataFrame({'Label': temp_labels, 'Product Name': products})
    df.to_csv('test.csv', index=False, mode='a', header=False)
    time.sleep(2)
