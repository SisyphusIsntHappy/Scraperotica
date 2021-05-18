#!/bin/python3

import requests
from bs4 import BeautifulSoup as soupify

class Story(object):
    def __init__(self, _id):
        self.url = "http://www.literotica.com/s%s" %(_id)
        self.page = ""
        self.category = ""
        self.description = ""
        self.title = ""
        self.fill_data()

    def first_page(self):
        try:
            conn = requests.get(self.url,headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
            conn.raise_for_status()
        except requests.HTTPError as e:
            print('HTTPError: {}'.format(e.code))
        except requests.URLError as e:
            print('URLError: {}'.format(e.reason))
        else:
            print('story found')
            self.page = soupify(conn.content, "lxml")

    def fill_data(self):
        if not self.page:
            self.first_page()
        self.title = self.page.find('title').text 
        # remove " - Literotica.com"
        self.title, self.category = self.title[:-17].rsplit(' - ', 1)

        self.description = self.page.find('meta', {'name': 'description'})
        self.description = self.description['content']
        if not self.page.find_all(class_="l_bJ"):
            self.num_pages = 1
        else:
            self.num_pages = int(self.page.find_all(class_="l_bJ")[-1].text)

    



