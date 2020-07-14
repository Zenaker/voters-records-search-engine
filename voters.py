import requests
import sys
import re

from threading import Thread

BASE_URL = "https://sortedbybirthdate.com/small_pages/"

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def listPages(birthdate=None, year=None):
    # birthdate format '20010912' which is equals to 2001, 12 September
    req = requests.get(BASE_URL + birthdate[:4] + "/").text
    count = req.count(birthdate)
    pages = []

    for index in range(count):
        endpoint = birthdate + req.split(birthdate)[index+1].split("</a>")[0]
        page = BASE_URL + birthdate[:4] + "/" + endpoint
        pages.append(page)

    return pages


def find(link, results, keyword):
    req = requests.get(link).text.lower()

    if keyword + " " in req:
        count = req.count(keyword + " ")
        for index in range(count):
            text_one = req.split(keyword + " ")[0].split("-->")[-1]
            text_two = req.split(keyword + " ")[index+1].split("<br>")[0]
            result = text_one + keyword + " " + text_two

            results.append(cleanhtml(result))

def search(links_list,  keyword):
    results = []
    threads = []
    for link in links_list:
        t = Thread(target=find, args=(link, results, keyword,),)
        threads.append(t)
    
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return results
