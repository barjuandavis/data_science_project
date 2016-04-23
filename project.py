"""
Created on Wed Apr 20 12:06:25 2016

@author: David Ruan
"""

from bs4 import BeautifulSoup
import requests

hltvUrl = "www.hltv.org/?pageid=192&teamid=4991&mapid=31"
r  = requests.get("http://" +hltvUrl)
data = r.text
soup = BeautifulSoup(data, "lxml")
#print(soup.prettify())

print('******************')
    
mydivs = soup.findAll("div", { "class" : "covSmallHeadline"})


for i in range(len(mydivs)):
    if "\%" in i:
        print(i)