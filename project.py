# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:06:25 2016

@author: David Ruan
"""

from bs4 import BeautifulSoup
import requests

def extractDataIntoCondesedList(match):
    #match is a list
    thisMatch=match[2]
    thisMap=(thisMatch.replace(' - ', ' ').split(' '))[0]
    firstTeam=(thisMatch.replace(' - ', ' ').split(' '))[1]
    print(thisMap)
    print(firstTeam)
    
    #print("Played on "+match[2])
    
hltvUrl = "http://www.hltv.org/results/"
gosuUrl = ""
fnaticStatsUrl = "http://www.hltv.org/?pageid=179&teamid=4991"
r  = requests.get(hltvUrl)
data = r.text
soup = BeautifulSoup(data)
#print(soup.prettify())
print()
results=soup.find_all("div", {"class": "matchListBox"},limit=50)
for i in results:
    if "mousesports" in i.text:
        listo=(str(i.text).splitlines())
        print(listo)
        
        extractDataIntoCondesedList(listo)
        #gather data
        
        
        



"""
for i in res:
    print(i)


    #find team ranking on hltv
def getTeamRank(team):
    r  = requests.get("http://www.hltv.org/ranking/teams/")
    data = r.text
    soup = BeautifulSoup(data)
    div=soup.div
    logo = div.attrs['ranking-logo']
    
getTeamRank('Natus Vincere')

"""