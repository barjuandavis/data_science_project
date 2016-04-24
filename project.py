# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:06:25 2016

@author: David Ruan
"""
from bs4 import BeautifulSoup
import requests, csv

csgoData=[]

def extractDataIntoCondensedList(match):
    line=''
    #match is a list
    thisMap=(match[2].replace(' - ', ' ').split(' '))[0]
    firstTeam=(match[2].replace(' - ', ' ').split(' '))[1]
    secondTeam=(match[13].strip())
    firstScore=int((match[7].replace(' - ', ' ').split(' '))[0])
    secondScore=int((match[7].replace(' - ', ' ').split(' '))[1])
    #do not include anything other than best of 1's
    if (firstScore+secondScore>=16):
        if (firstScore>secondScore):
            #print(firstTeam+' beat ' + secondTeam + ' ' + str(firstScore) + '-' + str(secondScore) +' on '+thisMap)
            #convert into csv format
            line+=str('\n' + firstTeam + ',' + secondTeam + ',' + str(firstScore) + ',' + str(secondScore) + ',' + thisMap)
        else:
            #print(secondTeam+' beat ' + firstTeam + ' ' + str(secondScore) + '-' + str(firstScore) +' on '+thisMap)
            #convert to csv format
            line+=str('\n' + secondTeam + ',' + firstTeam + ',' + str(secondScore) + ',' + str(firstScore) + ',' + thisMap)
#    else:
#        print("Not a Best of 1")
#        print(match)
    return line
    
#Only run this if you want new data (Will overwrite the previoius csv file)
def scrape(pages):
    print("Scraping. Please be patient")
    csvContents=''
    for i in range(pages):
        hltvUrl = "http://www.hltv.org/results/"
        if i==0:
            csvFile = open("csgo_results.csv",'w')
            csvFile.write("Winning Team, Losing Team, Winning Score, Losing Score, Map Played")
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

#def deepScrape(matchPage):
    

scrape(100)
csgoData = readCsv('csgo_results.csv')