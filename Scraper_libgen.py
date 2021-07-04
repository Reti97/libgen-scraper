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

proxy_type = ["http", "socks4", "socks5"]
proxy_country = ['AF', 'AL', 'AM', 'AR', 'AT', 'AU', 'BA', 'BD', 'BG', 'BO', 'BR', 'BY', 'CA', 'CL', 'CM', 'CN', 'CO', 'CZ', 'DE', 'EC', 'EG', 'ES', 'FR', 'GB', 'GE', 'GN', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IN', 'IQ', 'IR', 'IT', 'JP', 'KE', 'KG', 'KH', 'KR', 'KZ', 'LB', 'LT', 'LV', 'LY', 'MD', 'MM', 'MN', 'MU', 'MW', 'MX', 'MY', 'NG', 'NL', 'NO', 'NP', 'PE', 'PH', 'PK', 'PL', 'PS', 'PY', 'RO', 'RS', 'RU', 'SC', 'SE', 'SG', 'SK', 'SY', 'TH', 'TR', 'TW', 'TZ', 'UA', 'UG', 'US', 'VE', 'VN', 'ZA']

for prox in proxy_type:
    for country in proxy_country:
        proxy_list = Prawler.get_proxy_list(500, prox, "all", country)

#get Proxies
with open('proxies.csv') as f:
    list_proxy = list(csv.reader(f))


"""


proxy_cycle = cycle(list_proxy)

# Prime the pump
proxy = next(proxy_cycle)

for i in range(1, 10):          #würd (1, len(list_proxy)) ned meh Sinn mache?
    proxy = next(proxy_cycle)
    proxies = {
      "http": proxy,
      "https":proxy
    }

    #start book scraper
    suchbegriff = str(input("Suchbegriff:"))
    url_sb = suchbegriff.replace(" ", "+")
    debug = False
    page_index = 1
    all_book_links = []
    while True:
        URL = 'https://libgen.is/search.php?req=' + url_sb + f'&open=0&res=100&view=detailed&phrase=1&column=def&page={page_index}'
        page = requests.get(URL)
        soup = bs(page.content, 'html.parser')

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
        if len(new_book_links) > 0:
            all_book_links.extend(new_book_links)
            page_index += 1
            if debug:
                break
        else:
            break

    download_links = []
    #open book links
    for link in all_book_links:
        prepared_link = link.replace("https://libgen.is/book/index.php?md5=", "")
        URL = "http://library.lol/main/" + prepared_link
        page = requests.get(URL)
        soup = bs(page.content, 'html.parser')
        for a in soup.find_all('div', {'id' : 'download'}):
            for i in a.find_all('h2'):
                for h in i.find_all('a', href=True):
                    download_link = (h.get('href'))
                    download_str_link = str(download_link)
                    if download_str_link.split(".")[-1] == "pdf": #Without this it also finds sum weird djvu files
                        download_links.append(download_str_link)

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
        print(f"Downloading file nr. {book_index}")
        data = requests.get(url, stream=True)
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
"""