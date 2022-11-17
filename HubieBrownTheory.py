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

from basketball_reference_scraper.teams import get_roster, get_team_stats, get_opp_stats, get_roster_stats, get_team_misc
from basketball_reference_scraper.shot_charts import get_shot_chart
from basketball_reference_scraper.seasons import get_schedule, get_standings
#import matplotlib.pyplot as plt
from BasketballConstants import Constant
import re
from helper_hubie import get_abbreviation, classify_hubie
import pandas as pd

"""
In the below code we are setting the season to be analyzed. Seasons are determined by the year of their end date. 
Then we are obtaining the schedule and standings for said year. If attempting to get the most recent year, 2023 cannot be used None must be.
Then, we seperate the lists into Eastern and Western Conference teams
In addition, we save the current date as we are working with continually updating data. 
Also saving the date helps to easily find the games the team has already played this season from the entire schedule.
"""
season_endyear = 2023
latest_schedule = get_schedule(season_endyear, playoffs=False)
latest_standings = get_standings(date=None)
east_latest_standings = latest_standings['EASTERN_CONF']
west_latest_standings = latest_standings['WESTERN_CONF']
east_teams = east_latest_standings['TEAM']
west_teams = west_latest_standings['TEAM']
curr_date = '2022-11-14 00:00:00'


#We need to create a mass dataframe that has an entry for [PlayerName, Zone 1 Makes, Zone 1 Attempts, Zone 1FG%, Zone 2 Makes, Zone 2 Attempts,
#Zone2FG%, Zone 3 Makes, Zone 3 Attempts, Zone3FG%, Zone 4 Makes, Zone 4 Attempts, and Zone4FG]
df_cols = ['Player', 'Zone_1_Makes', 'Zone_1_Attempts', 'Zone_1_FG%', 'Zone_2_Makes', 'Zone_2_Attempts', 'Zone_2_FG%',
           'Zone_3_Makes, Zone_3_Attempts', 'Zone_3_FG%', 'Zone_4_Makes', 'Zone_4_Attempts', 'Zone_4_FG%']
df_final = pd.DataFrame(columns=df_cols)


"""
In the code below, we seek to loop thru all the teams. 
As we loop through all the teams, we assemble a list of their games played so far this season. 
Next, we obtain the roster of the team. 
Then, we loop through the roster. In addition, we also want to loop through the teams games for each player. 
    As we loop through the roster, for each game, we want to obtain data on each players shot attempts (their location and result)
    We will use the location and result to tabulate their misses, makes, and field goal percentage 
"""

for z in range(0, len(east_teams)):
    
    curr_team_reg = east_teams[z]
    curr_team_upper = curr_team_reg.upper()
    curr_team_games = latest_schedule[((latest_schedule.VISITOR == curr_team_reg) | (latest_schedule.HOME == curr_team_reg)) & (latest_schedule.DATE < curr_date)]
    #print(curr_team)
    curr_team = get_abbreviation(curr_team_upper)
    print(curr_team)
    
    team_roster = get_roster_stats(team = curr_team, season_end_year=season_endyear, data_format = 'PER_GAME', playoffs=False)
    players = team_roster['PLAYER']
    for y in range(0, len(players)):
        curr_player_examining = players[y]
        zone_one_makes, zone_one_attempts, zone_one_fg, zone_two_makes, zone_two_attempts, zone_two_fg = (0,0,0,0,0,0)
        zone_three_makes, zone_three_attempts, zone_three_fg, zone_four_makes, zone_four_attempts, zone_four_fg = (0,0,0,0,0,0)
        for x in range(0, len(curr_team_games)):
            date = curr_team_games.DATE[x]
            date_no_time = date.date()
            home_team_reg = curr_team_games.HOME[x]
            away_team_reg = curr_team_games.VISITOR[x]
            home_team_upper = home_team_reg.upper()
            away_team_upper = away_team_reg.upper()
            home_team = get_abbreviation(home_team_upper)
            away_team = get_abbreviation(away_team_upper)
            
            curr_game_shot_chart = get_shot_chart(date_no_time, home_team, away_team)
            
            if(home_team == curr_team):
                shot_chart = curr_game_shot_chart[home_team]
            else:
                shot_chart = curr_game_shot_chart[away_team]
            
            x_locs = shot_chart['x']
            y_locs = shot_chart['y']
            make_miss = shot_chart['MAKE_MISS']
            player = shot_chart['PLAYER']
            
            for w in range(0, len(shot_chart)):
                x_loc = x_locs[w]
                y_loc = y_locs[w]
                result = make_miss[w]
                curr_player = player[w]
                if(curr_player_examining == curr_player):
                    x_loc = re.findall('[\d]*[.][\d]+', x_loc)
                    y_loc = re.findall('[\d]*[.][\d]+', y_loc)
                    x_loc_num = ((Constant.Y_MAX) - float(x_loc[0]) -1)
                    y_loc_num = float(y_loc[0]) + 1
                    #Here is where we need to find the zone
                    hubie_value = classify_hubie(x_loc_num, y_loc_num)
                    
                    if(hubie_value == 1):
                        zone_one_attempts+=1
                        if(result == 'MAKE'):
                            zone_one_makes+=1
                    elif(hubie_value == 2):
                        zone_two_attempts+=1
                        if(result == 'MAKE'):
                            zone_two_makes+=1
                    elif(hubie_value == 3):
                        zone_three_attempts+=1
                        if(result == 'MAKE'):
                            zone_three_makes+=1
                    else:
                        zone_four_attempts+=1
                        if(result == 'MAKE'):
                            zone_four_makes+=1
        if(zone_one_attempts != 0):
            zone_one_fg = zone_one_makes / zone_one_attempts
        if(zone_two_attempts != 0):
            zone_two_fg = zone_two_makes / zone_two_attempts
        if(zone_three_attempts != 0):
            zone_three_fg = zone_three_makes / zone_three_attempts
        if(zone_four_attempts != 0):
            zone_four_fg = zone_four_makes / zone_four_attempts
        #Here we want to create an object to add to the final dataframe 
        final_row = [curr_player_examining, zone_one_makes, zone_one_attempts, zone_one_fg, zone_two_makes, zone_two_attempts,
                     zone_two_fg, zone_three_makes, zone_three_attempts, zone_three_fg, zone_four_makes, zone_four_attempts,
                     zone_four_fg]
        df_final.concat(final_row, axis = 0)
            #rint(home_team)
            #We need to find all the shots the player had in a specific game, then asssign each shot to a zone. When the shot is assigned to a zone,
            #We must update 
                


















