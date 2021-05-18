#!/bin/python3
from multiprocessing import Process
import os
import requests
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
        self.exclude = ["Audio", "Erotic Art", "Non-Erotic Poetry", "Erotic Poetry", "Gay Male", "Transgender & Crossdressers" ]
        self.fill_data()

        

    def fill_data(self):
        try:
            conn = requests.get(self.url,headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
            conn.raise_for_status()
            self.p = soupify(conn.content, "lxml")
            self.name_temp = self.p.find('a', {'class': 'contactheader'})
            self.name = self.name_temp.get_text()
            print('Found author : %s\n' % self.name)
            with  open("%stxt" %(self.name),'w') as foo:
                pass
             # WARNING: hard coded class names
            tofind = 'bb'
            self.stories = self.p.find_all('a', {'class': tofind})
            #self.stories += self.p.find_all('a', {'class': tofind2})
            self.stories = [x['href'][28:] for x in self.stories]
            print("Found %s stories\n" % len(self.stories))
        except requests.HTTPError as e:
            print('HTTPError: {}'.format(e.code))
        except requests.URLError as e:
            print('URLError: {}'.format(e.reason))

    def get_page(self,url,page,title):

        conn = requests.get(("%s?page=%s" %(url,page)),headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
        conn.raise_for_status()
        con = soupify(conn.content, "lxml")
        raw_html = con.find(class_="aa_ht") #hard coded class name
        data = raw_html.find_all('p')
        with open("%s-page-%s.txt" %(title, page),'w') as foo:
            for line in data:
                out = line.get_text() #eliminate any tags in between
                foo.write(out + '\n')
        print("Written page %s\n" %page)
         

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
            processes = []
            for page in range (1, st.num_pages + 1): #Assuming a maximum of 20 pages
                try:
                    process = Process(target=self.get_page, args=(st.url,page,st.title))      
                    processes.append(process)
                    process.start()
                except  requests.HTTPError as e:
                    break
            for proc in processes:
                proc.join()
            os.chdir(authordir)
            
        os.chdir(wd)     


def get_everything(_id):
    author = Author(_id)
    print("Getting stories\n")
    author.download_stories()
    print("Done!")


