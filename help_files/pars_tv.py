from requests_html import HTMLSession  
import requests
from bs4 import BeautifulSoup
from time import sleep
import numpy as np
import pandas as pd
import random
import datetime, threading, time

def get_maxpage():
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    session = HTMLSession()
    r = session.get('https://philips-philips.ru/televizory/', headers=user_agent)
    links = r.html.absolute_links
    links2 = [i for i in links if 'https://philips-philips.ru/televizory?page' in i]
    maxpage = max([int(i[42:]) for i in sorted(links2)])
    return maxpage

def get_html(url):
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    r = requests.get(url, headers=user_agent)
    return r.text

def get_html2(url):
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    session = HTMLSession()
    r = session.get(url, headers=user_agent)
    return r.text

def get_prices(method, maxpage):
    dd = []
    for page in range(maxpage+2):
        sec = random.randint(1,5)
        sleep(sec)
        url = 'https://philips-philips.ru/televizory?page='+str(page)

        html = method(url)
        soup = BeautifulSoup(html, 'lxml')
        tvs = soup.find_all('div', {'data-product-category':"Телевизоры"})
        for tv in tvs:
            sku = tv.find('div', class_="rating-wrapper")['data-productsku']
            name = tv.find('div', class_="teaser-title").text
            try:
                prices = tv.find('div', class_="field-item").text.split()
            except:
                prices = tv.find('div', class_="field field-name-commerce-price field-type-commerce-price field-label-hidden").text.split()
            price = ''
            for i in prices[:-1]:
                price = price + i
            dd.append([sku,name,int(price)])
    df = pd.DataFrame(dd, columns=['sku', 'name', 'price'])
    return df

def get_df_final():
    maxpage = get_maxpage()
    df1 = get_prices(method=get_html, maxpage=maxpage)
    df2 = get_prices(method=get_html2, maxpage=maxpage)
    result=pd.concat([df1, df2], axis=0)
    result.drop_duplicates(inplace=True)
    result.sort_values(by='price', inplace=True, ascending=False)
    result.reset_index(inplace=True, drop=True)
    result.index.name = 'index'
    return result

def get_percent(x,y):
    try:
        return round((x-y)/y*100, ndigits=1)
    except:
        return x
def daily_download_call():
    result2 = get_df_final()
    result = pd.read_csv('result.csv', index_col='index')
    result2.to_csv('result.csv')
    result2['price_yesterday'] = '_'
    for i in range(len(result2)):
        for j in range(len(result)):
            if result2.iloc[i,1] == result.iloc[j,1]:
                result2.iloc[i,3] = result.iloc[j,2]    
    result2['percent'] = '_'
    for i in range(len(result2)):
        result2.iloc[i,4] = get_percent(result2.iloc[i,3], result2.iloc[i,2])
    result2.to_excel('dayli_file_to_sent.xlsx')
    del result, result2

    threading.Timer(86400, daily_download_call ).start()
daily_download_call()
