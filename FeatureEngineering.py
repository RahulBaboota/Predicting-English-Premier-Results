## Importing necessary libraries and modules.
import numpy as np
from collections import OrderedDict
from InputData import loadDataFrameList

## Loading the list of dataframes from DataPreprocessing
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
        
        print 'Computing KPP ', Teams[z] , z 
    
    ## Filling in the coloumns for "GKPP, CKPP, STKPP".
    DataFrame['GKPP'] = DataFrame.apply(lambda row: row['HGKPP'] - row['AGKPP'], axis = 1)
    DataFrame['CKPP'] = DataFrame.apply(lambda row: row['HCKPP'] - row['ACKPP'], axis = 1)
    DataFrame['STKPP'] = DataFrame.apply(lambda row: row['HSTKPP'] - row['ASTKPP'], axis = 1)