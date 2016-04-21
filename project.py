# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:26:49 2016

@author: rishijavia
"""


from bs4 import BeautifulSoup
import requests
import urllib
url = "hltv.org/?pageid=179&teamid=6290&statsfilter=9"

r = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data, "lxml")

#print(soup.prettify())

def match_class(target):                                                        
    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match    

soup = BeautifulSoup(html)  

matches = soup.find_all(match_class(["covSmallHeadline"]))
print(matches)
for m in matches:
    print (m)

#covSmallHeadline