## Importing necessary libraries and modules.
import warnings
import pandas as pd
from InputData import loadDataFrameList

warnings.filterwarnings('ignore')

def trainTestSplit(Set):

	DataFrame = pd.read_csv('./EngineeredData.csv', delimiter = ',')

	## Removing unwanted fields firstly.
	## Creating a list of betting odds column fields.
	bettingStats = ["B365H","B365D","B365A","BWH","BWD","BWA","GBH","GBD","GBA","IWH","IWD","IWA","LBH","LBD","LBA","SBH","SBD","SBA","WHH","WHD","WHA","SJH","SJD","SJA","VCH","VCD","VCA","Bb1X2","BbMxH","BbAvH","BbMxD","BbAvD","BbMxA","BbAvA","BbOU","BbMx>2.5","BbAv>2.5","BbMx<2.5","BbAv<2.5","BbAH","BbAHh","BbMxAHH","BbAvAHH","BbMxAHA","BbAvAHA"]
	bettingStatsEx = ["BSH", "BSD", "BSA", "PSA", "PSH", "PSD", "PSCA", "PSCD", "PSCH"]

	## Creating a list of general unnecesaary column fields.
	genDropInfo = ["Div", "Date", "HomeTeam", "AwayTeam", "Referee"]

	## Creating a list of unnecessary pre-existing feature columns.
	preDropFeatures = ["FTHG", "FTAG", "HTHG", "HTAG", "HS", "AS", "HST", "AST", "HTR", "HS", "AS", "HF", "AF", "HY", "AY", "HR", "AR", "HC", "AC", "MHTGD", "MATGD"]

	## Dropping the above coloumns .
	DataFrame.drop(bettingStats + bettingStatsEx + genDropInfo + preDropFeatures, axis = 1, inplace = True)

	## List of features who's initial values are Nan.
	nanFeatures = ['GKPP', 'HGKPP', 'AGKPP', 'CKPP', 'HCKPP', 'ACKPP', 'STKPP', 'HSTKPP', 'ASTKPP', 'Streak', 'HSt', 'ASt', 'WeightedStreak', 'HStWeighted', 'AStWeighted']

	## Getting a list of the unique seasons.
	seasonNames = list(DataFrame.Season.unique())
	dataFramesList = []

	for season in seasonNames:
	    
	    ## Creating a Temporary DataFrame season-wise.
	    tempDF = DataFrame[ (DataFrame['Season'] == (season) )]
	    tempDF = tempDF.dropna(subset = nanFeatures)
	    dataFramesList.append(tempDF)

	DataFrame = pd.concat(dataFramesList)  

	## Splitting the data into Training and Testing splits.
	## For our "Target Variable" , we need the match outcomes which is the field "FTR" (Full Time Result) .
	## So , we will create a slice of this coloumn as well as "Season" (for indexing purposes) .
	Y = DataFrame[['FTR','Season']]

	## Now , we will choose the first 11 seasons as our Training Set and the final 2 as Testing Set .
	YTrain = Y[ (Y['Season'] == '2005-2006') | (Y['Season'] == '2006-2007') | (Y['Season'] == '2007-2008') | (Y['Season'] == '2008-2009') | (Y['Season'] == '2009-2010') | (Y['Season'] == '2010-2011') | (Y['Season'] == '2011-2012') | (Y['Season'] == '2012-2013') | (Y['Season'] == '2013-2014') | (Y['Season'] == '2014-2015') | (Y['Season'] == '2015-2016')]         
	YTest = Y[ (Y['Season'] == '2016-2017') | (Y['Season'] == '2017-2018')]

	## Now , we dont need the "Season" coloumn so drop it .
	YTrain.drop(['Season'], axis = 1, inplace = True)
	YTest.drop(['Season'], axis = 1, inplace = True)

	## Now, for creating the feature set, we first need to remove the target variable from the DataFrame .
	X = DataFrame
	X.drop(['FTR'], axis = 1, inplace = True)

	## Now , we will choose the first 11 seasons as our Training Set and the final 2 as Testing Set .
	XTrain = X[ (X['Season'] == '2005-2006') | (X['Season'] == '2006-2007') | (X['Season'] == '2007-2008') | (X['Season'] == '2008-2009') | (X['Season'] == '2009-2010') | (X['Season'] == '2010-2011') | (X['Season'] == '2011-2012') | (X['Season'] == '2012-2013') | (X['Season'] == '2013-2014') | (X['Season'] == '2014-2015') | (X['Season'] == '2015-2016')] 
	XTest = X[ (X['Season'] == '2016-2017') | (X['Season'] == '2017-2018')]

	## Now , we dont need the "Season" coloumn so drop it .
	XTrain.drop(['Season'], axis = 1, inplace = True)
	XTest.drop(['Season'], axis = 1, inplace = True)

	## Splitting the feature set into the appropriate set.
	if (Set == 'A'):

		## The set of features to be added in Set A i.e. the non-differential features.
		nonDifferentialFeatures = ["ATGD", "HTGD", "ACKPP", "HCKPP", "AGKPP", "HGKPP", "ASTKPP", "HSTKPP", "ASt", "HSt", "AStWeighted", "HStWeighted", "AForm", "HForm", "AOverall", "HOverall", "AAttack", "HAttack", "AMidfield", "HMidfield", "ADefense", "HDefense"]

		## Choosing the above feature set.
		XTrainA = XTrain[nonDifferentialFeatures]
		XTestA = XTest[nonDifferentialFeatures]

		return XTrainA, XTestA, YTrain, YTest

	if (Set == 'B'):

		## The set of features to be added in Set B i.e. the differential features.
		differentialFeatures = ["GD", "CKPP", "GKPP", "STKPP", "Streak", "WeightedStreak", "Form", "Overall", "Attack", "Midfield", "Defense"]

		## Choosing the above feature set.
		XTrainB = XTrain[differentialFeatures]
		XTestB = XTest[differentialFeatures]

		return XTrainB, XTestB, YTrain, YTest