#!/bin/python3

import urllib.request
from bs4 import BeautifulSoup

def get_story(link):
    print("Getting link ", link) 
    for i in range (1,21): #For stories less than 20 pages
        try :
            page = urllib.request.urlopen(link + "?page=%s" % i).read()
            print("Geting pages")
            soup = BeautifulSoup(page,"html.parser")            
            Write_to_File(soup, i)
        except urllib.request.HTTPError:
            print("Done\n")
            break

def Get_URL(URL):
    page = urllib.request.urlopen(URL).read()
    soup = BeautifulSoup(page,"html.parser")
    return soup 

def Get_title(soup):
    return soup.h1.text
    
def Get_text(soup):
    raw_html = soup.find(class_="aa_ht") #hard coded class name
    data = raw_html.find_all('p')
    return data

def Write_to_File(soup, page):
    title = Get_title(soup)
    data = Get_text(soup) 
    with open("%s-page-%s.txt" %(title, page),'w') as foo:
        for line in data:
            out = line.get_text() #eliminate any tags in between
            foo.write(out + '\n')
    print("Written page", page, "\n")



