# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

#top 20 teams
top_20 = [
{'name':'Natus Vincere', 'id':4608},
{'name':'Luminosity', 'id':6290},
{'name': 'fnatic', 'id':4991},
{'name':'Astralis', 'id':6665},
{'name':'NiP', 'id':4411},
{'name':'EnVyUs', 'id':5991},
{'name':'Virtus.pro', 'id':5378},
{'name':'dignitas', 'id':5422},
{'name':'mousesports', 'id':4494},
{'name':'Liquid', 'id':5973},
{'name':'CLG', 'id':5974},
{'name':'GODSENT', 'id':6902},
{'name':'G2', 'id':5995},
{'name':'Tempo Storm', 'id':6118},
{'name':'TyLoo', 'id':4863},
{'name':'Cloud9', 'id':5752},
{'name':'HellRaisers', 'id':5310},
{'name':'FaZe', 'id':6667},
{'name':'Gambit', 'id':6651},
{'name':'E-frag.net', 'id':6226}
]

#map pool
maps=[
{'name':'dust2', 'id':31},
{'name':'mirage', 'id':32},
{'name':'inferno', 'id':33},
{'name':'cache', 'id':29},
{'name':'train', 'id':35},
{'name':'cobblestone', 'id':39},
{'name':'overpass', 'id':40},
]

#Scrapes map data for every team in the top 20 and every map in our map pool
def scrape_map_stats():
    csv = ''
    csvFile = open("map_data.csv",'w')
    csvFile.write("Team, Map, Win %, Pistol Rounds Win %, Round win % after getting first kill, Round win % after receiving first death")
    for i in range(len(top_20)):
        team_id = top_20[i]['id']
        for j in range(len(maps)):
            map_id = maps[j]['id']
            hltvUrl = "http://www.hltv.org/?pageid=192&teamid=%d&mapid=%d" % (team_id, map_id)
            hltvUrl2 = "http://www.hltv.org/?pageid=192&teamid=%d&mapid=%d" % (team_id, map_id)
            print("Getting data from: " + hltvUrl)
            r  = requests.get(hltvUrl)
            data = r.text
            soup = BeautifulSoup(data,"lxml")
            results=soup.find_all("div", {"class": "covGroupBoxContent"},limit=1)
            for k in results:
                result=(str(k.text).splitlines())
            win_in_map = (result[34][11:-2])
            pistol_in_map = (result[52][23:-2])
            if (win_in_map == 'N/'):
                win_in_map = '0'
            if (pistol_in_map == 'N/'):
                pistol_in_map = '0'
                
            s  = requests.get(hltvUrl2)
            data2 = s.text
            soup2 = BeautifulSoup(data2,"lxml")
            results2=soup2.find_all("div", {"class": "covMainBoxContent"},limit=1)
            for k in results2:
                result2=(str(k.text).splitlines())
            first_kill = result2[11][42:-2]
            first_death = result2[18][45:-2]
            if (first_kill == 'N'):
                first_kill = '0'
            if (first_death == 'N'):
                first_death = '0'
            line = '\n' + top_20[i]['name'] + ',' + maps[j]['name'] + ',' + win_in_map + ',' + pistol_in_map + ',' + first_kill + ','+first_death
            csv += line

    csvFile.write(csv)
    csvFile.close

#Converts extracted data into a csv format for csgo_results.csv
def extractDataIntoCondensedList(match):
    line=''
    thisMap=(match[2].replace(' - ', ' ').split(' '))[0]
    firstTeam=(match[2].replace(' - ', ' ').split(' '))[1]
    secondTeam=(match[13].strip())
    firstScore=int((match[7].replace(' - ', ' ').split(' '))[0])
    secondScore=int((match[7].replace(' - ', ' ').split(' '))[1])
    
    if (firstScore+secondScore>=16):
        if (firstScore>secondScore):
            winner = firstTeam
        else:
            winner = secondTeam
        line+=str('\n' + secondTeam + ',' + firstTeam + ',' + winner + ',' + str(secondScore) + ',' + str(firstScore) + ',' + thisMap)
    return line
    
#Only run this if you want new data (Will overwrite the previoius csv file)
def scrape(pages):
    csvContents=''
    for i in range(pages):
        hltvUrl = "http://www.hltv.org/results/"
        if i==0:
            csvFile = open("csgo_results.csv",'w')
            csvFile.write("Team 1,Team 2,Winning Team,Winning Score,Losing Score,Map Played")
        if i>0:
            hltvUrl+=(str((i)*50)+'/')
        print("Getting data from: " + hltvUrl)
        r  = requests.get(hltvUrl)
        data = r.text
        soup = BeautifulSoup(data,"lxml")
        results=soup.find_all("div", {"class": "matchListBox"},limit=50)
        for j in results:
            result=(str(j.text).splitlines())
            csvContents+=extractDataIntoCondensedList(result)
    csvFile.write(csvContents)
    csvFile.close()
