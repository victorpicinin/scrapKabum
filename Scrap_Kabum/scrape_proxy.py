import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_proxy_list():
    proxylist = []
    resp = requests.get('https://free-proxy-list.net/') 
    df = pd.read_html(resp.text)[0]
    for Index,row in df.iterrows():
        proxy = row['IP Address'] + ':' + str(row['Port'])
        proxylist.append(proxy)
    return proxylist
