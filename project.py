"""
Created on Wed Apr 20 12:06:25 2016

@author: David Ruan
"""

from bs4 import BeautifulSoup
import requests

hltvUrl = "www.hltv.org/results/"
r  = requests.get("http://" +hltvUrl)
data = r.text
soup = BeautifulSoup(data)
results=soup.find_all("div", {"class": "matchListBox"},limit=50)
#print(soup.prettify())

print('******************')
res=results[0]
print(res.contents)

print(len(res))

for i in res:
    print(i)

"""
    #find team ranking on hltv
def getTeamRank(team):
    r  = requests.get("http://www.hltv.org/ranking/teams/")
    data = r.text
    soup = BeautifulSoup(data)
    div=soup.div
    logo = div.attrs['ranking-logo']
    
getTeamRank('Natus Vincere')

"""