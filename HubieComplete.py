#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 13:21:33 2022

@author: tedwards
"""

"""
The aim of this project is to test Hubie Brown's reported theory that players only shoot
well from 2 out of 3 of his projected zones onto an NBA basketball court.
"""

from basketball_reference_scraper.teams import get_roster_stats, get_roster
from basketball_reference_scraper.shot_charts import get_shot_chart
from basketball_reference_scraper.seasons import get_schedule, get_standings
#import matplotlib.pyplot as plt
from BasketballConstants import Constant
import re
from helper_hubie import get_abbreviation, get_unabbreviated, classify_hubie#, get_schedule
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
latest_schedule = pd.DataFrame({
    'DATE': [],
    'VISITOR': [],
    'VISITOR_PTS': [],
    'HOME': [],
    'HOME_PTS': []
    
    })
hubie_stats = pd.DataFrame({
    'Player_Name': [],
    'Zone_1_Attempts': [],
    'Zone_2_Attempts': [],
    'Zone_3_Attempts': [],
    'Zone_4_Attempts': [],
    'Zone_1_Makes': [],
    'Zone_2_Makes': [],
    'Zone_3_Makes': [],
    'Zone_4_Makes': [],
    'Player_Team': []
    })
hubie_stats_team_off = pd.DataFrame({
    'Team_Name': [],
    'Zone_1_Attempts': [],
    'Zone_2_Attempts': [],
    'Zone_3_Attempts': [],
    'Zone_4_Attempts': [],
    'Zone_1_Makes': [],
    'Zone_2_Makes': [],
    'Zone_3_Makes': [],
    'Zone_4_Makes': [],
    'Win_Or_Lose': []
    })
hubie_stats_team_def = pd.DataFrame({
    'Team_Name': [],
    'Zone_1_Attempts': [],
    'Zone_2_Attempts': [],
    'Zone_3_Attempts': [],
    'Zone_4_Attempts': [],
    'Zone_1_Makes': [],
    'Zone_2_Makes': [],
    'Zone_3_Makes': [],
    'Zone_4_Makes': [],
    'Win_Or_Lose': []
    })
hubie_stats_team_avg_off = pd.DataFrame({
    'Team_Name': [],
    'Zone_1_Attempts': [],
    'Zone_2_Attempts': [],
    'Zone_3_Attempts': [],
    'Zone_4_Attempts': [],
    'Zone_1_Makes': [],
    'Zone_2_Makes': [],
    'Zone_3_Makes': [],
    'Zone_4_Makes': []
    })
hubie_stats_team_avg_def = pd.DataFrame({
    'Team_Name': [],
    'Zone_1_Attempts': [],
    'Zone_2_Attempts': [],
    'Zone_3_Attempts': [],
    'Zone_4_Attempts': [],
    'Zone_1_Makes': [],
    'Zone_2_Makes': [],
    'Zone_3_Makes': [],
    'Zone_4_Makes': []
    })

latest_schedule = get_schedule(season_endyear, playoffs=False)
"""
latest_standings = get_standings(date=None)
east_teams = latest_standings['EASTERN_CONF']['TEAM']
west_teams = latest_standings['WESTERN_CONF']['TEAM']
"""
teams = ["ATL", "BOS","BRK","CHI","CHO","CLE", "DAL","DEN","DET","GSW","HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOP","NYK","OKC","ORL","PHI","PHO","POR","SAC","SAS","TOR","UTA","WAS"]


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

for z in range(0, len(teams)):
    curr_team_games = latest_schedule[((latest_schedule.VISITOR == get_unabbreviated(teams[z])) | (latest_schedule.HOME == get_unabbreviated(teams[z]))) & (latest_schedule.DATE < (datetime.now()-timedelta(days=1)))]
    #curr_team = get_abbreviation(east_teams[z].upper())
    curr_team = teams[z]
    print(curr_team)
    
    #team_roster = get_roster_stats(team = curr_team, season_end_year=season_endyear, data_format = 'PER_GAME', playoffs=False)
    team_ros = get_roster(curr_team, season_endyear)
    
    blank_row_team = [curr_team, 0,0,0,0,0,0,0,0]
    hubie_stats_team_avg_off.loc[len(hubie_stats_team_avg_off.index)] = blank_row_team
    hubie_stats_team_avg_def.loc[len(hubie_stats_team_avg_def.index)] = blank_row_team
    
    for y in range(0, len(team_ros['PLAYER'])):
        #curr_player_examining = team_roster.PLAYER[y]
        print(team_ros.PLAYER[y])
        #This regex is required because there are sometimes weird spaces or notation for different contracts 
        #Only players that appear in the call get_roster will be recorded,
        curr_player = re.findall("^[^\(]+", team_ros.PLAYER[y])[0]
        if(curr_player[-1] == " "):
            curr_player = curr_player[:-1]
        print(curr_player)
        blank_row = [curr_player, 0, 0, 0, 0, 0, 0, 0, 0, curr_team]
        hubie_stats.loc[len(hubie_stats.index)] = blank_row
     
    for index, row in curr_team_games.iterrows():
        date = curr_team_games.DATE[index].date()
        #date = date.date()
        print(date)
        
        z1m, z1a, z2m, z2a = (0,0,0,0)
        z3m, z3a, z4m, z4a = (0,0,0,0)
        def_z1m, def_z1a, def_z2m, def_z2a = (0,0,0,0)
        def_z3m, def_z3a, def_z4m, def_z4a = (0,0,0,0)
        
        home_team = get_abbreviation(curr_team_games.HOME[index].upper())
        away_team = get_abbreviation(curr_team_games.VISITOR[index].upper())
                   
        curr_game_shot_chart = get_shot_chart(date, home_team, away_team)
        if(curr_game_shot_chart == None): 
            print("Curr Game Shot Chart is Empty. Pausing then trying again.")
            time.sleep(60)
            curr_game_shot_chart = get_shot_chart(date, home_team, away_team)
        time.sleep(5)
        
        win_or_lose = 0
        if(home_team == curr_team):
            off_shot_chart = curr_game_shot_chart[home_team]
            def_shot_chart = curr_game_shot_chart[away_team]
            if curr_team_games.HOME_PTS[index] > curr_team_games.VISITOR_PTS[index]:
                win_or_lose = 1
        else:
            off_shot_chart = curr_game_shot_chart[away_team]
            def_shot_chart = curr_game_shot_chart[home_team]
            if curr_team_games.HOME_PTS[index] < curr_team_games.VISITOR_PTS[index]:
                win_or_lose = 1
        
        length = max(len(off_shot_chart), len(def_shot_chart))
        team_off_hubie_index = hubie_stats_team_avg_off[hubie_stats_team_avg_off.Team_Name == curr_team].index[0]
        team_def_hubie_index = hubie_stats_team_avg_def[hubie_stats_team_avg_def.Team_Name == curr_team].index[0]
        for w in range(0, length):
            if(w < len(off_shot_chart)):
                if(pd.isna(off_shot_chart.loc[w, 'PLAYER']) == False):
                    off_shooter = off_shot_chart.loc[w, 'PLAYER']
                    result = off_shot_chart.loc[w, 'MAKE_MISS']
                    
                    off_x_loc = re.findall('[\d]*[.][\d]+', off_shot_chart.loc[w, 'x'])
                    off_y_loc = re.findall('[\d]*[.][\d]+', off_shot_chart.loc[w, 'y'])
                    off_hubie_value = classify_hubie(((Constant.Y_MAX) - float(off_x_loc[0]) -1), float(off_y_loc[0]) + 1)
                    
                    shooter_in_roster = off_shooter in hubie_stats['Player_Name'].unique()
                    if(shooter_in_roster == True):
                        player_hubie_index = hubie_stats[hubie_stats.Player_Name == off_shooter].index[0]
                        if(off_hubie_value == 1):
                            hubie_stats.Zone_1_Attempts[player_hubie_index] = hubie_stats.Zone_1_Attempts[player_hubie_index] + 1
                            hubie_stats_team_avg_off.Zone_1_Attempts[team_off_hubie_index] = hubie_stats_team_avg_off.Zone_1_Attempts[team_off_hubie_index] + 1
                            z1a+=1
                            if(result == 'MAKE'): 
                                hubie_stats.Zone_1_Makes[player_hubie_index] = hubie_stats.Zone_1_Makes[player_hubie_index] + 1
                                hubie_stats_team_avg_off.Zone_1_Makes[team_off_hubie_index] = hubie_stats_team_avg_off.Zone_1_Makes[team_off_hubie_index] + 1
                                z1m+=1
                        if(off_hubie_value == 2):
                            hubie_stats.Zone_2_Attempts[player_hubie_index] = hubie_stats.Zone_2_Attempts[player_hubie_index] + 1
                            hubie_stats_team_avg_off.Zone_2_Attempts[team_off_hubie_index] = hubie_stats_team_avg_off.Zone_2_Attempts[team_off_hubie_index] + 1
                            z2a+=1
                            if(result == 'MAKE'): 
                                hubie_stats.Zone_2_Makes[player_hubie_index] = hubie_stats.Zone_2_Makes[player_hubie_index] + 1
                                hubie_stats_team_avg_off.Zone_2_Makes[team_off_hubie_index] = hubie_stats_team_avg_off.Zone_2_Makes[team_off_hubie_index] + 1
                                z2m+=1
                        if(off_hubie_value == 3):
                            hubie_stats.Zone_3_Attempts[player_hubie_index] = hubie_stats.Zone_3_Attempts[player_hubie_index] + 1
                            hubie_stats_team_avg_off.Zone_3_Attempts[team_off_hubie_index] = hubie_stats_team_avg_off.Zone_3_Attempts[team_off_hubie_index] + 1
                            z3a+=1
                            if(result == 'MAKE'): 
                                hubie_stats.Zone_3_Makes[player_hubie_index] = hubie_stats.Zone_3_Makes[player_hubie_index] + 1
                                hubie_stats_team_avg_off.Zone_3_Makes[team_off_hubie_index] = hubie_stats_team_avg_off.Zone_3_Makes[team_off_hubie_index] + 1
                                z3m+=1
                        if(off_hubie_value == 4):
                            hubie_stats.Zone_4_Attempts[player_hubie_index] = hubie_stats.Zone_4_Attempts[player_hubie_index] + 1
                            hubie_stats_team_avg_off.Zone_4_Attempts[team_off_hubie_index] = hubie_stats_team_avg_off.Zone_4_Attempts[team_off_hubie_index] + 1
                            z4a+=1
                            if(result == 'MAKE'): 
                                hubie_stats.Zone_4_Makes[player_hubie_index] = hubie_stats.Zone_4_Makes[player_hubie_index] + 1
                                hubie_stats_team_avg_off.Zone_4_Makes[team_off_hubie_index] = hubie_stats_team_avg_off.Zone_4_Makes[team_off_hubie_index] + 1
                                z4m+=1
            if(w < len(def_shot_chart)):
                if(pd.isna(def_shot_chart.loc[w, 'PLAYER']) == False):
                    result = def_shot_chart.loc[w, 'MAKE_MISS']
                    def_x_loc = re.findall('[\d]*[.][\d]+', def_shot_chart.loc[w, 'x'])
                    def_y_loc = re.findall('[\d]*[.][\d]+', def_shot_chart.loc[w, 'y'])
                    def_hubie_value = classify_hubie(((Constant.Y_MAX) - float(def_x_loc[0]) -1), float(def_y_loc[0]) + 1)
                    if(def_hubie_value == 1):
                        hubie_stats_team_avg_def.Zone_1_Attempts[team_def_hubie_index] = hubie_stats_team_avg_def.Zone_1_Attempts[team_def_hubie_index] + 1
                        def_z1a += 1
                        if(result == 'MAKE'):
                            hubie_stats_team_avg_def.Zone_1_Makes[team_def_hubie_index] = hubie_stats_team_avg_def.Zone_1_Makes[team_def_hubie_index] + 1
                            def_z1m += 1
                    if(def_hubie_value == 2):
                        hubie_stats_team_avg_def.Zone_2_Attempts[team_def_hubie_index] = hubie_stats_team_avg_def.Zone_2_Attempts[team_def_hubie_index] + 1
                        def_z2a += 1
                        if(result == 'MAKE'):
                            hubie_stats_team_avg_def.Zone_2_Makes[team_def_hubie_index] = hubie_stats_team_avg_def.Zone_2_Makes[team_def_hubie_index] + 1
                            def_z2m += 1
                    if(def_hubie_value == 3):
                        hubie_stats_team_avg_def.Zone_3_Attempts[team_def_hubie_index] = hubie_stats_team_avg_def.Zone_3_Attempts[team_def_hubie_index] + 1
                        def_z3a += 1
                        if(result == 'MAKE'):
                            hubie_stats_team_avg_def.Zone_3_Makes[team_def_hubie_index] = hubie_stats_team_avg_def.Zone_3_Makes[team_def_hubie_index] + 1
                            def_z3m += 1
                    if(def_hubie_value == 4):
                        hubie_stats_team_avg_def.Zone_4_Attempts[team_def_hubie_index] = hubie_stats_team_avg_def.Zone_4_Attempts[team_def_hubie_index] + 1
                        def_z4a += 1
                        if(result == 'MAKE'):
                            hubie_stats_team_avg_def.Zone_4_Makes[team_def_hubie_index] = hubie_stats_team_avg_def.Zone_4_Makes[team_def_hubie_index] + 1
                            def_z4m += 1
                    
        hubie_stats_team_off.loc[len(hubie_stats_team_off.index)] = [curr_team, z1a, z2a, z3a, z4a, z1m, z2m, z3m, z4m, win_or_lose]
        hubie_stats_team_def.loc[len(hubie_stats_team_def.index)] = [curr_team, def_z1a, def_z2a, def_z3a, def_z4a, def_z1m, def_z2m, def_z3m, def_z4m, win_or_lose]
        
        
