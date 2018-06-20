import pandas as pd
# from FeatureEngineering import Feature_Engineering

## DataFrame returned after applying feature engineering on them .
DataFrame = pd.read_csv('Data/Premier-League-Use/EngineeredData_s_.csv' , sep=',' )

# DataFrame = Feature_Engineering()


## Defining a function to  remove the undesired information .
def Clean_DataFrame(DataFrame):

    ## Defining the coloumn labels to be dropped ( This includes all the betting statistics ) .
    Dropped_coloumns_headings = ["B365H","B365D","B365A","BWH","BWD","BWA","GBH","GBD","GBA","IWH","IWD","IWA","LBH","LBD","LBA","SBH","SBD","SBA","WHH","WHD","WHA","SJH","SJD","SJA","VCH","VCD","VCA","BSH","BSD","BSA","Bb1X2","BbMxH","BbAvH","BbMxD","BbAvD","BbMxA","BbAvA","BbOU","BbMx>2.5","BbAv>2.5","BbMx<2.5","BbAv<2.5","BbAH","BbAHh","BbMxAHH","BbAvAHH","BbMxAHA","BbAvAHA","PSA","PSH","PSD"]

    ## Dropping the above coloumns .
    DataFrame.drop(Dropped_coloumns_headings, axis=1, inplace=True)
    # DataFrame.describe()

    return DataFrame

## Defining the Cleaned and Concatenated DataFrame .
DataFrame = Clean_DataFrame(DataFrames)

# def DataPreprocessing() :
#     return DataFrame

DataFrame.to_csv('Data/Premier-League-Use/CleanedData_s_.csv', sep=',')
