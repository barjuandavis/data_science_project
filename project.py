# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, csv

#Hardcoded Data
teams=[	  {'Team Name':'Natus Vincere','Team Rank':1,'Team id':4608,'KD':1.07, 'Rating':1.03},
		  {'Team Name':'Luminosity','Team Rank':2,'Team id':6290,'KD':1.14, 'Rating':0},
		  {'Team Name':'Fnatic','Team Rank':3,'Team id':4991,'KD':1.12, 'Rating':1.06},
		  {'Team Name':'Astralis','Team Rank':4,'Team id':6665,'KD':1.11, 'Rating':0},
		  {'Team Name':'NiP','Team Rank':5,'Team id':4411,'KD':1.16, 'Rating':1.09},
		  {'Team Name':'EnVyUs','Team Rank':6,'Team id':5991,'KD':1.07, 'Rating':1.04},
		  {'Team Name':'Virtus.pro','Team Rank':7,'Team id':5378,'KD':1.06, 'Rating':1.03},
		  {'Team Name':'dignitas','Team Rank':8,'Team id':5422,'KD':1.05, 'Rating':1.02},
		  {'Team Name':'mousesports','Team Rank':9,'Team id':4494,'KD':1.04, 'Rating':1.01},
		  {'Team Name':'Liquid','Team Rank':10,'Team id':5973,'KD':1.08, 'Rating':1.04},
		  {'Team Name':'CLG','Team Rank':11,'Team id':5974,'KD':1.05, 'Rating':1.02},
		  {'Team Name':'GODSENT','Team Rank':12,'Team id':6902,'KD':1.03, 'Rating':0},
		  {'Team Name':'G2','Team Rank':13,'Team id':5995,'KD':1.01, 'Rating':0},
		  {'Team Name':'Tempo Storm','Team Rank':14,'Team id':6118,'KD':1.12, 'Rating':0},
		  {'Team Name':'TyLoo','Team Rank':15,'Team id':4863,'KD':1.04, 'Rating':0},
		  {'Team Name':'Cloud9','Team Rank':16,'Team id':5752,'KD':1.06, 'Rating':1.02},
		  {'Team Name':'HellRaisers','Team Rank':17,'Team id':5310,'KD':1.03, 'Rating':1.01},
		  {'Team Name':'FaZe','Team Rank':18,'Team id':6667,'KD':0.99, 'Rating':0},
		  {'Team Name':'Gambit','Team Rank':19,'Team id':6651,'KD':1.00, 'Rating':0},
		  {'Team Name':'E-frag.net','Team Rank':20,'Team id':6226,'KD':1.09, 'Rating':0}]
    
csgoData=[]

def isTop20(input):
    for i in range(len(teams)):
        if (input == teams[i]['Team Name']):
            return True
    return False

def isMap(input):
    maps = ["dust2","mirage","inferno","cache","train","cobblestone","overpass"]
    if input in maps:
        return True
    return False

def get_rating(input):
    for i in range(len(teams)):
        if(input == teams[i]['Team Name']):
            return teams[i]['Rating']
    return 0
    
def get_kd(input):
    for i in range(len(teams)):
        if(input == teams[i]['Team Name']):
            return teams[i]['KD']
    return 0

def extractDataIntoCondensedList(match):
    line=''
    #match is a list
    thisMap=(match[2].replace(' - ', ' ').split(' '))[0]
    firstTeam=(match[2].replace(' - ', ' ').split(' '))[1]
    secondTeam=(match[13].strip())
    firstScore=int((match[7].replace(' - ', ' ').split(' '))[0])
    secondScore=int((match[7].replace(' - ', ' ').split(' '))[1])
    team1Won=True
    #do not include anything other than best of 1's
    if (firstScore+secondScore>=16):
        if (secondScore>firstScore):
            team1Won=False
        line+=('\n' + firstTeam + ',' + secondTeam + ',' + str(firstScore) + ',' + str(secondScore) + ',' + thisMap + ',' + str(team1Won))
        
    return line
    
#Only run this if you want new data (Will overwrite the previoius csv file)
def scrape(pages):
    print("Scraping. Please be patient")
    csvContents=''
    for i in range(pages):
        hltvUrl = "http://www.hltv.org/results/"
        if i==0:
            csvFile = open("csgo_results.csv",'w')
            csvFile.write("Winning Team, Losing Team, Winning Score, Losing Score, Map Played, Team1Won")
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
    csvFile.close()
    print('Filtering CSV')
    filterCsv()
    
#view csv contents
def readCsv(fileName):
    with open(fileName, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        rows = [r for r in reader]
    return rows
    
def returnMapStats(t, m):
    rows=readCsv('map_data.csv')
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
            
def filterCsv():    
    """
    What new CSV should look like:
    Team1Name, Team2Name, MapName, TeamWhoWonTheGame(basically team1 based on David's data),
    Team1Rating, Team2Rating, Team1KD, Team2KD, Team1MapWin%, Team2MapWin%,
    Team1PistolRound%, Team2PistolRound%, Team1first_kill, Team2first_kill, 
    Team1first_death, Team2first_death
    """
    og_data = readCsv("csgo_results.csv")
    csv=''
    csvFile = open("filtered_top20.csv",'w')
    csvFile.write("Team 1,Team 2,Map,Team 1 Won,Team 1 Rating,Team 2 Rating,Team 1 KD,Team 2 KD,Team 1 Map Win %,Team 2 Map Win %,Team 1 Pistol Round Win %,Team 2 Pistol Round Win %,Team 1 first kill win %,Team 2 first kill win %,Team 1 first death win %,Team 2 first death win %")
    for data in og_data:
        if (isTop20(data[0]) and isTop20(data[1]) and isMap(data[4])):
            team1name = data[0]
            team2name = data[1]
            #update this if we change format of our og data
            
            map_played = data[4]
            team1rating = str(get_rating(team1name))
            team2rating = str(get_rating(team2name))
            team1kd = str(get_kd(team1name))
            team2kd = str(get_kd(team2name))
            team1Won = str(data[5])
            
            map_data1 = returnMapStats(team1name, map_played)
            map_data2 = returnMapStats(team2name, map_played)
            team1mapwin = map_data1[0]
            team2mapwin = map_data2[0]
            team1pistol = map_data1[1]
            team2pistol = map_data2[1]
            team1firstkill = map_data1[2]
            team2firstkill = map_data2[2]
            team1firstdeath = map_data1[3]
            team2firstdeath = map_data2[3]
            line = '\n' + team1name + ',' + team2name + ',' + map_played + ',' + team1Won + ',' + team1rating + ',' + team2rating + ',' + team1kd + ',' + team2kd + ',' + team1mapwin + ',' + team2mapwin + ',' + team1pistol + ',' + team2pistol + ',' + team1firstkill + ',' + team2firstkill + ',' + team1firstdeath + ',' + team2firstdeath
            csv += line
    csvFile.write(csv)

def getVariables():
    with open("filterd_top20.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        rows = [r for r in reader]
        return rows[0]
        
def getDataReady():
    variables = getVariables()
    data = readCsv("filterd_top20.csv")
    dictio = []
    winner = []
    for i in range(len(data)):
        #check if team1 has higher rating:
        if data[i][4] > data[i][5]:
            rating = 'y'
        else:
            rating = 'n'
        
        #check if team1 has higher kd:
        if data[i][6] > data[i][7]:
            kd = 'y'
        else:
            kd = 'n'
        
        #check if team1 has higher map win %:
        if data[i][8] > data[i][9]:
            mapwin = 'y'
        else:
            mapwin = 'n'
        
        #check if team1 has higher pistol win %:
        if data[i][10] > data[i][11]:
            pistol = 'y'
        else:
            pistol = 'n'
            
        #check if team1 has higher win after first_kill:
        if data[i][12] > data[i][13]:
            firstkill = 'y'
        else:
            firstkill = 'n'
        
        #check if team1 has higher win after first_death:
        if data[i][14] > data[i][15]:
            firstdeath = 'y'
        else:
            firstdeath = 'n'
            
        dictio.append({"Team 1":data[i][0], "Team 2":data[i][1], "Map":data[i][2],
                       "Team 1 has higher rating":rating, "Team 1 has higher kd":kd, 
                       "Team 1 has higher map win %":mapwin, "Team 1 has higher pistol win %": pistol,
                       "Team 1 has higher win after first kill":firstkill, 
                       "Team 1 has higher win after first death":firstdeath})
        #need to change this part after changing og data format:
        winner.append(True)
        
    inputs = [(c,a) for c,a in zip(dictio, winner)]
    return inputs
         
"""
Team1name,Team2name,MapName,Team1wonthegame,Team1hasHigherRating,Team1hasHigherKD

Hardcode rankings"""

inputs = [
        ({'Map':'','Team1hashigherrating':'','Team1hasHigherAverageKD':'','Team1HasHigherMapWinRateOnMap':'','Team1HasHigherPistolRoundWinRateOnMap':''},   False),
        ({'Map':'','Team1hashigherrating':'','Team1hasHigherAverageKD':'','Team1WinHasHigherWinRate':''},   False)]
