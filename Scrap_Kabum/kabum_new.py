import re
import requests
import datetime
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import numpy as np
import random
import scrape_proxy as sp

proxies_list = sp.get_proxy_list()

def get_randomProxy():
    proxies = {
        'http': random.choice(proxies_list)
    }
    return proxies

def get_parsed_page(url,proxy):
    # This fixes a blocked by cloudflare error i've encountered
    headers = {
        "referer": "https://www.kabum.com.br/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        print('Trying proxy...')
        return BeautifulSoup(requests.get(url, headers=headers, proxies=proxy).text, "lxml")
    except:
        get_parsed_page(url,get_randomProxy())

def busca_produtos(url):
    print('Buscando pagina...')
    try:
        page = get_parsed_page(url,get_randomProxy())
    except Exception as e:
        print('Falha ao buscar a pagina')
        print(e)
        return None
    prod_arr = []
    produtos = page.find_all('div', {'class': re.compile(r'productCard')})
    for produto in produtos:
        prod_obj = {}
        name = produto.find('h2', {'class': re.compile(r'nameCard')})
        preco = produto.find('span', {'class': re.compile(r'priceCard')})
        codigo = produto.find('a',{'href':re.compile(r'/produto/')})['href']
        codigo = codigo[codigo.find('/produto/')+9:]
        codigo = codigo[:codigo.find('/')]
        if '---' in preco.text:
            continue
        prod_obj['name'] = name.text
        prod_obj['id'] = codigo
        prod_obj['preco'] = preco.text.replace(u'R$\xa0','')
        classe = url[url.find('.br/')+4:url.find('?')]
        prod_obj['Classe'] = classe[:classe.find('/')]
        prod_obj['Tipo'] = classe[classe.find('/')+1:]
        prod_obj['Data'] = datetime.datetime.today().strftime("%d/%m/%Y")
        prod_arr.append(prod_obj)
    return prod_arr

#busca_produtos(page)
#hardware/placa-de-video-vga
def busca_categoria(categoria):
    all_prod = []
    for i in range(1, 11, 1):
        url = "https://www.kabum.com.br/"+ categoria +"?page_number="+ str(i) +"&page_size=100&facet_filters=&sort=most_searched"
        produtos = busca_produtos(url)
        if produtos == None:
            print('Ending Code')
            return None
        if len(produtos) < 100:
            all_prod = all_prod +produtos
            print('Busca de '+ categoria +' Completa...')
            return all_prod
        all_prod = all_prod +produtos
        print('Proxima pagina '+ categoria +' - ' + str(i))


vga = busca_categoria('hardware/placa-de-video-vga')
print('stop')