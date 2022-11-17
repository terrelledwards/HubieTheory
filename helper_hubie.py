#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 13:53:55 2022

@author: tedwards
"""
import pandas as pd
import numpy as np

full_team_names = ['ATLANTA HAWKS', 'BOSTON CELTICS', 'BROOKLYN NETS', 'CHICAGO BULLS',
                   'CHARLOTTE HORNETS', 'CLEVELAND CAVALIERS', 'DALLAS MAVERICKS', 'DENVER NUGGETS',
                   'DETROIT PISTONS', 'GOLDEN STATE WARRIORS', 'HOUSTON ROCKETS', 'INDIANA PACERS',
                   'LOS ANGELES CLIPPERS', 'LOS ANGELES LAKERS', 'MEMPHIS GRIZZLIES', 'MIAMI HEAT',
                   'MILWAUKEE BUCKS', 'MINNESOTA TIMBERWOLVES', 'NEW ORLEANS PELICANS', 'NEW YORK KNICKS',
                   'OKLAHOMA CITY THUNDER', 'ORLANDO MAGIC', 'PHILADELPHIA 76ERS', 'PHOENIX SUNS',
                   'PORTLAND TRAIL BLAZERS', 'SACREMENTO KINGS', 'SAN ANTONIO SPURS', 'TORONTO RAPTORS',
                   'UTAH JAZZ', 'WASHINGTON WIZARDS']
abbreviated_team_names = ['ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
                          'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
                          'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
#data = [full_team_names, abbreviated_team_names]
#data = t(data)
#numpy_array = np.array(data)
#transpose = numpy_array.T
#transpose_list = transpose.tolist()
#df = pd.DataFrame(transpose, columns=['Full', 'Abbreviated'])

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
    #print(team_name)
   # print("Above is what we are searching for.")
    for z in range(0, len(full_team_names)):
        curr_team = full_team_names[z]
        #print(curr_team)
        #print(z)
        #print("We are looking through teams. Above is the team currently being viewed as well as the index.")
        if(curr_team == team_name):
            #print("Found match")
            #print(abbreviated_team_names[z])
            return abbreviated_team_names[z]
    #return abbreviated_team_names[index]
    
    
    
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
