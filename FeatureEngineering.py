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