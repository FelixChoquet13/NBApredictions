#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 12:03:15 2016

@author: FelixChoquet
"""
# imports
import pandas as pd
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import datetime
import numpy as np
 

# variables              
teamNames = ['Cleveland', 'Sacramento', 'Golden State', 'Dallas', 'New Jersey',
       'Oklahoma City', 'Memphis', 'New Orleans', 'Atlanta', 'Indiana',
       'Houston', 'Phoenix', 'Boston', 'Minnesota', 'Miami',
       'Philadelphia', 'Detroit', 'Toronto', 'Portland', 'Milwaukee',
       'San Antonio', 'Denver', 'Charlotte', 'Chicago', 'Washington',
       'LA Lakers', 'Utah', 'New York', 'Orlando', 'LA Clippers','Brooklyn']       
datesLastGames = dict()
resultsLastGames = dict()
lastGames = dict()
lastAwayGames = dict()
lastHomeGames = dict()
lastOpposition = dict()
seasonLastOpposition = dict()
for team in teamNames:
    lastGames[team]=[]
    lastAwayGames[team] = []
    lastHomeGames[team] = []
    lastOpposition[team] = dict()
    seasonLastOpposition[team] = dict()
driver = webdriver.PhantomJS()
games = []

# scrapping
for year in range(2011,2017):
    for month in [1,2,3,4,10,11,12]:
        if month < 7:
            season = year
        else:
            season = year + 1
        for day in range (1,32):
            date = (month,day,year)
            adress = "http://www.basketball-reference.com/boxscores/index.cgi?month=%s&day=%s&year=%s"
            driver.get(adress%date)
            try:
                firstDigitNumberOfGames = driver.find_element_by_xpath('//*[@id="content"]/div[2]/h2').text[0]
                secondDigitNumberOfGames = driver.find_element_by_xpath('//*[@id="content"]/div[2]/h2').text[1]                                
                numberOfGames = int(firstDigitNumberOfGames+secondDigitNumberOfGames)
                for i in range(1,numberOfGames+1):
                    gameSummary = dict()
                    awayTeam = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[%s]/table[1]/tbody/tr[1]/td[1]/a'%i).text
                    homeTeam = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[%s]/table[1]/tbody/tr[2]/td[1]/a'%i).text                                        
                    gameSummary['awayTeam']= awayTeam
                    gameSummary['awayTeamScore']=driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[%s]/table[1]/tbody/tr[1]/td[2]'%i).text
                    gameSummary['homeTeam']= homeTeam
                    gameSummary['homeTeamScore']=driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[%s]/table[1]/tbody/tr[2]/td[2]'%i).text
                    gameSummary['year'] = year
                    gameSummary['month'] = month
                    gameSummary['day'] = day
                    gameSummary['season'] = season
                    gameSummary['percentageWinsAwayTeam10lastGamesBeforeGame'] = sum(lastGames[awayTeam][-10:])/10
                    gameSummary['percentageWinsHomeTeam10lastGamesBeforeGame'] = sum(lastGames[homeTeam][-10:])/10
                    gameSummary['percentageWinsAwayTeam5lastGamesBeforeGame'] = sum(lastGames[awayTeam][-5:])/5
                    gameSummary['percentageWinsHomeTeam5lastGamesBeforeGame'] = sum(lastGames[homeTeam][-5:])/5
                    gameSummary['percentageWinsAwayTeam3lastAwayGamesBeforeGame'] = sum(lastAwayGames[awayTeam][-3:])/3
                    gameSummary['percentageWinsHomeTeam3lastHomeGamesBeforeGame'] = sum(lastHomeGames[homeTeam][-3:])/3
                    #Extrait la dernière opposition lors de la même saison
                    try:
                        if seasonLastOpposition[homeTeam][awayTeam] == season:
                            gameSummary['resultLastOppositionForHomeTeam'] = lastOpposition[homeTeam][awayTeam]
                            gameSummary['resultLastOppositionForAwayTeam'] = lastOpposition[awayTeam][homeTeam]
                        else:
                            gameSummary['resultLastOppositionForHomeTeam'] = np.nan
                            gameSummary['resultLastOppositionForAwayTeam'] = np.nan
                    except KeyError:
                        gameSummary['resultLastOppositionForHomeTeam'] = np.nan
                        gameSummary['resultLastOppositionForAwayTeam'] = np.nan
                    #Extrait le nombre de jours depuis le dernier match
                    if homeTeam in datesLastGames.keys():
                        if (datetime.date(year,month,day)-datesLastGames[homeTeam]).days < 15:
                            gameSummary['daysSinceLastGameHomeTeam']=(datetime.date(year,month,day)-datesLastGames[homeTeam]).days
                    if awayTeam in datesLastGames.keys():
                        if (datetime.date(year,month,day)-datesLastGames[awayTeam]).days < 15:
                            gameSummary['daysSinceLastGameAwayTeam']=(datetime.date(year,month,day)-datesLastGames[awayTeam]).days
                    #Extrait le résultat du dernier match
                    if homeTeam in resultsLastGames.keys():
                        if (datetime.date(year,month,day)-datesLastGames[homeTeam]).days < 15:
                            gameSummary['resultLastGameHomeTeam']=resultsLastGames[homeTeam]
                    if awayTeam in resultsLastGames.keys():
                        if (datetime.date(year,month,day)-datesLastGames[awayTeam]).days < 15:
                            gameSummary['resultLastGameAwayTeam']=resultsLastGames[awayTeam]
                    #Extrait et enregistre le résultat du match & le résultat des derniers matchs pour les 2 équipes (pas grave si sur 2 saisons confondues car je supprime les 10 premiers matchs de la saison de chaque équipe ensuite dans l'analyse)
                    if int(gameSummary['homeTeamScore'])>int(gameSummary['awayTeamScore']):
                        result = 'winAtHome'
                        resultsLastGames[awayTeam] = 'awayLoss'
                        resultsLastGames[homeTeam] = 'homeWin'
                        lastGames[awayTeam].append(0)
                        lastGames[homeTeam].append(1)
                        lastAwayGames[awayTeam].append(0)
                        lastHomeGames[homeTeam].append(1)
                        lastOpposition[homeTeam][awayTeam] = 'homeWin'
                        lastOpposition[awayTeam][homeTeam] = 'awayLoss'
                        seasonLastOpposition[homeTeam][awayTeam] = season
                        seasonLastOpposition[awayTeam][homeTeam] = season
                    else:
                        result = 'lossAtHome'
                        resultsLastGames[awayTeam] = 'awayWin'
                        resultsLastGames[homeTeam] = 'homeLoss'
                        lastGames[awayTeam].append(1)
                        lastGames[homeTeam].append(0)
                        lastAwayGames[awayTeam].append(1)
                        lastHomeGames[homeTeam].append(0)
                        lastOpposition[homeTeam][awayTeam] = 'homeLoss'
                        lastOpposition[awayTeam][homeTeam] = 'awayWin'
                        seasonLastOpposition[homeTeam][awayTeam] = season
                        seasonLastOpposition[awayTeam][homeTeam] = season
                    gameSummary['result']=result
                    #Enregistre la date du match
                    datesLastGames[awayTeam] = datetime.date(year,month,day)
                    datesLastGames[homeTeam] = datetime.date(year,month,day)     
                    
                    games.append(gameSummary)
                print (date,'loaded')
            except NoSuchElementException:
                print ('No game on',date)
                next
                
        # copie excel        
        databaseGames = pd.DataFrame(games)
        writer = pd.ExcelWriter('NBA%s%s.xlsx'%(year,month), engine='xlsxwriter')
        databaseGames.to_excel(writer, sheet_name='Sheet1')
        writer.save()
