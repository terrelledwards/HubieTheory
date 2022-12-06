#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 08:28:02 2022

@author: tedwards
"""

"""
The aim of this part of the project is to test if Hubie Brown's theory can be exteneded to looking at how teams defend. 
All of the shots against a certain team will be recorded by noting their Hubie value and make/miss status. 
All of the data for each team will be amalgamated into a single dataframe for an exploratory analysis in RStudio. 
"""

"""
In order for this data to be useful for predictions, we need to record the wins and losses along with the Hubie values per game 
"""

#from basketball_reference_scraper.teams import get_roster_stats
from basketball_reference_scraper.shot_charts import get_shot_chart
from basketball_reference_scraper.seasons import get_schedule, get_standings
#import matplotlib.pyplot as plt
from BasketballConstants import Constant
import re
from helper_hubie import get_abbreviation, classify_hubie
import pandas as pd
from datetime import datetime, timedelta
import time

season_endyear = 2023
#Currently, an error is being thrown——Length mismatch:
latest_schedule = pd.DataFrame({
    'DATE': [],
    'VISITOR': [],
    'VISITOR_PTS': [],
    'HOME': [],
    'HOME_PTS': []
    
    })
hubie_stats = pd.DataFrame({
    'Team_Name': [],
    'Zone_1_Makes': [],
    'Zone_1_Attempts': [],
    'Zone_2_Makes': [],
    'Zone_2_Attempts': [],
    'Zone_3_Makes': [],
    'Zone_3_Attempts': [],
    'Zone_4_Makes': [],
    'Zone_4_Attempts': [],
    'Date':[],
    'Win_or_Lose': []
    })

latest_schedule = get_schedule(season_endyear, playoffs=False)
latest_standings = get_standings(date=None)
east_teams = latest_standings['EASTERN_CONF']['TEAM']
west_teams = latest_standings['WESTERN_CONF']['TEAM']


for z in range(0, len(east_teams)):
    curr_team_games = latest_schedule[((latest_schedule.VISITOR == east_teams[z]) | (latest_schedule.HOME == east_teams[z])) & (latest_schedule.DATE < (datetime.now()-timedelta(days=4)))]
    curr_team = get_abbreviation(east_teams[z].upper())
    print(curr_team)
    
    for index, row in curr_team_games.iterrows():
        zone_one_makes, zone_one_attempts, zone_two_makes, zone_two_attempts = (0,0,0,0)
        zone_three_makes, zone_three_attempts, zone_four_makes, zone_four_attempts = (0,0,0,0)
        win_lose = 0 #0 will be used to denote a loss
        date = curr_team_games.DATE[index].date()
        #date = date.date()
        print(date)
        
        home_team = get_abbreviation(curr_team_games.HOME[index].upper())
        away_team = get_abbreviation(curr_team_games.VISITOR[index].upper())
        home_team_pts = curr_team_games.HOME_PTS[index]
        away_team_pts = curr_team_games.VISITOR_PTS[index]
        
        curr_game_shot_chart = get_shot_chart(date, home_team, away_team)
        if(curr_game_shot_chart == None): print("Curr Game Shot Chart is Empty")
        time.sleep(5)
        
        #Here we want to access the shot chart for the opposing team, not the shot chart for the team we currently are on in our loop.
        #This is accomplished by switching from == to != in our assignment of shot_chart
        if(home_team != curr_team):
            shot_chart = curr_game_shot_chart[home_team]
            #Here we need to check if the home_team which is not the team being examined won the game
            if(home_team_pts < away_team_pts): win_lose = 1
            
        else:
            shot_chart = curr_game_shot_chart[away_team]
            if(home_team_pts > away_team_pts): win_lose = 1
        
        for w in range(0, len(shot_chart)):
            x_loc = re.findall('[\d]*[.][\d]+', shot_chart.loc[w, 'x'])
            y_loc = re.findall('[\d]*[.][\d]+', shot_chart.loc[w, 'y'])
            
            hubie_value = classify_hubie(((Constant.Y_MAX) - float(x_loc[0]) -1), float(y_loc[0]) + 1)
            
            if(hubie_value == 1):
                zone_one_attempts+=1
                if(shot_chart.loc[w, 'MAKE_MISS'] == 'MAKE'): zone_one_makes+=1
            elif(hubie_value == 2):
                zone_two_attempts+=1
                if(shot_chart.loc[w, 'MAKE_MISS'] == 'MAKE'): zone_two_makes+=1
            elif(hubie_value == 3):
                zone_three_attempts+=1
                if(shot_chart.loc[w, 'MAKE_MISS'] == 'MAKE'): zone_three_makes+=1
            else:
                zone_four_attempts+=1
                if(shot_chart.loc[w, 'MAKE_MISS'] == 'MAKE'): zone_four_makes+=1
        final_row = [curr_team, zone_one_makes, zone_one_attempts, zone_two_makes, zone_two_attempts, zone_three_makes, zone_three_attempts, zone_four_makes, zone_four_attempts, date, win_lose]
        hubie_stats.loc[len(hubie_stats.index)] = final_row
        

















