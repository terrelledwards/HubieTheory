# Hubie_Brown_Theory_Test

The goal of this project is to test Hubie Brown's theory that is outlined here: https://www.breakthroughbasketball.com/stats/using-shot-charts.html#:~:text=On%20the%20shot%20chart%2C%20you,the%20page%20without%20the%20circle.

Using the Basketball-Reference-Scraper-API detailed here: https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/API.md we will access the requisite shot chart data for each player to calculate their FG% from the different shooting zones outlined by Hubie Brown. 

The files HubieComplete.py and helper_hubie.py contain all of the relevant code. The additional files are previous versions of the code. In HubieComplete, the end year of the season must be specified. Using just that, the Hubie Values by player and team are generated for the season ending with the specified year. The file helper_hubie contains additional helper functions. 
