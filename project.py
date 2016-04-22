# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:06:25 2016

@author: David Ruan
"""

from bs4 import BeautifulSoup
import requests

def extractDataIntoCondesedList(match):
    #match is a list
    thisMap=(match[2].replace(' - ', ' ').split(' '))[0]
    firstTeam=(match[2].replace(' - ', ' ').split(' '))[1]
    secondTeam=(match[13].strip())
    firstScore=int((match[7].replace(' - ', ' ').split(' '))[0])
    secondScore=int((match[7].replace(' - ', ' ').split(' '))[1])
    #do not include anything other than best of 1's
    if (firstScore+secondScore>=16):
        print()
        print(match)
        print(thisMap)
        print(firstTeam)
        print(secondTeam)
        print(firstScore)
        print(secondScore)
        if (firstScore>secondScore):
            print(firstTeam+' beat ' + secondTeam + ' ' + str(firstScore) + '-' + str(secondScore) +' on '+thisMap)
        else:
            print(secondTeam+' beat ' + firstTeam + ' ' + str(secondScore) + '-' + str(firstScore) +' on '+thisMap)

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
    result=(str(i.text).splitlines())
    #gather data
    extractDataIntoCondesedList(result)
    
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