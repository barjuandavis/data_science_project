# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:06:25 2016

@author: David Ruan
"""
from bs4 import BeautifulSoup
import requests, csv

#Harcoded Data
teams=[	  {'Team Name':'Natus Vincere','Team Rank':1,'Team id':4608,'KD':1.07},
		  {'Team Name':'Luminosity','Team Rank':2,'Team id':6290,'KD':1.14},
		  {'Team Name':'Fnatic','Team Rank':3,'Team id':4991,'KD':1.12},
		  {'Team Name':'Astralis','Team Rank':4,'Team id':6665,'KD':1.11},
		  {'Team Name':'NiP','Team Rank':5,'Team id':4411,'KD':1.16},
		  {'Team Name':'EnVyUs','Team Rank':6,'Team id':5991,'KD':1.07},
		  {'Team Name':'Virtus.pro','Team Rank':7,'Team id':5378,'KD':1.06},
		  {'Team Name':'dignitas','Team Rank':8,'Team id':5422,'KD':1.05},
		  {'Team Name':'mousesports','Team Rank':9,'Team id':4494,'KD':1.04},
		  {'Team Name':'Liquid','Team Rank':10,'Team id':5973,'KD':1.08},
		  {'Team Name':'CLG','Team Rank':11,'Team id':5974,'KD':1.05},
		  {'Team Name':'GODSENT','Team Rank':12,'Team id':6902,'KD':1.03},
		  {'Team Name':'G2','Team Rank':13,'Team id':5995,'KD':1.01},
		  {'Team Name':'Tempo Storm','Team Rank':14,'Team id':6118,'KD':1.12},
		  {'Team Name':'TyLoo','Team Rank':15,'Team id':4863,'KD':1.04},
		  {'Team Name':'Cloud9','Team Rank':16,'Team id':5752,'KD':1.06},
		  {'Team Name':'HellRaisers','Team Rank':17,'Team id':5310,'KD':1.03},
		  {'Team Name':'FaZe','Team Rank':18,'Team id':6667,'KD':0.99},
		  {'Team Name':'Gambit','Team Rank':19,'Team id':6651,'KD':1.00},
		  {'Team Name':'E-frag.net','Team Rank':20,'Team id':6226,'KD':1.09}]
    
csgoData=[]

def isTop20(input):
    for i in range(len(teams)):
        if (input == teams[i]['Team Name']):
            return True
    return False

def extractDataIntoCondensedList(match):
    line=''
    #match is a list
    thisMap=(match[2].replace(' - ', ' ').split(' '))[0]
    firstTeam=(match[2].replace(' - ', ' ').split(' '))[1]
    secondTeam=(match[13].strip())
    firstScore=int((match[7].replace(' - ', ' ').split(' '))[0])
    secondScore=int((match[7].replace(' - ', ' ').split(' '))[1])
    #Get team1HasHigherRating
    #Get team1winRateonMap
    #do not include anything other than best of 1's
    if (firstScore+secondScore>=16):
        if (firstScore>secondScore):
            #convert into csv format
            line+=str('\n' + firstTeam + ',' + secondTeam + ',' + str(firstScore) + ',' + str(secondScore) + ',' + thisMap)
        else:
            #convert to csv format
            line+=str('\n' + secondTeam + ',' + firstTeam + ',' + str(secondScore) + ',' + str(firstScore) + ',' + thisMap)
    return line
    
#Only run this if you want new data (Will overwrite the previoius csv file)
def scrape(pages):
    print("Scraping. Please be patient")
    csvContents=''
    for i in range(pages):
        hltvUrl = "http://www.hltv.org/results/"
        if i==0:
            csvFile = open("csgo_results.csv",'w')
            csvFile.write("Winning Team, Losing Team, Winning Score, Losing Score, Map Played, Team1HasHigherRating, Team1HasHigherMapWinRate")
        if i>0:
            hltvUrl+=(str((i)*50)+'/')
        print(hltvUrl)
        r  = requests.get(hltvUrl)
        data = r.text
        soup = BeautifulSoup(data,"lxml")
        results=soup.find_all("div", {"class": "matchListBox"},limit=50)
        for j in results:
            result=(str(j.text).splitlines())
            csvContents+=extractDataIntoCondensedList(result)
    csvFile.write(csvContents)

#view csv contents
def readCsv(fileName):
    with open(fileName, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        rows = [r for r in reader]
    return rows
    
def returnMapStats(t, m):
    import csv
    with open('map_data.csv', 'r') as f:
         reader = csv.reader(f, delimiter=',')
         next(reader)
         rows = [r for r in reader]
    data = []
    for i in range(len(rows)):
        if ((t == rows[i][0]) and (m == rows[i][1])):
            win_percent = rows[i][2]
            data.append(win_percent)
            
            pistol_percent = rows[i][3]
            data.append(pistol_percent)
            
            first_kill = rows[i][4]
            data.append(first_kill)
            
            first_death = rows[i][5]
            data.append(first_death)
            return data

#def deepScrape(matchPage):

"""
Team1name,Team2name,MapName,Team1wonthegame,Team1hasHigherRating,Team1hasHigherKD

Hardcode rankings"""

inputs = [
        ({'Map':'','Team1hashigherrating':'','Team1hasHigherAverageKD':'','Team1HasHigherMapWinRateOnMap':'','Team1HasHigherPistolRoundWinRateOnMap':''},   False),
        ({'Map':'','Team1hashigherrating':'','Team1hasHigherAverageKD':'','Team1WinHasHigherWinRate':''},   False)]

#for i in readCsv('csgo_results.csv'):
#    print(i)
#    
#print("Intern", classify(tree, { "level" : "Intern" } ))