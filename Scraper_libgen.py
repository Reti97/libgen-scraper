import requests
from bs4 import BeautifulSoup as bs
import re
from re import match
import urllib
import urllib.request
import os
import pdfminer.high_level as pdfminer
from threading import Thread
from itertools import cycle
import csv
import Prawler
import random
import time
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


proxy_type = ["http", "socks4", "socks5"]
proxy_country = ['AF', 'AL', 'AM', 'AR', 'AT', 'AU', 'BA', 'BD', 'BG', 'BO', 'BR', 'BY', 'CA', 'CL', 'CM', 'CN', 'CO', 'CZ', 'DE', 'EC', 'EG', 'ES', 'FR', 'GB', 'GE', 'GN', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IN', 'IQ', 'IR', 'IT', 'JP', 'KE', 'KG', 'KH', 'KR', 'KZ', 'LB', 'LT', 'LV', 'LY', 'MD', 'MM', 'MN', 'MU', 'MW', 'MX', 'MY', 'NG', 'NL', 'NO', 'NP', 'PE', 'PH', 'PK', 'PL', 'PS', 'PY', 'RO', 'RS', 'RU', 'SC', 'SE', 'SG', 'SK', 'SY', 'TH', 'TR', 'TW', 'TZ', 'UA', 'UG', 'US', 'VE', 'VN', 'ZA']
proxy_http = []
#Format:
# { “http”: “http://10.10.10.10:8000” }
proxy_socks4 = []
#Format:
# { 'http': "socks4://myproxy:9191" }
proxy_socks5 = []
#Format:
# { 'http': "socks5://myproxy:9191" }


for country in proxy_country:
    proxy_http.append(Prawler.get_proxy_list(10, 'http', "all", country))
    proxy_socks4.append(Prawler.get_proxy_list(10, "socks4", "all", country))
    proxy_socks5.append(Prawler.get_proxy_list(10, "socks5", "all", country))


clean_proxy_http = [item for sublist in proxy_http for item in sublist]
clean_proxy_socks4 = [item for sublist in proxy_socks4 for item in sublist]
clean_proxy_socks5 = [item for sublist in proxy_socks5 for item in sublist]

proxies = {'http' : [], 'socks4': [], 'socks5' : []}

for i in clean_proxy_http:
    proxies["http"].append('http://' + i)

for i in clean_proxy_socks4:
    proxies["socks4"].append('socks4://' + i)

for i in clean_proxy_socks5:
    proxies["socks5"].append('socks5://' + i)

def get_random_proxy():
    rand_key = random.choice(list(proxies.keys()))
    rand_value =  random.choice(proxies[rand_key])
    proxy_format = { }
    proxy_format[rand_key] = rand_value
    return proxy_format

def get_random_header():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   

    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

    # Get Random User Agent String.
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {'User-Agent':str(user_agent)}
    return headers

suchbegriff = str(input("Suchbegriff:"))
url_sb = suchbegriff.replace(" ", "+")

#start book scraper
debug = False
page_index = 1
all_book_links = []
while True:
    try:
        URL = 'https://libgen.is/search.php?req=' + url_sb + f'&open=0&res=100&view=detailed&phrase=1&column=def&page={page_index}'
        page = session.get(URL, headers=get_random_header(), proxies=get_random_proxy(), )
        soup = bs(page.content, 'html.parser')
        time.sleep(random.randrange(5))

        #getting the links to every book on a page
        links = []
        for i in soup.find_all('td', {'colspan' : '2'}):
            link = i.find('a', href=True)
            href_link = (link['href'])
            str_link = str(href_link)
            links.append(str_link.replace('..', ''))
            if link is None:
                continue

        #slug to books
        new_book_links = []
        regex = re.compile('.*book\/index\.php\?.*')
        links_books = [n for n in links if regex.match(n)]

        #building the correct links directly to the book 
        for e in links_books:
            link_to_book = 'https://libgen.is' + str(e)
            new_book_links.append(link_to_book)
            time.sleep(random.randrange(3))

        if len(new_book_links) > 0:
            all_book_links.extend(new_book_links)
            page_index += 1
            if debug:
                break
        else:
            break

    except:
        continue

download_links = []
#open book links
for link in all_book_links:
    try:
        prepared_link = link.replace("https://libgen.is/book/index.php?md5=", "")
        URL = "http://library.lol/main/" + prepared_link
        page = session.get(URL, headers=get_random_header(), proxies=get_random_proxy(),)
        soup = bs(page.content, 'html.parser')
        time.sleep(random.randrange(7))
        for a in soup.find_all('div', {'id' : 'download'}):
            for i in a.find_all('h2'):
                for h in i.find_all('a', href=True):
                    download_link = (h.get('href'))
                    download_str_link = str(download_link)
                    if download_str_link.split(".")[-1] == "pdf": #Without this it also finds sum weird djvu files
                        download_links.append(download_str_link)
    except:
        continue

#Let's try to download first link for starters
book_index = 1

#Do sum stuff asynchronously cause me tiref of waiting
def convert_book_to_text(pdfpath, txtpath):
    pdf_text = pdfminer.extract_text(pdfpath)
    text_file = open(txtpath, "w", encoding='utf8')
    text_file.writelines(pdf_text)
    text_file.close()
    print(f"Assimilated {txtpath.split('/')[-1]}")

for url in download_links:
    try:
        print(f"Downloading file nr. {book_index}")

        data = session.get(url, stream=True, headers=get_random_header(), proxies=get_random_proxy())
        time.sleep(random.randrange(5))
        datafolder = "/".join([os.getcwd(), suchbegriff.replace(" ", "_")])
        if not os.path.exists(datafolder):
            os.makedirs(datafolder)
        filename = f"book_{book_index}.pdf"
        textfilename = f"book_{book_index}.txt"
        full_path = "/".join([datafolder, filename])
        outputFile = open(full_path, "wb")
        outputFile.write(data.content)
        outputFile.close()
        print("Download complete, starting to parse in background...")
        
        full_text_path = "/".join([datafolder, textfilename])
        parser_thread = Thread(target=convert_book_to_text, args=(full_path, full_text_path))
        parser_thread.start()   
        book_index += 1
    except:
        continue