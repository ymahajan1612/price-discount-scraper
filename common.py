from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
def fetchProductDetails(url, require_name = False):
    headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    response = requests.get(url, headers=headers)
    html = BeautifulSoup(response.content, "html.parser")
    html_pretty = BeautifulSoup(html.prettify(), "html.parser")
    title = html_pretty.find(id="productTitle").get_text().strip()
    available = html_pretty.find("div", attrs={'id': 'availability'})
    in_stock = False if "currently unavailable" in available.get_text().strip().lower() else True
    print(in_stock)
    price = html_pretty.find("span",{"class":"a-price"}).find("span").text.strip()
    if require_name:
        return title, price
    else:
        return price
