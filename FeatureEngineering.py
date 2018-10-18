## Importing necessary libraries and modules.
import warnings
import numpy as np
import pandas as pd 
from collections import OrderedDict
from InputData import loadDataFrameList

warnings.filterwarnings('ignore')

## Loading the list of dataframes from DataPreprocessing.
DataFrames = loadDataFrameList()

'''-----------------------------------     Adding Goal Difference as a Feature  --------------------------------------------'''

## Creating a function that computes the columns "HTGD" ( Home Team Goal Difference ) and "ATGD" ( Away Team Goal Difference ) .
def computeTGD(DataFrame) :
    
    ## Initialising the values contained in the coloumns "HTGD" and "ATGD" . (Goal Difference)
    DataFrame['HTGD'] = np.nan
    DataFrame['ATGD'] = np.nan
    
    ## Creating a list of all the teams that played in that season .
    Teams = list((DataFrame).HomeTeam.unique())

    ## Creating a Temporary DataFrame which consists of the records of the matches teamwise .
    for z in range(0, 20):

        ## Creating a Temporary DataFrame where the team was either "Home" or "Away" .
        tempDF = DataFrame[ (DataFrame['HomeTeam'] == str(Teams[z]) ) | ( DataFrame['AwayTeam'] == str(Teams[z])) ]

        ## Creating a list which contains "Matchwise Goal Difference" for the team under observation .
        MGDList = []

        for index, row in tempDF.iterrows():

            if (Teams[z] == row['HomeTeam']):
                MGDList.append(row['MHTGD'])

            elif (Teams[z] == row['AwayTeam']):
                MGDList.append(row['MATGD'])

        ## Creating a list which contains "Goal Difference" for the team under observation before coming into each match.
        GDList = []

        for i in range(0, 38):
            
            ## When the team has played no match.
            if (i == 0):
                GDList.append(0)
            
            ## When the team has played exactly one match.
            elif (i == 1):
                GDList.append(MGDList[i - 1])
            
            ## When the team has played more than 1 match.
            else:
                GDList.append(GDList[i - 1] + MGDList[i - 1])


        ## We will now normalise the Goal Difference.
        for m in range(0, 38):

            GDList[m] /= 100

        ## Creating a list for the index values of the games contained in tempDF.
        gameIndices = tempDF.index.tolist()

        ## Creating two lists which contains the index number of those games wherein the team under observation was Home or Away.

        indexHome = []
        indexAway = []

        for index, row in tempDF.iterrows():
            
            ## If team was Home Team.
            if (Teams[z] == row['HomeTeam']):
                 indexHome.append(index)
                    
            ## If team was Away Team.
            elif (Teams[z] == row['AwayTeam']):
                indexAway.append(index)

        ## Appending the appropriate "Goal Difference" values to the dataframe .
        for j in range(0, 38):

            if (gameIndices[j] in indexHome):
                DataFrame['HTGD'][gameIndices[j]] = GDList[j]
            elif (gameIndices[j] in indexAway):
                DataFrame['ATGD'][gameIndices[j]] = GDList[j]

    ## Filling in the coloumns for "GD".
    DataFrame['GD'] = DataFrame.apply(lambda row: row['HTGD'] - row['ATGD'], axis = 1)


''''-----------------------------------     Adding KPP as a Feature  --------------------------------------------'''

## Creating a function which computes the KPP (K-Past Performance) feature for Goals, Corners and Shots on Target.

def computeKPP(DataFrame, slidingWindowParameter):
    
    ## Set slidingWindowParameter to k.
    k = slidingWindowParameter

    ## Creating a list of all the teams that played in that season.
    Teams = list((DataFrame).HomeTeam.unique())
    
    ## Initialising the values contained in the coloumns "HGKPP , HCKPP , HSTKPP" and "AGKPP , ACKPP , ASTKPP". (KPP Features).
    DataFrame['HGKPP'] = np.nan
    DataFrame['AGKPP'] = np.nan
    DataFrame['HCKPP'] = np.nan
    DataFrame['ACKPP'] = np.nan
    DataFrame['HSTKPP'] = np.nan
    DataFrame['ASTKPP'] = np.nan
    
    ## Creating a Temporary DataFrame which consists of the records of the matches teamwise.
    for z in range(0, 20):

        ## Creating a Temporary DataFrame where the team was either "Home" or "Away" .
        tempDF = DataFrame[(DataFrame['HomeTeam'] == str(Teams[z])) | ( DataFrame['AwayTeam'] == str(Teams[z]))]

        ## Creating a list which contains Goals, Corners and Number of Shots on Target for the team under observation match-wise.
        Goals = []
        Corners = []
        shotsonTarget = []

        for index, row in tempDF.iterrows():
    
            if (Teams[z] == row['HomeTeam']):
                Goals.append(float(row['FTHG']))
                Corners.append(float(row['HC']))
                shotsonTarget.append(float(row['HST']))

            elif (Teams[z] == row['AwayTeam']):
                Goals.append(float(row['FTAG']))
                Corners.append(float(row['AC']))
                shotsonTarget.append(float(row['AST']))

        ## Creating lists to hold values for the corresponding KPP Features.
        # Since these features will be non existent for the first k matches of each team, fill Nan for the first k values.
        goalsKPP = [np.nan] * k
        cornersKPP = [np.nan] * k
        shotsOnTargetKPP = [np.nan] * k
        
        ## Adding appropriate values to the list.
        ## The number of computations performed will be (n + 1 - k) where :
        ## n = number of matches in the season for each team (38).
        ## k = sliding window hyper-parameter.
        for i in range(0, (39 - k)):

            ## Obtaining the slice of records to be observed.
            ## Sum the slice of records and normalize it by k.
            goalSliceSum = sum(Goals[i : (i + k)])/k
            cornerSliceSum = sum(Corners[i : (i + k)])/k
            shotsOnTargetSliceSum = sum(shotsonTarget[i : (i + k)])/k

            ## Appending to the list of the corresponding KPP features.
            goalsKPP.append(goalSliceSum)
            cornersKPP.append(cornerSliceSum)
            shotsOnTargetKPP.append(shotsOnTargetSliceSum)
            
        ## Creating a list for the index values of the games contained in the tempDF.
        gameIndices = tempDF.index.tolist()

        ## Creating two lists which contains the index number of those games wherein the team under observation was Home or Away.
        indexHome = []
        indexAway = []

        ## Segregate home and away match indices.
        for index, row in tempDF.iterrows():
            
            if (Teams[z] == row['HomeTeam']):
                 indexHome.append(index)

            elif (Teams[z] == row['AwayTeam']):
                indexAway.append(index)

        ## Appending the appropriate "KPP" values to the dataframe.
        for j in range(0, 38):

            if (gameIndices[j] in indexHome):
                DataFrame['HGKPP'][gameIndices[j]] = goalsKPP[j]
                DataFrame['HCKPP'][gameIndices[j]] = cornersKPP[j]
                DataFrame['HSTKPP'][gameIndices[j]] = shotsOnTargetKPP[j]

            elif (gameIndices[j] in indexAway):
                DataFrame['AGKPP'][gameIndices[j]] = goalsKPP[j]
                DataFrame['ACKPP'][gameIndices[j]] = cornersKPP[j]
                DataFrame['ASTKPP'][gameIndices[j]] = shotsOnTargetKPP[j]
        
    
    ## Filling in the coloumns for "GKPP, CKPP, STKPP".
    DataFrame['GKPP'] = DataFrame.apply(lambda row: row['HGKPP'] - row['AGKPP'], axis = 1)
    DataFrame['CKPP'] = DataFrame.apply(lambda row: row['HCKPP'] - row['ACKPP'], axis = 1)
    DataFrame['STKPP'] = DataFrame.apply(lambda row: row['HSTKPP'] - row['ASTKPP'], axis = 1)


''''-----------------------------------     Adding Streak and Weighted Streak as a Feature  --------------------------------------------'''

## Creating a function which computes the Streak and Weighted Streak.

def computeStreak(DataFrame, slidingWindowParameter):
    
    ## Set slidingWindowParameter to k.
    k = slidingWindowParameter

    ## Creating a list of all the teams that played in that season.
    Teams = list((DataFrame).HomeTeam.unique())
    
    ## Initialsing the values in the coloumns "HSt, ASt , HStWeigted , AStWeigted".
    DataFrame['HSt'] = np.nan
    DataFrame['ASt'] = np.nan
    DataFrame['HStWeighted'] = np.nan
    DataFrame['AStWeighted'] = np.nan
    
    ## Creating a Temporary DataFrame which consists of the records of the matches teamwise.
    for z in range(0, 20):

        ## Creating a Temporary DataFrame where the team was either "Home" or "Away" .
        tempDF = DataFrame[(DataFrame['HomeTeam'] == str(Teams[z])) | ( DataFrame['AwayTeam'] == str(Teams[z]))]
    
        ## Creating a list which contains the points assigned to each team after their match. 
        ## 0 - Loss
        ## 1 - Draw
        ## 3 - Win
        matchPoints = []

        ## Creating a list which contains the weights assigned to each match according to the sliding window hyper-parameter.
        ## The weighting scheme is such that the first match in the window will be a assigned a weight of 1 and the last match will be 
        ## assigned a weight of k.
        weightList = [(i + 1) for i in range(0, k)]
        
        for index , row in tempDF.iterrows():
            
            if (Teams[z] == row['HomeTeam']):
                if (row['FTR'] == 'A') :
                    matchPoints.append(0.0)
                elif (row['FTR'] == 'D') :
                    matchPoints.append(1.0)
                elif (row['FTR'] == 'H') :
                    matchPoints.append(3.0)

            elif (Teams[z] == row['AwayTeam']):
                if (row['FTR'] == 'H') :
                    matchPoints.append(0.0)
                elif (row['FTR'] == 'D') :
                    matchPoints.append(1.0)
                elif (row['FTR'] == 'A') :
                    matchPoints.append(3.0)
        
        ## Creating lists to hold values for the corresponding Streak and Weighted Streak Features.
        ## Since these features will be non existent for the first k matches of each team, fill Nan for the first k values.
        streak = [np.nan] * k
        weightedStreak = [np.nan] * k
        
        ## Adding appropriate values to the list.
        ## The number of computations performed will be (n + 1 - k) where :
        ## n = number of matches in the season for each team (38).
        ## k = sliding window hyper-parameter.
        for i in range(0, (39 - k)):

            ## Obtaining the slice of records to be observed.
            matchPointsSlice = matchPoints[i : (i + k)]

            ## Sum the slice of records and normalize it by 3k.
            streakValue = sum(matchPointsSlice)/(3 * k)

            ## Multiply the slice by the weights.
            ## Sum the slice of records and normalize it by (3k(k+1))/2.
            weightedStreakValue = sum(list(np.array(matchPointsSlice) * np.array(weightList)))/((1.5) * k * (k + 1))

            ## Appending to the list of the corresponding features.
            streak.append(streakValue)
            weightedStreak.append(weightedStreakValue)
            
        ## Creating a list for the index values of the games contained in the tempDF.
        gameIndices = tempDF.index.tolist()

        ## Creating two lists which contains the index number of those games wherein the team under observation was Home or Away.
        indexHome = []
        indexAway = []

        ## Segregate home and away match indices.
        for index, row in tempDF.iterrows():

            if (Teams[z] == row['HomeTeam']):
                 indexHome.append(index)

            elif (Teams[z] == row['AwayTeam']):
                indexAway.append(index)

        ## Appending the appropriate "KPP" values to the dataframe.
        for j in range(0, 38):

            if (gameIndices[j] in indexHome):
                DataFrame['HSt'][gameIndices[j]] = streak[j]
                DataFrame['HStWeighted'][gameIndices[j]] = weightedStreak[j]

            elif (gameIndices[j] in indexAway):
                DataFrame['ASt'][gameIndices[j]] = streak[j]
                DataFrame['AStWeighted'][gameIndices[j]] = weightedStreak[j]
                
    
    ## Filling in the coloumns for "Streak and WeightedStreak".
    DataFrame['Streak'] = DataFrame.apply(lambda row: row['HSt'] - row['ASt'], axis = 1)
    DataFrame['WeightedStreak'] = DataFrame.apply(lambda row: row['HStWeighted'] - row['AStWeighted'], axis = 1)

''''-----------------------------------     Adding Form as a Feature  --------------------------------------------'''

## Creating a function which computes the Form.

def computeForm(DataFrame, stealingFraction):
    
    ## Hyper-Parameter k.
    k = stealingFraction

    ## Initialising the values contained in the coloumns "HForm" and "AForm".
    DataFrame['HForm'] = 1.0
    DataFrame['AForm'] = 1.0

    ## Creating a global form dictionary with keys as team names and value as list of form.
    gFormDict = {}

    ## Creating a global form dictionary with keys as team names and value as list of match indices.
    teamMatchLookup = {}

    ## Dictionary which keeps track of a team's match indices.
    matchCounterDict = {}

    ## Creating a list of all the teams that played in that season .
    Teams = list((dataFrame).HomeTeam.unique())

    for teamName in Teams :

        ## Initialising values.
        gFormDict[teamName] = 1.0
        matchCounterDict[teamName] = 0

        ## For each team playing in the season, create a temporary dataframe to record the match numbers of each team.
        ## Create a temporary dataframe for the team under consideration.
        tempDF = DataFrame[(DataFrame['HomeTeam'] == str(teamName)) | ( DataFrame['AwayTeam'] == str(teamName))]

        ## Assigning match indices list to the relevant team.
        teamMatchLookup[teamName] =  tempDF.index.tolist()

    ## Iterating over each match in the season.
    for index, row in DataFrame.iterrows():
        
        ## Exit condition. Since the last update in the form values will be in the 2nd last match for each team, we have to run the loop till each team's 2nd last match.
        ## This condition happens at the 370th in each season.
        if (index == 370):
        
            break

        ## Update match counter for the playing teams.
        matchCounterDict[row['HomeTeam']] += 1
        matchCounterDict[row['AwayTeam']] += 1

        ## Case where home team wins. Since the home team wins here, a positive update is given to the home team and a negative update is given to the away team.        
        if (row['FTR'] == 'H'):

            ## Form values of the teams before coming into the match.
            prevHomeForm = gFormDict[row['HomeTeam']]
            prevAwayForm = gFormDict[row['AwayTeam']]

            ## Next match index of the Home and Away Team.
            nextMatchH = teamMatchLookup[row['HomeTeam']][matchCounterDict[row['HomeTeam']]]
            nextMatchA = teamMatchLookup[row['AwayTeam']][matchCounterDict[row['AwayTeam']]]
    
            ## Since the home team wins here, a positive update is given to the home team and a negative update is given to the away team. 
            homeUpdate = gFormDict[row['HomeTeam']] + k * gFormDict[row['AwayTeam']]
            awayUpdate = gFormDict[row['AwayTeam']] - k * gFormDict[row['AwayTeam']]

            ## Selecting next match record for the current Home Team.
            matchInfoH = DataFrame.iloc[[nextMatchH]]

            ## Check whether current Home Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoH['HomeTeam'][nextMatchH] == row['HomeTeam']):
                DataFrame.loc[nextMatchH, 'HForm'] = homeUpdate

            elif (matchInfoH['AwayTeam'][nextMatchH] == row['HomeTeam']):
                DataFrame.loc[nextMatchH, 'AForm'] = homeUpdate

            ## Update value in the dictionary.
            gFormDict[row['HomeTeam']] = homeUpdate

            ## Selecting next match record for the current Away Team.
            matchInfoA = DataFrame.iloc[[nextMatchA]]

            ## Check whether current Away Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoA['HomeTeam'][nextMatchA] == row['AwayTeam']):
                DataFrame.loc[nextMatchA, 'HForm'] = awayUpdate

            elif (matchInfoA['AwayTeam'][nextMatchA] == row['AwayTeam']):
                DataFrame.loc[nextMatchA, 'AForm'] = awayUpdate

            ## Update value in the dictionary.
            gFormDict[row['AwayTeam']] = awayUpdate


        ## Case where away team wins. Since the away team wins here, a positive update is given to the away team and a negative update is given to the home team.        
        if (row['FTR'] == 'A'):

            ## Form values of the teams before coming into the match.
            prevHomeForm = gFormDict[row['HomeTeam']]
            prevAwayForm = gFormDict[row['AwayTeam']]
        
            ## Next match index of the Home and Away Team.
            nextMatchH = teamMatchLookup[row['HomeTeam']][matchCounterDict[row['HomeTeam']]]
            nextMatchA = teamMatchLookup[row['AwayTeam']][matchCounterDict[row['AwayTeam']]]

            ## Since the away team wins here, a positive update is given to the away team and a negative update is given to the home team.        
            homeUpdate = gFormDict[row['HomeTeam']] - k * gFormDict[row['HomeTeam']]
            awayUpdate = gFormDict[row['AwayTeam']] + k * gFormDict[row['HomeTeam']]

            ## Selecting next match for the current Home Team.
            matchInfoH = DataFrame.iloc[[nextMatchH]]

            ## Check whether current Home Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoH['HomeTeam'][nextMatchH] == row['HomeTeam']):
                DataFrame.loc[nextMatchH, 'HForm'] = homeUpdate

            elif (matchInfoH['AwayTeam'][nextMatchH] == row['HomeTeam']):
                DataFrame.loc[nextMatchH, 'AForm'] = homeUpdate

            ## Update value in the dictionary.
            gFormDict[row['HomeTeam']] = homeUpdate

            ## Selecting next match for the current Away Team.
            matchInfoA = DataFrame.iloc[[nextMatchA]]

            ## Check whether current Away Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoA['HomeTeam'][nextMatchA] == row['AwayTeam']):            
                DataFrame.loc[nextMatchA, 'HForm'] = awayUpdate

            elif (matchInfoA['AwayTeam'][nextMatchA] == row['AwayTeam']):
                DataFrame.loc[nextMatchA, 'AForm'] = awayUpdate

            ## Update value in the dictionary.
            gFormDict[row['AwayTeam']] = awayUpdate

        ## Case where a draw occurs.
        if (row['FTR'] == 'D'):

            # Form values of the teams before coming into the match.
            prevHomeForm = gFormDict[row['HomeTeam']]
            prevAwayForm = gFormDict[row['AwayTeam']]
    
            ## Next match index of the Home and Away Team.
            nextMatchH = teamMatchLookup[row['HomeTeam']][matchCounterDict[row['HomeTeam']]]
            nextMatchA = teamMatchLookup[row['AwayTeam']][matchCounterDict[row['AwayTeam']]]

            ## Form Updates.
            homeUpdate = gFormDict[row['HomeTeam']] - k * ((gFormDict[row['HomeTeam']]) - (gFormDict[row['AwayTeam']]))
            awayUpdate = gFormDict[row['AwayTeam']] - k * ((gFormDict[row['AwayTeam']]) - (gFormDict[row['HomeTeam']]))

            ## Selecting next match for the current Home Team.
            matchInfoH = DataFrame.iloc[[nextMatchH]]

            ## Check whether current Home Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoH['HomeTeam'][nextMatchH] == row['HomeTeam']):
                DataFrame.loc[nextMatchH, 'HForm'] = homeUpdate

            elif (matchInfoH['AwayTeam'][nextMatchH] == row['HomeTeam']):
                DataFrame.loc[nextMatchH, 'AForm'] = homeUpdate

            ## Update value in the dictionary.
            gFormDict[row['HomeTeam']] = homeUpdate

            ## Selecting next match for the current Away Team.
            matchInfoA = DataFrame.iloc[[nextMatchA]]

            ## Check whether current Away Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoA['HomeTeam'][nextMatchA] == row['AwayTeam']):
                DataFrame.loc[nextMatchA, 'HForm'] = awayUpdate

            elif (matchInfoA['AwayTeam'][nextMatchA] == row['AwayTeam']):
                DataFrame.loc[nextMatchA, 'AForm'] = awayUpdate

            ## Update value in the dictionary.
            gFormDict[row['AwayTeam']] = awayUpdate
    
    # Filling in the coloumns for "Form".
    DataFrame['Form'] = DataFrame.apply(lambda row: row['HForm'] - row['AForm'], axis = 1)


## Computing features for all the data.
for i, dataFrame in enumerate(DataFrames):

    ## List of features who's initial values are Nan.
    nanFeatures = ['GKPP', 'HGKPP', 'AGKPP', 'CKPP', 'HCKPP', 'ACKPP', 'STKPP', 'HSTKPP', 'ASTKPP', 'Streak', 'HSt', 'ASt', 'WeightedStreak', 'HStWeighted', 'AStWeighted']
    
    dataFrame['MHTGD'] = dataFrame.apply(lambda row: row['FTHG'] - row['FTAG'], axis = 1)
    dataFrame['MATGD'] = dataFrame.apply(lambda row: row['FTAG'] - row['FTHG'], axis = 1)
    
    ## Computing the features.
    computeTGD(dataFrame)
    computeKPP(dataFrame, 6)
    computeStreak(dataFrame, 6)
    computeForm(dataFrame, 0.33)
    
    ## Dropping all rows containing Nan values for the above feature list.
    dataFrame = dataFrame.dropna(subset = nanFeatures)
    
    print(i)

## Concatening all the dataframes together.
DataFrame = pd.concat(DataFrames)

## Saving the newly engineered dataset.
DataFrame.to_csv('./EngineeredData.csv', sep = ',', index = False)