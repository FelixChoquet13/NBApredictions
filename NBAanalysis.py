#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:07:32 2016

@author: FelixChoquet
"""
#imports
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

def databaseSetup(excelFile):
    X = pd.read_excel(excelFile)
    teamNames = X['awayTeam'].unique()
    seasons = X['season'].unique()
    data = pd.DataFrame()
    
    ##Stats sur la saison
    #Bilans pour chaque équipe à l'extérieur, à domicile et globalement APRES chaque match
    
    for season in seasons:
        Xseason=X[X.season==season]
        for teamName in teamNames:
            Xseason['awayWin' + teamName] = Xseason.apply(lambda m : 1 if m['awayTeam']==teamName and m['result']=='lossAtHome' else 0, axis = 1)
            Xseason['awayLoss' + teamName] = Xseason.apply(lambda m : 1 if m['awayTeam']==teamName and m['result']=='winAtHome' else 0, axis = 1)   
            Xseason['homeWin' + teamName] = Xseason.apply(lambda m : 1 if m['homeTeam']==teamName and m['result']=='winAtHome' else 0, axis = 1)  
            Xseason['homeLoss' + teamName] = Xseason.apply(lambda m : 1 if m['homeTeam']==teamName and m['result']=='lossAtHome' else 0, axis = 1)
            Xseason['awayWin' + teamName] = Xseason['awayWin' + teamName].cumsum()
            Xseason['awayLoss' + teamName] = Xseason['awayLoss' + teamName].cumsum()
            Xseason['homeWin' + teamName] = Xseason['homeWin' + teamName].cumsum()
            Xseason['homeLoss' + teamName] = Xseason['homeLoss' + teamName].cumsum()
            Xseason['totalWin' + teamName] = Xseason['homeWin' + teamName]+Xseason['awayWin' + teamName]
            Xseason['totalLoss' + teamName] = Xseason['homeLoss' + teamName]+Xseason['awayLoss' + teamName]
    
        data = pd.concat([data,Xseason])
    X = data
            
    #Variables affichant 1 ou 0 en fonction du résultat du match
    X['awayWin'] = X.apply(lambda m : 1 if m['result']=='lossAtHome' else 0, axis = 1)
    X['awayLoss'] = X.apply(lambda m : 1 if m['result']=='winAtHome' else 0, axis = 1)
    X['homeWin'] = X.apply(lambda m : 1 if m['result']=='winAtHome' else 0, axis = 1)
    X['homeLoss'] = X.apply(lambda m : 1 if m['result']=='lossAtHome' else 0, axis = 1)
    
    #Bilans des deux équipes opposées sur la saison AVANT le match (globalement et pour les matchs à l'exéterieur de l'équipe visiteuse et les matchs à domicile de l'équipe recevant)
    X['totalWinsAwayTeamBeforeGame']= X.apply(lambda m: m['totalWin' + m['awayTeam']]-m['awayWin'],axis =1)
    X['totalLossAwayTeamBeforeGame']= X.apply(lambda m: m['totalLoss' + m['awayTeam']]-m['awayLoss'] ,axis =1)
    X['totalWinsHomeTeamBeforeGame']= X.apply(lambda m: m['totalWin' + m['homeTeam']]-m['homeWin']  ,axis =1)
    X['totalLossHomeTeamBeforeGame']= X.apply(lambda m: m['totalLoss' + m['homeTeam']]-m['homeLoss'] ,axis =1)
    X['totalAwayWinsAwayTeamBeforeGame']= X.apply(lambda m: m['awayWin' + m['awayTeam']]-m['awayWin']  ,axis =1)
    X['totalAwayLossAwayTeamBeforeGame']= X.apply(lambda m: m['awayLoss' + m['awayTeam']]-m['awayLoss'] ,axis =1)
    X['totalHomeWinsHomeTeamBeforeGame']= X.apply(lambda m: m['homeWin' + m['homeTeam']]-m['homeWin'] ,axis =1)
    X['totalHomeLossHomeTeamBeforeGame']= X.apply(lambda m: m['homeLoss' + m['homeTeam']]-m['homeLoss'] ,axis =1)
    X['gamesPlayedAwayTeam'] = X['totalWinsAwayTeamBeforeGame']+X['totalLossAwayTeamBeforeGame']
    X['gamesPlayedHomeTeam'] = X['totalWinsHomeTeamBeforeGame']+X['totalLossHomeTeamBeforeGame']
    
    #Bilans (en %) des deux équipes opposées sur la saison AVANT le match (globalement et pour les matchs à l'exéterieur de l'équipe visiteuse et les matchs à domicile de l'équipe recevant)
    X['percentageWinsAwayTeamBeforeGame']= X['totalWinsAwayTeamBeforeGame']/(X['totalWinsAwayTeamBeforeGame']+X['totalLossAwayTeamBeforeGame'])
    X['percentageWinsHomeTeamBeforeGame']= X['totalWinsHomeTeamBeforeGame']/(X['totalWinsHomeTeamBeforeGame']+X['totalLossHomeTeamBeforeGame'])
    X['percentageAwayWinsAwayTeamBeforeGame']= X['totalAwayWinsAwayTeamBeforeGame']/(X['totalAwayWinsAwayTeamBeforeGame']+X['totalAwayLossAwayTeamBeforeGame'])
    X['percentageHomeWinsHomeTeamBeforeGame']= X['totalHomeWinsHomeTeamBeforeGame']/(X['totalHomeWinsHomeTeamBeforeGame']+X['totalHomeLossHomeTeamBeforeGame'])
 
    
    #Supprime les matchs de playoff et les matchs pour lesquels les équipes avaient disputé moins de 10 matchs auparavant
    X.drop(list(X[X.month == 4][X.day>13].index),axis=0,inplace=True)
    X = X.reset_index(drop=True)
    X = X[X.gamesPlayedHomeTeam>=10]
    X = X[X.gamesPlayedAwayTeam>=10]
    X = X[['result','resultLastOppositionForAwayTeam','resultLastOppositionForHomeTeam','percentageWinsHomeTeam3lastHomeGamesBeforeGame','percentageWinsAwayTeam3lastAwayGamesBeforeGame','percentageWinsHomeTeam5lastGamesBeforeGame','percentageWinsAwayTeam5lastGamesBeforeGame','percentageWinsHomeTeam10lastGamesBeforeGame','percentageWinsAwayTeam10lastGamesBeforeGame','percentageHomeWinsHomeTeamBeforeGame','percentageAwayWinsAwayTeamBeforeGame','percentageWinsHomeTeamBeforeGame','percentageWinsAwayTeamBeforeGame','daysSinceLastGameHomeTeam','daysSinceLastGameAwayTeam','resultLastGameHomeTeam','resultLastGameAwayTeam']]
    writer = pd.ExcelWriter('NBACleanData.xlsx', engine='xlsxwriter')
    X.to_excel(writer, sheet_name='Sheet1')
    writer.save()


def SVC_ML(excelFile):
    X = pd.read_excel(excelFile)
    
    #Transforme les strings en code chiffré
    X.result = X.result.astype("category").cat.codes
    X.resultLastGameHomeTeam = X.resultLastGameHomeTeam.astype("category").cat.codes
    X.resultLastGameAwayTeam = X.resultLastGameAwayTeam.astype("category").cat.codes
    X.resultLastOppositionForAwayTeam = X.resultLastOppositionForAwayTeam.astype("category").cat.codes
    X.resultLastOppositionForHomeTeam = X.resultLastOppositionForHomeTeam.astype("category").cat.codes
    
    labels = X.result.copy()
    X.drop(['result'],axis=1,inplace = True)
    
    #Scale les features
    from sklearn import preprocessing
    scaled = preprocessing.StandardScaler().fit_transform(X)
    scaled = pd.DataFrame(scaled, columns=X.columns)
    X=scaled
    
    #Crée le training set et le test set
    from sklearn.cross_validation import train_test_split
    data_train, data_test, label_train, label_test = train_test_split(X, labels, test_size=0.2,random_state=7)
    
    #Implémente SVC en cherchant les meilleurs paramètres par cross validation
    best_score = 0
    best_c = 0
    best_gamma = 0
    from sklearn.metrics import accuracy_score
    from sklearn import cross_validation as cval
    from sklearn.svm import SVC
    for c in np.arange(2,3,0.5):
        for gamma in np.arange(0.001,0.003,0.001):
            score = np.mean(cval.cross_val_score(SVC(C=c,gamma=gamma), data_train, label_train, cv=10))
            print(score)
            if score > best_score:
                best_score = score
                best_c = c
                best_gamma = gamma
           
    bestModel = SVC(C=best_c,gamma=best_gamma)
    bestModel.fit(data_train, label_train) 
    predictions = bestModel.predict(data_test)
    finalScore = accuracy_score(label_test, predictions)
    print('Accuracy is',round(finalScore*100,2),'%')

def KNN_ML(excelFile):
    X = pd.read_excel(excelFile)
    
    #Transforme les strings en code chiffré
    X.result = X.result.astype("category").cat.codes
    X.resultLastGameHomeTeam = X.resultLastGameHomeTeam.astype("category").cat.codes
    X.resultLastGameAwayTeam = X.resultLastGameAwayTeam.astype("category").cat.codes
    X.resultLastOppositionForAwayTeam = X.resultLastOppositionForAwayTeam.astype("category").cat.codes
    X.resultLastOppositionForHomeTeam = X.resultLastOppositionForHomeTeam.astype("category").cat.codes
    
    labels = X.result.copy()
    X.drop(['result'],axis=1,inplace = True)
    
    #Scale les features
    from sklearn import preprocessing
    scaled = preprocessing.StandardScaler().fit_transform(X)
    scaled = pd.DataFrame(scaled, columns=X.columns)
    X=scaled
    
    #Crée le training set et le test set
    from sklearn.cross_validation import train_test_split
    data_train, data_test, label_train, label_test = train_test_split(X, labels, test_size=0.2,random_state=7)
    
    #Implémente KNN en cherchant les meilleurs paramètres par cross validation
    best_score = 0
    best_parameter = 0
    from sklearn.metrics import accuracy_score
    from sklearn import cross_validation as cval
    from sklearn.neighbors import KNeighborsClassifier
    for paramater in np.arange(21,35,1):
        score = np.mean(cval.cross_val_score(KNeighborsClassifier(n_neighbors=paramater), data_train, label_train, cv=10))
        print(score)
        if score > best_score:
            best_score = score
            best_parameter = paramater
           
    bestModel = KNeighborsClassifier(n_neighbors=best_parameter)
    bestModel.fit(data_train, label_train) 
    predictions = bestModel.predict(data_test)
    finalScore = accuracy_score(label_test, predictions)
    print('Accuracy is',round(finalScore*100,2),'%')
    
    


def RF_ML(excelFile):
    X = pd.read_excel(excelFile)
    
    #Transforme les strings en code chiffré
    X.result = X.result.astype("category").cat.codes
    X.resultLastGameHomeTeam = X.resultLastGameHomeTeam.astype("category").cat.codes
    X.resultLastGameAwayTeam = X.resultLastGameAwayTeam.astype("category").cat.codes
    X.resultLastOppositionForAwayTeam = X.resultLastOppositionForAwayTeam.astype("category").cat.codes
    X.resultLastOppositionForHomeTeam = X.resultLastOppositionForHomeTeam.astype("category").cat.codes
    
    labels = X.result.copy()
    X.drop(['result'],axis=1,inplace = True)
    
    #Scale les features
    from sklearn import preprocessing
    scaled = preprocessing.StandardScaler().fit_transform(X)
    scaled = pd.DataFrame(scaled, columns=X.columns)
    X=scaled
    
    #Crée le training set et le test set
    from sklearn.cross_validation import train_test_split
    data_train, data_test, label_train, label_test = train_test_split(X, labels, test_size=0.2,random_state=7)
    
    #Implémente Random Forest en cherchant les meilleurs paramètres par cross validation
    best_score = 0
    best_estimator = 0
    best_depth = 0
    from sklearn.metrics import accuracy_score
    from sklearn import cross_validation as cval
    from sklearn.ensemble import RandomForestClassifier
    for estimator in np.arange(15,45,3):
        for depth in np.arange(5,15,2):
            score = np.mean(cval.cross_val_score(RandomForestClassifier(n_estimators=estimator,max_depth=depth), data_train, label_train, cv=10))
            print(score)
            if score > best_score:
                best_score = score
                best_estimator = estimator
                best_depth = depth
           
    bestModel = RandomForestClassifier(n_estimators=best_estimator,max_depth=best_depth)
    bestModel.fit(data_train, label_train) 
    predictions = bestModel.predict(data_test)
    finalScore = accuracy_score(label_test, predictions)
    print('Accuracy is',round(finalScore*100,2),'%')