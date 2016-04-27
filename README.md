## CS:GO Game Predictor

Download all the .py files. 

(Note: download the .csv files if you don't want to scrape data yourself. The main data set, csgo_results.csv, has data from 200 pages)

#Usage

Once you have all the required files, run the project.py file. This will import any necessary modules and python files.
These instructions are also provided when running the program. 
To use call the "predict()" function using these values

predict(# of HLTV pages to scrape data from, Team 1 name, Team 2 name, Map to be Played)
  
If pages is set to 0, data will not be scraped and any previously scraped data will be used.
This program is designed to predict from the top 20 current teams (As Ranked by HLTV)\nand the maps in the current map pool.
To see a list of the teams, call the "teamNames()" function.
To see a list of maps, call the "mapNames()" function.
Team and Map names are case sensitive.

#Notes
This program is only designed to work with the current (at the time of writing) top 20 teams, as rated by HLTV
This allows us to make sure we have enough stats for these teams.
Hard coded variables include
-Team Rank (As determined by HLTV ranking system at the time of writing.)
-Team Id - (As seen in hltv url)
-KD - (Found on individual team stats page)
-Rating (This was calculated by averaging the player ratings of the current rosters for each of the top 20 teams)
-Hltv scraping is done using BeautifulSoup 4.
-This program makes use of the decision tree algorithm code written by Joel Grus
