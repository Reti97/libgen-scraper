import requests
from bs4 import BeautifulSoup as bs
import re
from re import match
import urllib
import urllib.request
import PyPDF2

suchbegriff = str(input("Suchbegriff:"))
url_sb = suchbegriff.replace(" ", "+")

URL = 'https://libgen.is/search.php?req=' + url_sb + '&open=0&res=25&view=detailed&phrase=1&column=def'
page = requests.get(URL)

soup = bs(page.content, 'html.parser')
test = soup.find("div", {"id": "paginator_example_top"})
print(test)


pages = []
#getting links to all the pages
for z in soup.find("div", {"id": "paginator_example_top"}):
    pg = z.find('a', href=True)
    href_pg = (pg['href'])
    str_pg = str(href_pg)
    pages.append(str_pg)
    if pg is None:
        continue

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
regex = re.compile('.*book\/index\.php\?.*')
links_books = [n for n in links if regex.match(n)]

#building the correct links directly to the book 
book_links = []
for e in links_books:
    link_to_book = 'https://libgen.is' + str(e)
    book_links.append(link_to_book)

