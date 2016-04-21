# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:26:49 2016

@author: rishijavia
"""


from bs4 import BeautifulSoup
import requests
url = "hltv.org"

r = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data)

print(soup.prettify())