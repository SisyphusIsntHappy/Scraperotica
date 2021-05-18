#!/bin/python3
from multiprocessing import Process
import urllib.request
from bs4 import BeautifulSoup
import requests
def get_story(link):
    print("Getting link ", link)
    page = requests.get(link,headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    soup = BeautifulSoup(page.content,"lxml")            
    print("Geting pages")
    if not soup.find_all(class_="l_bJ"):
        num_pages = 1
    else:
        num_pages = int(soup.find_all(class_="l_bJ")[-1].text)
    processes = []
    for page in range(1, num_pages + 1):
        
        process = Process(target=Write_to_File, args=(link, page))
        processes.append(process)
        process.start()
    for proc in processes:
        proc.join()


def Write_to_File(link, page):
    html = requests.get("%s?page=%s" %(link,page),headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    soup = BeautifulSoup(html.content,"lxml")
    raw_html = soup.find(class_="aa_ht") #hard coded class name
    title = soup.h1.text
    data = raw_html.find_all('p')
    with open("%s-page-%s.txt" %(title, page),'w') as foo:
        for line in data:
            out = line.get_text() #eliminate any tags in between
            foo.write(out + '\n')
    print("Written page", page, "\n")



