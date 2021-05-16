#!/bin/python3

import os
import urllib.request
from bs4 import BeautifulSoup as soupify
from story import Story


class Author(object):
    def __init__(self, _id):
        try:
            int(_id)
        except ValueError:
            raise ValueError("invalid author uid '%s'" %(_id))
        self.url = "http://literotica.com/stories/memberpage.php?uid=%s&page=submissions" %(_id)
        self.stories = []
        self.name = ""
        self.exclude = ["Audio"]
        self.fill_data()

        

    def fill_data(self):
        try:
            conn = urllib.request.urlopen(self.url)
            self.p = soupify(conn, "html.parser")
            self.name_temp = self.p.find('a', {'class': 'contactheader'})
            self.name = self.name_temp.get_text()
            print('Found author : %s\n' % self.name)
             # WARNING: hard coded class names
            tofind = 'bb'
            self.stories = self.p.find_all('a', {'class': tofind})
            #self.stories += self.p.find_all('a', {'class': tofind2})
            self.stories = [x['href'][28:] for x in self.stories]
            print("Found %s stories\n" % len(self.stories))
        except urllib.error.HTTPError as e:
            print('HTTPError: {}'.format(e.code))
        except urllib.error.URLError as e:
            print('URLError: {}'.format(e.reason))

    def download_stories(self):
        wd = os.getcwd()
        print("Creating author directory %s\n" % self.name)
        try:
            os.mkdir(self.name)
        except FileExistsError:
                print("Directory exists")
        os.chdir(self.name)
        authordir = os.getcwd()
        for story in range (0, len(self.stories)):
            st = Story(self.stories[story])
            if st.category in self.exclude :
                print("Skipping audio story : %s\n" %st.title)
                continue
            print("Creating category directory %s\n" %st.category)
            try:
                os.makedirs(st.category)
            except FileExistsError:
                print("Directory exists")
            os.chdir(st.category)
            print("Getting story %s\n" % st.title)
            print("Creating story directory %s\n" %st.title)
            os.mkdir(st.title)
            os.chdir(st.title)
            for page in range (1, 21): #Assuming a maximum of 20 pages
                try:
                    con =  urllib.request.urlopen(("%s?page=%s" %(st.url,page)))
                    con = soupify(con, "html.parser")
                    raw_html = con.find(class_="aa_ht") #hard coded class name
                    data = raw_html.find_all('p')
                    with open("%s-page-%s.txt" %(st.title, page),'w') as foo:
                        for line in data:
                            out = line.get_text() #eliminate any tags in between
                            foo.write(out + '\n')
                    print("Written page %s\n" %page)
                except  urllib.error.HTTPError as e:
                    break
            os.chdir(authordir)
            
        os.chdir(wd)     


def get_everything(_id):
    author = Author(_id)
    print("Getting stories\n")
    author.download_stories()
    print("Done!")


