# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 15:49:02 2016

@author: rishijavia
"""
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

maps=[
{'name':'dust2', 'id':31},
{'name':'mirage', 'id':32},
{'name':'inferno', 'id':33},
{'name':'cache', 'id':29},
{'name':'train', 'id':35},
{'name':'cobblestone', 'id':39},
{'name':'overpass', 'id':40},
]


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