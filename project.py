"""
Created on Wed Apr 20 12:06:25 2016

@author: David Ruan
"""

from bs4 import BeautifulSoup
import requests

hltvUrl = "www.hltv.org/?pageid=179&teamid=4991"
r  = requests.get("http://" +hltvUrl)
data = r.text
soup = BeautifulSoup(data, "lxml")
results=soup.find_all("div", {"class": "matchListBox"},limit=50)
print(soup.prettify())

print('******************')
res=results[0]
print(res.contents)

print(len(res))

for i in res:
    print(i)
    
#mydivs = soup.findAll("div", { "class" : "matchScoreCell" })
#
#print(mydivs)