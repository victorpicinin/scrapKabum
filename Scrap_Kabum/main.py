import re
import requests
import datetime
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import numpy as np
from selenium import webdriver

from lxml import html
import time
from datetime import date
import pysql as pysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
today = date.today()

def get_produtos(URL):
    output = pd.DataFrame()
    driver.get(URL)
    time.sleep(1)
    produtos = driver.find_elements_by_xpath("//*[@class='sc-fzqARJ eITELq']")
    try:
        CAT = driver.find_elements_by_xpath("//*[@class='sc-AxirZ kIolVN']")[1].text
    except Exception as e:
        print(e)
        CAT = driver.find_elements_by_xpath("//*[@class='sc-AxirZ kIolVN']")[0].text

    for produto in produtos:
        print(produto.find_element_by_xpath("./div/div[1]/a").text)
        print(produto.find_element_by_xpath("./div/div[2]/div[1]/div[2]").text)
        print(produto.find_element_by_xpath("./div/div[2]/div[1]/div[3]").text)
        print(produto.find_element_by_xpath("./div/div[2]/div[1]/div[4]").text)
        if produto.find_element_by_xpath("./div/div[2]/div[1]/div[2]").text == 'Em até 12X sem juros':
            preco_produto = produto.find_element_by_xpath("./div/div[2]/div[1]/div[3]").text
            #print(produto.find_element_by_xpath("./div/div[2]/div[1]/div[3]").text)
        else:
            preco_produto = produto.find_element_by_xpath("./div/div[2]/div[1]/div[4]").text
            #print(produto.find_element_by_xpath("./div/div[2]/div[1]/div[2]").text)
        nome = produto.find_element_by_xpath("./div/div[1]/a").text
        marca = produto.find_element_by_xpath("./div/div[1]/div[2]/img").get_attribute('alt')
        preco_produto = preco_produto.replace('R$ ','').replace('.','').replace(',','.')
        url_produto = produto.find_element_by_css_selector("a[href*='/produto/']").get_attribute('href')
        codigo_produto = url_produto[33:url_produto[33:len(url_produto)].find('/')+33]
        produto = {'CODIGO':codigo_produto,'MARCA':marca,'CATEGORIA': CAT ,'PRECO': preco_produto,'DATA':today.strftime("%d/%m/%Y"),'NOME':nome,'URL': url_produto}
        output = output.append(produto, ignore_index=True)
        print(produto)
    return output


vga1 = get_produtos('https://www.kabum.com.br/hardware/placa-de-video-vga?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
vga2 = get_produtos('https://www.kabum.com.br/hardware/placa-de-video-vga?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
vgas = [vga1,vga2]
vgas = pd.concat(vgas)

cpu1 = get_produtos('https://www.kabum.com.br/hardware/processadores?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
cpu2 = get_produtos('https://www.kabum.com.br/hardware/processadores?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
cpus = [cpu1,cpu2]
cpus = pd.concat(cpus)

ram1 = get_produtos('https://www.kabum.com.br/hardware/memoria-ram?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
ram2 = get_produtos('https://www.kabum.com.br/hardware/memoria-ram?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
ram3 = get_produtos('https://www.kabum.com.br/hardware/memoria-ram?pagina=3&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
ram4 = get_produtos('https://www.kabum.com.br/hardware/memoria-ram?pagina=4&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
ram5 = get_produtos('https://www.kabum.com.br/hardware/memoria-ram?pagina=5&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
ram6 = get_produtos('https://www.kabum.com.br/hardware/memoria-ram?pagina=6&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
rams = [ram1,ram2,ram3,ram4,ram5,ram6]
rams = pd.concat(rams)

ssd1 = get_produtos('https://www.kabum.com.br/hardware/ssd-2-5?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
ssd2 = get_produtos('https://www.kabum.com.br/hardware/ssd-2-5?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
ssd3 = get_produtos('https://www.kabum.com.br/hardware/ssd-2-5?pagina=3&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
ssds = [ssd1,ssd2,ssd3]
ssds = pd.concat(ssds)

mdboard1 = get_produtos('https://www.kabum.com.br/hardware/placas-mae?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
mdboard2 = get_produtos('https://www.kabum.com.br/hardware/placas-mae?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
mdboard3 = get_produtos('https://www.kabum.com.br/hardware/placas-mae?pagina=3&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
mdboard4 = get_produtos('https://www.kabum.com.br/hardware/placas-mae?pagina=4&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
mdboards = [mdboard1,mdboard2,mdboard3,mdboard4]
mdboards = pd.concat(mdboards)

pwr1 = get_produtos('https://www.kabum.com.br/hardware/fontes?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
pwr2 = get_produtos('https://www.kabum.com.br/hardware/fontes?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
pwr3 = get_produtos('https://www.kabum.com.br/hardware/fontes?pagina=3&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
pwrs = [pwr1,pwr2,pwr3]
pwrs = pd.concat(pwrs)

headset1 = get_produtos('https://www.kabum.com.br/perifericos/headset-gamer?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
headset2 = get_produtos('https://www.kabum.com.br/perifericos/headset-gamer?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
headset3 = get_produtos('https://www.kabum.com.br/perifericos/headset-gamer?pagina=3&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
headsets = [headset1,headset2,headset3]
headsets = pd.concat(headsets)

mouse1 = get_produtos('https://www.kabum.com.br/perifericos/-mouse-gamer?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
mouse2 = get_produtos('https://www.kabum.com.br/perifericos/-mouse-gamer?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
mouse3 = get_produtos('https://www.kabum.com.br/perifericos/-mouse-gamer?pagina=3&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
mouse4 = get_produtos('https://www.kabum.com.br/perifericos/-mouse-gamer?pagina=4&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
mouse5 = get_produtos('https://www.kabum.com.br/perifericos/-mouse-gamer?pagina=5&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
mouse6 = get_produtos('https://www.kabum.com.br/perifericos/-mouse-gamer?pagina=6&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
mouses = [mouse1,mouse2,mouse3,mouse4,mouse5,mouse6]
mouses = pd.concat(mouses)

keyb1 = get_produtos('https://www.kabum.com.br/perifericos/teclado-gamer?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
keyb2 = get_produtos('https://www.kabum.com.br/perifericos/teclado-gamer?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
keyb3 = get_produtos('https://www.kabum.com.br/perifericos/teclado-gamer?pagina=3&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
keyb4 = get_produtos('https://www.kabum.com.br/perifericos/teclado-gamer?pagina=4&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
keybs = [keyb1,keyb2,keyb3,keyb4]
keybs = pd.concat(keybs)

monitor1 = get_produtos('https://www.kabum.com.br/computadores/monitores?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
monitor2 = get_produtos('https://www.kabum.com.br/computadores/monitores?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
monitors = [monitor1,monitor2]
monitors = pd.concat(monitors)

smartphone1 = get_produtos('https://www.kabum.com.br/celular-telefone/smartphones?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
smartphone2 = get_produtos('https://www.kabum.com.br/celular-telefone/smartphones?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
smartphone3 = get_produtos('https://www.kabum.com.br/celular-telefone/smartphones?pagina=3&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
smartphone4 = get_produtos('https://www.kabum.com.br/celular-telefone/smartphones?pagina=4&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
smartphone5 = get_produtos('https://www.kabum.com.br/celular-telefone/smartphones?pagina=5&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
smartphones = [smartphone1,smartphone2,smartphone3,smartphone4,smartphone5]
smartphones = pd.concat(smartphones)


audio1 = get_produtos('https://www.kabum.com.br/audio?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
audio2 = get_produtos('https://www.kabum.com.br/audio?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
audio3 = get_produtos('https://www.kabum.com.br/audio?pagina=3&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
audio4 = get_produtos('https://www.kabum.com.br/audio?pagina=4&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
audios = [audio1,audio2,audio3,audio4]
audios = pd.concat(audios)


tv1 = get_produtos('https://www.kabum.com.br/tv?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
tv2 = get_produtos('https://www.kabum.com.br/tv?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
tvs = [tv1,tv2]
tvs = pd.concat(tvs)


smarthome = get_produtos('https://www.kabum.com.br/smart-home?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
suportes = get_produtos('https://www.kabum.com.br/perifericos/suportes?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
frames = [vgas, cpus, rams,ssds,mdboards,pwrs,headsets,mouses,keybs,monitors,smartphones,smarthome,suportes,audios,tvs]
banco = pd.concat(frames)

banco['NOME'] = banco['NOME'].replace({"'":''}, regex=True)
banco['CATEGORIA'] = banco['CATEGORIA'].replace({"'":''}, regex=True)
pysql.INSERT_DATAFRAME(banco,'bd_precos')
banco.to_csv('C:/Users/Victor/Documents/banco.csv',encoding='latin1')