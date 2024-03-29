# Predictive analysis and modelling football results using machine learning approach for English Premier League

Code for the paper <a href = "https://www.sciencedirect.com/science/article/pii/S0169207018300116"> Predictive analysis and modelling football results using machine learning approach for English Premier League </a>.
<br>
<br>
Alternate Paper Link : <a href = "https://drive.google.com/open?id=1oX0j4os_6Yepj1ZwMgl9pm3X7Ml6COq9"> Alternate Paper Link </a>

## Abstract

The introduction of artificial intelligence has given us the ability to build predictive systems with unprecedented accuracy. Machine learning is being used in virtually all areas in one way or another, due to its extreme effectiveness. One such area where predictive systems have gained a lot of popularity is the prediction of football match results. This paper demonstrates our work on the building of a generalized predictive model for predicting the results of the English Premier League. Using feature engineering and exploratory data analysis, we create a feature set for determining the most important factors for predicting the results of a football match, and consequently create a highly accurate predictive system using machine learning. We demonstrate the strong dependence of our models’ performances on important features. Our best model using gradient boosting achieved a performance of 0.2156 on the ranked probability score (RPS) metric for game weeks 6 to 38 for the English Premier League aggregated over two seasons (2014–2015 and 2015–2016), whereas the betting organizations that we consider (Bet365 and Pinnacle Sports) obtained an RPS value of 0.2012 for the same period. Since a lower RPS value represents a higher predictive accuracy, our model was not able to outperform the bookmaker’s predictions, despite obtaining promising results.

## Instructions to Run

**1. Clone the repository**
      
      $ git clone https://github.com/RahulBaboota/Predicting-English-Premier-Results.git
      $ cd Predicting-English-Premier-Results
      
**2. Create new virtual environment**

      $ sudo pip install virtualenv
      $ virtualenv venv
      $ source venv/bin/activate
      $ pip install -r requirements.txt
      
**3. Repository Information**

<ul>
      <li> The folder <b>Data</b> contains the raw data collected from <a href = 'https://www.bbc.com/sport/football'> Football UK </a>. </li>
      <br>
      <li> The folder <b>GridSearch</b> contains the pickled grid search objects for the machine learning models. </li>
      <br>
      <li> The folder <b>Scraper.py</b> contains the code for scraping the FIFA Ratings for the teams. (The scraper might be redundant now if the website layout has changed since). as well as the scraped data.</li>
      <br>
      <li> The file <b>FeatureEngineering.py</b> contains the code for creating the features from the raw data. </li>
      <br>
      <li> The file <b>TrainTestSplit.py</b> contains the code for splitting up the data into a training and testing split as well as creating the subsets <i>A</i> and <i>B</i> as mentioned in the paper. </li>
      <br>
       <li> The jupyter notebooks are for the different models on both subsets <i>A</i> as well as <i>B</i>.
             
## Results

<img src="https://github.com/RahulBaboota/Predicting-English-Premier-Results/blob/master/Images/AllModelsBar.jpeg">
<img src="https://github.com/RahulBaboota/Predicting-English-Premier-Results/blob/master/Images/RPS.jpeg">
