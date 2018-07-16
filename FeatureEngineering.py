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
    for i in range(0, 20):

        ## Creating a Temporary DataFrame where the team was either "Home" or "Away" .
        tempDF = DataFrame[ (DataFrame['HomeTeam'] == str(Teams[i]) ) | ( DataFrame['AwayTeam'] == str(Teams[i])) ]

        ## Creating a list which contains "Matchwise Goal Difference" for the team under observation .
        MGDList = []

        for index, row in tempDF.iterrows():
            if (row['HomeTeam'] == Teams[i]):
                MGDList.append(row['MHTGD'])
            else:
                MGDList.append(row['MATGD'])

        ## Creating a list which contains "Goal Difference" for the team under observation before coming into each match.
        GDList = []

        for j in range(0, 38):
            
            ## When the team has played no match.
            if (j == 0):
                GDList.append(0)
            
            ## When the team has played exactly one match.
            elif (j == 1):
                GDList.append(MGDList[j - 1])
            
            ## When the team has played more than 1 match.
            else:
                GDList.append(GDList[j - 1] + MGDList[j - 1])


        ## We will now normalise the Goal Difference.
        for j in range(0, 38):

            GDList[j] /= 100

        ## Creating a list for the index values of the games contained in tempDF.
        gameIndices = tempDF.index.tolist()

        ## Creating two lists which contains the index number of those games wherein the team under observation was Home or Away.

        indexHome = []
        indexAway = []

        for index, row in tempDF.iterrows():
            
            ## If team was Home Team.
            if (row['HomeTeam'] == Teams[i]):
                 indexHome.append(index)
                    
            ## If team was Away Team.
            else:
                indexAway.append(index)

        ## Appending the appropriate "Goal Difference" values to the dataframe .
        for k in range(0, 38):

            if (gameIndices[k] in indexHome):
                DataFrame['HTGD'][gameIndices[k]] = GDList[k]
            elif (gameIndices[k] in indexAway):
                DataFrame['ATGD'][gameIndices[k]] = GDList[k]