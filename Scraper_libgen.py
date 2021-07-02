import requests
from bs4 import BeautifulSoup as bs
import re
from re import match
import urllib
import urllib.request
import PyPDF2

suchbegriff = str(input("Suchbegriff:"))
url_sb = suchbegriff.replace(" ", "+")

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
                download_link = (link['href'])
                print(link['href'])
                download_str_link = str(download_link)
                download_links.append(download_str_link)

print(download_links)