#!/bin/python3

import urllib.request
import urllib.request
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
            conn = urllib.request.urlopen(self.url)
        except urllib.error.HTTPError as e:
            print('HTTPError: {}'.format(e.code))
        except urllib.error.URLError as e:
            print('URLError: {}'.format(e.reason))
        else:
            print('story found')
            self.page = soupify(conn, "html.parser")

    def fill_data(self):
        if not self.page:
            self.first_page()
        self.title = self.page.find('title').text 
        # remove " - Literotica.com"
        self.title, self.category = self.title[:-17].rsplit(' - ', 1)

        self.description = self.page.find('meta', {'name': 'description'})
        self.description = self.description['content']

    



