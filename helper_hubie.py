#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 13:53:55 2022

@author: tedwards
"""
import pandas as pd
from requests import get
from datetime import datetime
from bs4 import BeautifulSoup
#import numpy as np

full_team_names = ['ATLANTA HAWKS', 'BOSTON CELTICS', 'BROOKLYN NETS', 'CHICAGO BULLS',
                   'CHARLOTTE HORNETS', 'CLEVELAND CAVALIERS', 'DALLAS MAVERICKS', 'DENVER NUGGETS',
                   'DETROIT PISTONS', 'GOLDEN STATE WARRIORS', 'HOUSTON ROCKETS', 'INDIANA PACERS',
                   'LOS ANGELES CLIPPERS', 'LOS ANGELES LAKERS', 'MEMPHIS GRIZZLIES', 'MIAMI HEAT',
                   'MILWAUKEE BUCKS', 'MINNESOTA TIMBERWOLVES', 'NEW ORLEANS PELICANS', 'NEW YORK KNICKS',
                   'OKLAHOMA CITY THUNDER', 'ORLANDO MAGIC', 'PHILADELPHIA 76ERS', 'PHOENIX SUNS',
                   'PORTLAND TRAIL BLAZERS', 'SACRAMENTO KINGS', 'SAN ANTONIO SPURS', 'TORONTO RAPTORS',
                   'UTAH JAZZ', 'WASHINGTON WIZARDS']
abbreviated_team_names = ['ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
                          'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
                          'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
team_names = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Chicago Bulls', 'Charlotte Hornets', 'Cleveland Cavaliers', 
              'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers',
              'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwuakee Bucks', 'Minnesota Timberwolves',
              'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic', 'Philidelphia 76ers', 'Phoenix Suns',
              'Portland Trailblazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']

def area(x1,y1,x2,y2,x3,y3):
    return abs((x1*(y2-y3)+(x2*(y3-y1))+(x3*(y1-y2)))/2.0)

def classify_hubie(xval, yval):
    group = 0
    if (yval >= 19):
        if (yval <= 24):
            if (xval >= 1) & (xval <= 49):
                group = 3
            else:
                group = 4
        else:
            group = 4
    elif yval < 19:
        if xval <= 17:
            #Triangle R
            A=area(17,3,3,3,17,19) #MNO
            A1=area(17,3,3,3,xval,yval) #MNB
            A2=area(17,3,17,19,xval,yval) #MOB
            A3=area(3,3,17,19,xval,yval) #NOB
            if (A1)+(A2)+(A3)==A:
                group = 1
            else:
                group = 4
        elif xval >= 33:
            #Triangle L 
            A=area(47,3,33,3,33,19) #MNO
            A1=area(47,3,33,3,xval,yval) #MNB
            A2=area(47,3,33,19,xval,yval) #MOB
            A3=area(33,3,33,19,xval,yval) #NOB
            if (A1)+(A2)+(A3)==A:
                group = 2
            else:
                group = 4
        else:
            group = 4
    else:        
        group = 4
    return group

def get_abbreviation(team_name):
    for z in range(0, len(full_team_names)):
        curr_team = full_team_names[z]
        if(curr_team == team_name):
            return abbreviated_team_names[z]

def get_unabbreviated(team_abbr):
    for z in range(0, len(abbreviated_team_names)):
        curr_team = abbreviated_team_names[z]
        if(curr_team == team_abbr):
            return team_names[z]
    
def get_schedule(season, playoffs=False):
    months = ['October', 'November', 'December', 'January', 'February', 'March',
            'April', 'May', 'June']
    if season==2020:
        months = ['October-2019', 'November', 'December', 'January', 'February', 'March',
                'July', 'August', 'September', 'October-2020']
    df = pd.DataFrame()
    for month in months:
        r = get(f'https://www.basketball-reference.com/leagues/NBA_{season}_games-{month.lower()}.html')
        print(r)
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table', attrs={'id': 'schedule'})
            if table:
                month_df = pd.read_html(str(table))[0]
                df = pd.concat([df, month_df])
        else:
            print("Failing to obtain proper status code. ")

    df = df.reset_index()

    cols_to_remove = [i for i in df.columns if 'Unnamed' in i]
    cols_to_remove += [i for i in df.columns if 'Notes' in i]
    cols_to_remove += [i for i in df.columns if 'Start' in i]
    cols_to_remove += [i for i in df.columns if 'Attend' in i]
    cols_to_remove += [i for i in df.columns if 'Arena' in i]
    cols_to_remove += ['index']
    df = df.drop(cols_to_remove, axis=1)
    df.columns = ['DATE', 'VISITOR', 'VISITOR_PTS', 'HOME', 'HOME_PTS']
    return df
    
    
"""    
ATLANTA HAWKS : ATL
BOSTON CELTICS : BOS
BROOKLYN NETS : BRK
CHICAGO BULLS : CHI
CHARLOTTE HORNETS : CHO
CLEVELAND CAVALIERS : CLE
DALLAS MAVERICKS : DAL
DENVER NUGGETS : DEN
DETROIT PISTONS : DET
GOLDEN STATE WARRIORS : GSW
HOUSTON ROCKETS : HOU
INDIANA PACERS : IND
LOS ANGELES CLIPPERS : LAC
LOS ANGELES LAKERS : LAL
MEMPHIS GRIZZLIES : MEM
MIAMI HEAT : MIA
MILWAUKEE BUCKS : MIL
MINNESOTA TIMBERWOLVES : MIN
NEW ORLEANS PELICANS : NOP
NEW YORK KNICKS : NYK
OKLAHOMA CITY THUNDER : OKC
ORLANDO MAGIC : ORL
PHILADELPHIA 76ERS : PHI
PHOENIX SUNS : PHO
PORTLAND TRAIL BLAZERS : POR
SACRAMENTO KINGS : SAC
SAN ANTONIO SPURS : SAS
TORONTO RAPTORS : TOR
UTAH JAZZ : UTA
WASHINGTON WIZARDS : WAS
"""
