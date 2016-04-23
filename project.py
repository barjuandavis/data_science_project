# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:06:25 2016

@author: David Ruan
"""
from bs4 import BeautifulSoup
import requests

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
            line+=str('\n' + secondTeam + ',' + firstTeam + ',' + str(secondScore) + ',' + str(firstScore) + ',' + thisMap)
            #convert to csv format
    return line
    
#Only run this if you want new data (Will overwrite the previoius csv file)
def scrape(pages):
    print("Scraping. Please be patient")
    csv=''
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
            csv+=extractDataIntoCondensedList(result)
    csvFile.write(csv)

scrape(100)
