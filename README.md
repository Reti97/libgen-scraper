# libgen-scraper

## About The Project
[Plexatic](https://github.com/PLEXATIC) and myself both Study AI & ML Plexatic once mentioned, that he had the idea of training an AI with data from books and so we came up with the idea of building such a scraper.

## Getting Started
You can just clone this project or copy the file, install all the dependencies / libraries with "pip install library_name".

## Prerequisites
The following libraries are being used:

- requests
- Beautifulsoup 4
- re
- urllib
- os
- pdfminer
- threading
- itertools
- csv
- Prawler
- random
- time
- random_user_agent.user_agent
- random_user_agent.params

## Usage

You can just get this File, install everything and try to run it, after some time you will be able to add some input (your search term) and then the script will start downloading all books matching the search term from libgen.is.<br>
As the source code of libgen most probably will be changed from time to time, we can't guarantee, that the script will work, but it did as of today (October, 7th, 2021).<br>
If you wanna speed up the downloads, you can minimize the numbers of proxies fetched. You can also change or delete the random sleep time. Both risks the number of getting blocked, but feel free to try it out.<br>
The downloaded files will be downloaded in a folder named the same as your search query within your user folder.
