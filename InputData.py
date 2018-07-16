import pandas as pd

def loadDataFrameList():

    ## Loading in the datasets for all the league seasons
    df2005_2006 = pd.read_csv('Data/Premier-League-Use/Premier_2005-2006.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2006_2007 = pd.read_csv('Data/Premier-League-Use/Premier_2006-2007.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2007_2008 = pd.read_csv('Data/Premier-League-Use/Premier_2007-2008.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2008_2009 = pd.read_csv('Data/Premier-League-Use/Premier_2008-2009.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2009_2010 = pd.read_csv('Data/Premier-League-Use/Premier_2009-2010.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2010_2011 = pd.read_csv('Data/Premier-League-Use/Premier_2010-2011.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2011_2012 = pd.read_csv('Data/Premier-League-Use/Premier_2011-2012.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2012_2013 = pd.read_csv('Data/Premier-League-Use/Premier_2012-2013.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2013_2014 = pd.read_csv('Data/Premier-League-Use/Premier_2013-2014.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2014_2015 = pd.read_csv('Data/Premier-League-Use/Premier_2014-2015.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2015_2016 = pd.read_csv('Data/Premier-League-Use/Premier_2015-2016.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2016_2017 = pd.read_csv('Data/Premier-League-Use/Premier_2016-2017.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2017_2018 = pd.read_csv('Data/Premier-League-Use/Premier_2017-2018.csv' , sep=",", parse_dates=['Date'], dayfirst=True)

    ## Defining a list of dataframes for them to be concatenated together .
    DataFrames=[df2005_2006,df2006_2007,df2007_2008,df2008_2009,df2009_2010,df2010_2011,df2011_2012,df2012_2013,df2013_2014,df2014_2015,df2015_2016,df2016_2017,df2017_2018]

    return DataFrames