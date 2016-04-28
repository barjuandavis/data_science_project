# -*- coding: utf-8 -*-
from scraper import scrape_map_stats
from scraper import scrape
from decision_trees import build_tree_id3
from decision_trees import classify
import os.path, csv, random

#Hard coded Team Data
teams=[	  {'Team Name':'Natus Vincere','Team Rank':1,'Team id':4608,'KD':1.07, 'Rating':1.044},
		  {'Team Name':'Luminosity','Team Rank':2,'Team id':6290,'KD':1.14, 'Rating':1.106},
		  {'Team Name':'fnatic','Team Rank':3,'Team id':4991,'KD':1.12, 'Rating':1.084},
		  {'Team Name':'Astralis','Team Rank':4,'Team id':6665,'KD':1.11, 'Rating':1.06},
		  {'Team Name':'NiP','Team Rank':5,'Team id':4411,'KD':1.16, 'Rating':1.114},
		  {'Team Name':'EnVyUs','Team Rank':6,'Team id':5991,'KD':1.07, 'Rating':1.072},
		  {'Team Name':'Virtus.pro','Team Rank':7,'Team id':5378,'KD':1.06, 'Rating':1.046},
		  {'Team Name':'dignitas','Team Rank':8,'Team id':5422,'KD':1.05, 'Rating':1.024},
		  {'Team Name':'mousesports','Team Rank':9,'Team id':4494,'KD':1.04, 'Rating':1.074},
		  {'Team Name':'Liquid','Team Rank':10,'Team id':5973,'KD':1.08, 'Rating':1.064},
		  {'Team Name':'CLG','Team Rank':11,'Team id':5974,'KD':1.05, 'Rating':1.04},
		  {'Team Name':'GODSENT','Team Rank':12,'Team id':6902,'KD':1.03, 'Rating':1.03},
		  {'Team Name':'G2','Team Rank':13,'Team id':5995,'KD':1.01, 'Rating':1.056},
		  {'Team Name':'Tempo Storm','Team Rank':14,'Team id':6118,'KD':1.12, 'Rating':1.03},
		  {'Team Name':'TyLoo','Team Rank':15,'Team id':4863,'KD':1.04, 'Rating':1.152},
		  {'Team Name':'Cloud9','Team Rank':16,'Team id':5752,'KD':1.06, 'Rating':1.026},
		  {'Team Name':'HellRaisers','Team Rank':17,'Team id':5310,'KD':1.03, 'Rating':1.056},
		  {'Team Name':'FaZe','Team Rank':18,'Team id':6667,'KD':0.99, 'Rating':1.046},
		  {'Team Name':'Gambit','Team Rank':19,'Team id':6651,'KD':1.00, 'Rating':1.018},
		  {'Team Name':'E-frag.net','Team Rank':20,'Team id':6226,'KD':1.09, 'Rating':1.05}]

maps = ["dust2","mirage","inferno","cache","train","cobblestone","overpass"]
#csgoData=[]

#Checks if a team is part of the top 20
def isTop20(input):
    for i in range(len(teams)):
        if (input == teams[i]['Team Name']):
            return True
    return False

#Checks if a team is part of our map pool
def isMap(input):
    if input in maps:
        return True
    return False

#Returns team's rating from hard coded data
def get_rating(input):
    for i in range(len(teams)):
        if(input == teams[i]['Team Name']):
            return teams[i]['Rating']
    return 0

#Returns team's HLTV ranking from hard coded data
def get_rank(input):
    for i in range(len(teams)):
        if(input == teams[i]['Team Name']):
            return teams[i]['Team Rank']
    return 0 

#Returns team's KD from hard coded data
def get_kd(input):
    for i in range(len(teams)):
        if(input == teams[i]['Team Name']):
            return teams[i]['KD']
    return 0

#Function to read CSV file and return it as a list
def readCsv(fileName):
    with open(fileName, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        rows = [r for r in reader]
    return rows

#Returns a team's stats for a particular map
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
            
#Creates a new CSV file with data from only the top 20 teams
def filterCSV():
    og_data = readCsv("csgo_results.csv")
    csv=''
    csvFile = open("filtered_top20.csv",'w')
    csvFile.write("Team 1,Team 2,Map,Winner,Team 1 rank,Team 2 rank,Team 1 Rating,Team 2 Rating,Team 1 KD,Team 2 KD,Team 1 Map Win %,Team 2 Map Win %,Team 1 Pistol Round Win %,Team 2 Pistol Round Win %,Team 1 first kill win %,Team 2 first kill win %,Team 1 first death win %,Team 2 first death win %")
    for data in og_data:
        if (isTop20(data[0]) and isTop20(data[1]) and isMap(data[5])):
            team1name = data[0]
            team2name = data[1]
            #update this if we change format of our og data
            teamwon = data[2]
            map_played = data[5]
            team1rank = str(get_rank(team1name))
            team2rank = str(get_rank(team2name))
            team1rating = str(get_rating(team1name))
            team2rating = str(get_rating(team2name))
            team1kd = str(get_kd(team1name))
            team2kd = str(get_kd(team2name))
            
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
            line = '\n' + team1name + ',' + team2name + ',' + map_played + ',' + teamwon + ',' + team1rank + ',' + team2rank + ',' + team1rating + ',' + team2rating + ',' + team1kd + ',' + team2kd + ',' + team1mapwin + ',' + team2mapwin + ',' + team1pistol + ',' + team2pistol + ',' + team1firstkill + ',' + team2firstkill + ',' + team1firstdeath + ',' + team2firstdeath
            csv += line
    csvFile.write(csv)
    csvFile.close

#Returns the names of the variables stored in our data file
def getVariables():
    if os.path.isfile("filtered_top20.csv"):
        with open("filtered_top20.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',')
            rows = [r for r in reader]
            for i in rows[0]:
                print(i)
    else:
        print('\"filtered_top20.csv\" was not found.')

#Sets up training data for Decision tree Algorithm
def getDataReady():
    data = readCsv("filtered_top20.csv")
    dictio = []
    winner = []
    for i in range(len(data)):
        #check if team1 has better rank: 
        rank = 'n'
        if float(data[i][4]) < float(data[i][5]):
            rank = 'y'
            
        #check if team1 has higher rating:
        rating = 'n'
        if float(data[i][6]) > float(data[i][7]):
            rating = 'y'        
        
        #check if team1 has higher kd:
        kd = 'n'
        if float(data[i][8]) > float(data[i][9]):
            kd = 'y'
        
        #check if team1 has higher map win %:
        mapwin = 'n'
        if float(data[i][10]) > float(data[i][11]):
            mapwin = 'y'
        
        #check if team1 has higher pistol win %:
        pistol = 'n'
        if float(data[i][12]) > float(data[i][13]):
            pistol = 'y'
            
        #check if team1 has higher win after first_kill:
        firstkill = 'n'
        if float(data[i][14]) > float(data[i][15]):
            firstkill = 'y'
        
        #check if team1 has higher win after first_death:
        firstdeath = 'n'
        if float(data[i][16]) > float(data[i][17]):
            firstdeath = 'y'
            
        dictio.append({"Map":data[i][2],
                       "Team 1 has higher rating":rating, "Team 1 has higher kd":kd, 
                       "Team 1 has higher map win %":mapwin, "Team 1 has higher pistol win %": pistol,
                       "Team 1 has higher win after first kill":firstkill, 
                       "Team 1 has higher win after first death":firstdeath,
                       "Team 1 has better rank" : rank})
        
        
        if data[i][0] == data[i][3]:
            winner.append(True)
        else:
            winner.append(False)
        
    inputs = [(c,a) for c,a in zip(dictio, winner)]
    return inputs
    
#Prepares user entered data for use with Decision tree
def userInputStats(team1, team2, m):
    map_data1 = returnMapStats(team1, m)
    map_data2 = returnMapStats(team2, m)
    
    rank = 'n'
    if (get_rank(team1) < get_rank(team2)):
        rank = 'y'
    
    kd = 'n'
    if (get_kd(team1) > get_kd(team2)):
        kd = 'y'
        
    map_win = 'n'
    if (float(map_data1[0]) > float(map_data2[0])):
        map_win = 'y'
    
    pistol = 'n'
    if (float(map_data1[1]) > float(map_data2[1])):
        pistol = 'y'
        
    rating = 'n'
    if (get_rating(team1) > get_rating(team2)):
        rating = 'y'

    first = 'n'
    if (float(map_data1[2]) > float(map_data2[2])):
        first = 'y'    
    
    death = 'n'
    if (float(map_data1[3]) > float(map_data2[3])):
        death = 'y'
        
    output = {
    'Team 1 has higher kd': kd,
    'Team 1 has higher map win %': map_win,
    'Team 1 has higher pistol win %': pistol,
    'Team 1 has higher rating':rating,
    'Team 1 has higher win after first death':death,
    'Team 1 has higher win after first kill':first,
    'Team 1 has better rank':rank
    }
    return output

#Print out list of top 20 team names
def teamNames():
    print("Team Names:")
    for i in teams:
        print(i['Team Name'])
        
#Print out maps in our map pool
def mapNames():
    print("Map Names:")
    for i in maps:
        print(i)

#Train data on 60% of the dataset and test on the rest 40%
def accuracy():
    if os.path.isfile('filtered_top20.csv'):
        data_set = getDataReady()
        train_data = []
        for i in range(int(len(data_set)*0.1)):
            train_data.append(data_set[i])
            
        tree = build_tree_id3(train_data)
        
        data = readCsv("filtered_top20.csv")
        counter = 0
        counter2 = 0
        for i in range(int(len(data_set)*0.1), len(data)):
            team1 = data[i][0]
            team2 = data[i][1]
            m = data[i][2]
            
            #make winner to true if team 1 won the game            
            winner = False
            if(data[i][3] == data[i][0]):
                winner = True
            boolean = {True : team1, False : team2} 
            
            #test if our predicted result is same is winner of the game
            if boolean[classify(tree,userInputStats(team1, team2, m))] and winner:
                counter += 1
            
            if not boolean[classify(tree,userInputStats(team1, team2, m))] and not winner:
                counter2 += 1
        
        acc = ((counter + counter2) / ((len(data)) - (int(len(data_set)*0.1))))*100
        print("The algorithm is {}% accurate.".format(acc))
    else:
        print('\"filtered_top20.csv\" was not found. Please scrape for data before attempting to predict')

#Main function to run all the code by itself, add number of pages to scrape
def predict(pages, team1, team2, m):
    #make sure we have data on these teams
    if not(isTop20(team1)):
        print("Team 1 is not a top 20 team")
        return
    if not(isTop20(team2)):
        print("Team 2 is not a top 20 team")
        return 
    if not(isMap(m)):
        print("The map is not in our pool")
        return
    if pages>0:
        print("Scraping process will take some time, please be patient")
        print("**********Scraping Map Results now**********")
        scrape(pages)
        print("**********Scraping Map Stats now**********")
        scrape_map_stats()
        print("**********Filtering Data now**********")
        filterCSV()
        print("**********Generating Data now**********")
    #Make sure we have a "filtered_top20.csv" file to examine (in case the user doesn't scrape)
    if os.path.isfile('filtered_top20.csv'):
        data = getDataReady()
        tree = build_tree_id3(data)
        boolean = {True : team1, False : team2}
        print("{} would win.".format(boolean[classify(tree,userInputStats(team1, team2, m))]))  
    else:
        print('\"filtered_top20.csv\" was not found. Please scrape for data before attempting to predict')
    
#User instructions
print('CSGO Match Predictor.\n\nTo use call the predict function using these values.\n\npredict(# of HLTV pages to scrape data from, Team 1 name, Team 2 name, Map to be Played)\n')
print('If pages is set to 0, data will not be scraped and any previously scraped data will be used.\n')
print('This program is designed to predict from the top 20 current teams (As Ranked by HLTV)\nand the maps in the current map pool.\n')
print('To see a list of the teams, call the \"teamNames()\" function.\n')
print('To see a list of maps, call the \"mapNames()\" function.\n')
print('Team and Map names are case sensitive.\n')