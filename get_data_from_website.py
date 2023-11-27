import pandas as pd
import requests
from bs4 import BeautifulSoup

URLs = []
labels = []
products = []

def df_to_excel(df, output_file_path, sheet_name):
    with pd.ExcelWriter(output_file_path, mode='a', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def excel_to_df(input_file_path, sheet_name):
    df = pd.read_excel(input_file_path, sheet_name=sheet_name)
    return df

def get_label_from_vg(a_tag):
    temp = a_tag.get('href')
    if 'https://' not in temp:
        temp = 'https://vatgia.com' + temp
    response = requests.get(temp)
    soup = BeautifulSoup(response.content, 'html.parser')
    div_1 = soup.find(id='category_list_picture')
    div_2 = soup.find(id='category_list')
    div_3 = soup.find_all('div', 'box_cate_vg')

    if div_1 is not None:
        for a in div_1.find_all('a'):
            URLs.append(a.get('href'))
            labels.append(a.text.strip())

    if div_2 is not None:
        for a in div_2.find_all('a'):
            URLs.append(a.get('href'))
            labels.append(a.text.strip())

    if div_3 is not None:
        for div in div_3:
            a_tags = div.find_all('a')
            for a_tag in a_tags:
                labels.append(a_tag.text.strip())
                URLs.append(a_tag.get('href'))
                get_label_from_vg(a_tag)

def get_data_from_lasenza(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    ul = soup.find(id='search-result-items')
    divs = ul.find_all('div', 'product-tile')

    product_urls = []
    #print(len(divs))
    for div in divs:
        a_tag = div.find('a', 'thumb-link rollover')
        # print(a_tag)
        if a_tag is not None:
            product_urls.append(a_tag.get('href'))
    # print(len(product_urls))
    get_products_data(product_urls=product_urls) 

def get_products_data(product_urls):
    #i = 0
    for url in product_urls:
        if 'lasenza.com' not in url:
            url = 'lasenza.com' + url
        if 'https://' not in url:
            url = 'https://' + url
        response = requests.get(url)
        # i += 1
        # print(i)
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find('div', 'product-col-2 product-detail')
        variation_div = div.find('div', 'product-variations')

        collection = div.find('h2', 'product-collection')
        name = div.find('h1', 'product-name')
        product_number_div = div.find('div', 'product-number')
        span = product_number_div.find('span')
        ##
        color = variation_div.find('ul', 'swatches color')
        #print(color)
        color_list = color.find_all('li', 'selectable')
        all_color = []
        for li in color_list:
            div = li.find('div', 'image-wrapper')
            img = div.find('img')
            src_url = img['src']
            color_code = src_url.split('/')[-1].split('.')[0]
            all_color.append(str(color_code))
        ##
        size = variation_div.find('ul', 'swatches size')
        #print(size)
        s_list = size.find_all('li', 'selectable')
        all_size = [li.find('a').text.strip() for li in s_list]
        ##
        cup = variation_div.find('ul', 'swatches cup')
        #print(cup)
        if cup is not None:
            c_list = cup.find_all('li', 'selectable')
            all_cup = [li.find('a').text.strip() for li in c_list]
            combinations = [x + y for x in all_size for y in all_cup]
        else:
            combinations = all_size
        #print(combinations)
        for s in combinations:
            if collection is not None:
                for c in all_color:
                    result_string = 'Others Lasenza ' + collection.text.strip() + ' ' + name.text.strip() + ' ' + span.text.strip() + ' - ' + c.strip() + ' Size ' + s.strip()
            else: 
                for c in all_color:
                    result_string = 'Others Lasenza ' + name.text.strip() + ' ' + span.text.strip() + ' - ' + c.strip() + ' Size ' + s.strip()
            #print(result_string)
            products.append(result_string)

if __name__ == "__main__":
    URL = "https://vatgia.com"
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    if 'vatgia.com' in URL:
        divs = soup.find_all('div', 'box_cate_vg')
        for div in divs:
            a_tags = div.find_all('a')
            for a_tag in a_tags:
                labels.append(a_tag.text.strip())
                URLs.append(a_tag.get('href'))
                get_label_from_vg(a_tag)
        # div = soup.find('div', 'mega_menu')
        # ul = div.find('ul', 'mega_menu_navigate')
        # list = ul.find_all('li', 'navigate')
        # for li in list:
        #     div_list = li.find_all('div', 'sub')
        #     for d in div_list:
        #         a = d.find('a')
        #         if a and 'hot' in a.get('class', []):
        #             continue
        #         else:
        #             URLs.append(a.get('href'))
        #             labels.append(a.text.strip())

        results = {'Label':labels, 'URL':URLs}
        with open('vg_products_by_labels2', mode='w', encoding='utf8') as file:
            for label, url in zip(results['Label'], results['URL']):
                if label is not None and len(label) > 1 and url is not None:
                    file.write(f"Label: {label}, URL: {url}\n")
        print(len(labels))
        print(len(URLs))
        print("Data extraction completed.")
    
    if 'lasenza.com' in URL:
        uls = soup.find('ul', 'menu-category level-1')
        a_tags = uls.find_all('a', 'has-sub-menu')
        for a_tag in a_tags:
            URLs.append(a_tag.get('href'))
            labels.append(a_tag.text.strip())
        
        for i in range(len(labels)-1, -1, -1):
            if labels[i] == 'New' or labels[i] == 'Clearance':
                labels.pop(i)
                URLs.pop(i)
        
        get_data_from_lasenza('https://www.lasenza.com/accessories')
        with open('lasenza_products.txt', 'a', encoding='utf8') as file:
            for item in products:
                file.write(str(item) + '\n')
        print('Done')
            
