#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 12:34:30 2022

@author: tedwards
"""

"""
The aim of this project is to test Hubie Brown's reported theory that players only shoot
well from 2 out of 3 of his projected zones onto an NBA basketball court.
"""

from basketball_reference_scraper.teams import get_roster_stats
from basketball_reference_scraper.shot_charts import get_shot_chart
from basketball_reference_scraper.seasons import get_schedule, get_standings
#import matplotlib.pyplot as plt
from BasketballConstants import Constant
import re
from helper_hubie import get_abbreviation, classify_hubie
import pandas as pd
from datetime import datetime, timedelta
import time

"""
In the below code we are setting the season to be analyzed. Seasons are determined by the year of their end date. 
Then we are obtaining the schedule and standings for said year. If attempting to get the most recent year, 2023 cannot be used None must be.
Then, we seperate the lists into Eastern and Western Conference teams
In addition, we save the current date as we are working with continually updating data. 
Also saving the date helps to easily find the games the team has already played this season from the entire schedule.
"""
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
    'Player_Name': [],
    'Player_Team': [],
    'Zone_1_Makes': [],
    'Zone_1_Attempts': [],
    'Zone_1_FG%': [],
    'Zone_2_Makes': [],
    'Zone_2_Attempts': [],
    'Zone_2_FG%': [],
    'Zone_3_Makes': [],
    'Zone_3_Attempts': [],
    'Zone_3_FG%': [],
    'Zone_4_Makes': [],
    'Zone_4_Attempts': [],
    'Zone_4_FG%': []    
    })

latest_schedule = get_schedule(season_endyear, playoffs=False)
latest_standings = get_standings(date=None)
east_teams = latest_standings['EASTERN_CONF']['TEAM']
west_teams = latest_standings['WESTERN_CONF']['TEAM']

"""
east_latest_standings = latest_standings['EASTERN_CONF']
west_latest_standings = latest_standings['WESTERN_CONF']
east_teams = east_latest_standings['TEAM']
west_teams = west_latest_standings['TEAM']
curr_date = datetime.now()
"""

"""
We may want to restructure this to be like latest_schedule above where the columns are predefined. This may change how we index 
into the columns later on. We should still be able to call things like we do for latest_schedule.

In the code below, we seek to loop thru all the teams. 
As we loop through all the teams, we assemble a list of their games played so far this season. 
Next, we obtain the roster of the team. 
Then, we loop through the roster. In addition, we also want to loop through the teams games for each player. 
    As we loop through the roster, for each game, we want to obtain data on each players shot attempts (their location and result)
    We will use the location and result to tabulate their misses, makes, and field goal percentage 
"""

for z in range(0, len(west_teams)):
    curr_team_games = latest_schedule[((latest_schedule.VISITOR == west_teams[z]) | (latest_schedule.HOME == west_teams[z])) & (latest_schedule.DATE < (datetime.now()-timedelta(days=4)))]
    curr_team = get_abbreviation(west_teams[z].upper())
    print(curr_team)
    
    team_roster = get_roster_stats(team = curr_team, season_end_year=season_endyear, data_format = 'PER_GAME', playoffs=False)
    
    #This loop will successfully access all players on the team currently being examined 
    for y in range(0, len(team_roster['PLAYER'])):
        curr_player_examining = team_roster.PLAYER[y]
        print(curr_player_examining)
        zone_one_makes, zone_one_attempts, zone_one_fg, zone_two_makes, zone_two_attempts, zone_two_fg = (0,0,0,0,0,0)
        zone_three_makes, zone_three_attempts, zone_three_fg, zone_four_makes, zone_four_attempts, zone_four_fg = (0,0,0,0,0,0)
        for index, row in curr_team_games.iterrows():
            date = curr_team_games.DATE[index].date()
            #date = date.date()
            print(date)
            
            home_team = get_abbreviation(curr_team_games.HOME[index].upper())
            away_team = get_abbreviation(curr_team_games.VISITOR[index].upper())
            
            """
            if(home_team == None): home_team = get_abbreviation(row[3].upper())
            if(away_team == None): away_team = get_abbreviation(row[1].upper())
            """
            
            curr_game_shot_chart = get_shot_chart(date, home_team, away_team)
            if(curr_game_shot_chart == None): print("Curr Game Shot Chart is Empty")
            time.sleep(5)
            
            if(home_team == curr_team):
                shot_chart = curr_game_shot_chart[home_team]
            else:
                shot_chart = curr_game_shot_chart[away_team]
            
            for w in range(0, len(shot_chart)):
                if(curr_player_examining == shot_chart.loc[w, 'PLAYER']):
                    x_loc = re.findall('[\d]*[.][\d]+', shot_chart.loc[w, 'x'])
                    y_loc = re.findall('[\d]*[.][\d]+', shot_chart.loc[w, 'y'])
                    #x_loc_num = ((Constant.Y_MAX) - float(x_loc[0]) -1)
                    #y_loc_num = float(y_loc[0]) + 1
                    
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
        if(zone_one_attempts != 0):
            zone_one_fg = zone_one_makes / zone_one_attempts
        if(zone_two_attempts != 0):
            zone_two_fg = zone_two_makes / zone_two_attempts
        if(zone_three_attempts != 0):
            zone_three_fg = zone_three_makes / zone_three_attempts
        if(zone_four_attempts != 0):
            zone_four_fg = zone_four_makes / zone_four_attempts

        final_row = [curr_player_examining, curr_team, zone_one_makes, zone_one_attempts, zone_one_fg, zone_two_makes, zone_two_attempts,
                     zone_two_fg, zone_three_makes, zone_three_attempts, zone_three_fg, zone_four_makes, zone_four_attempts,
                     zone_four_fg]
        hubie_stats.loc[len(hubie_stats.index)] = final_row
                
