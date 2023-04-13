# twitter_stance_on_ukraine

## Overview
In this project, Twitter's stance towards the war in Ukraine is determined using Distlbert transformer with a shallow NN.
- Approximately 10K tweets that mention Ukraine are classified daily
- Aggregated results are shown in a Dash app, deployed on Elastic Beanstalk


## 1. Running the code
- Install Python 3.10.0 or above
- Required packages for the **whole repo are in** [requirements_full](requirements_full.txt)
- [requirements](requirements.txt) is for **deployment purposes only**

## 2. Training Data
- Data for training, validating, and testing is located in the [dataset](dataset) folder
- Code for collecting and labeling training data can be found in [training_data_obtainer](src/training_data_obtainer.py)
    - Note that snscraper library stopped working on Macs, so Google Colab was used to scrape the tweets
- Tweets were collected using the following 3 methods:
- Search by user:
    - E.g. since Donald Trump Junior only critisizes all the help given to Ukraine, his tweets that mention Ukraine are automatically labeled as negative
    - Likewise, tweets by Timothy Snyder that mention Ukraine are automatically labeled as positive
    - Tweets from neutral news channels (e.g. AP News, Reuters) that mention Ukraine are automatically labeled as neutral
- Search by keywords:
    - Combinations of keywords that will most likely end up in a *positive* tweet towards Ukraine. E.g. - "ukraine will win", "putin is a terrorist", etc.
    - Combinations of keywords that will most likely end up in a *negative* tweet towards Ukraine. E.g. - "puppet government in ukraine", "azov neo-nazi", etc.
- Search by hashtags:
    - Similar to a keyword search. Used hashtags that would most likely end up in a strongly positive/strongly negative tweet.
- Train data size ~33,000 tweets, validation and test data are ~11,000 tweets each

## 3. Preprocessing
- All the text preprocessing functions can be found in [preprocessor_funcs](src/preprocessor/preprocessor_funcs.py) module
- Preprocessing pipelines can be found in [preprocessor_pipelines](src/preprocessor/preprocessor_pipelines.py) module

## 4. Training a Model
- To define a model, use [model_compiler](src/training/model_compiler.py)
    - DistilBert Transformer with a shallow neural nets were trained and evaluated
- To train a model, use [train_module](src/training/train_module.py)
    - Separate classes are used to train and evaluate the models shown in [class_train](src/training/class_train.py)
    - To train the latest model, run [train_module](src/training/train_module.py) module
    - Validation and test results for each model are automatically logged to the [logs](models/logs) folder
    - Results for all models can be viewed via Tensorboard

## 5. Classifying Daily Tweets
- [daily_predictions](src/predict/daily_predictions.py) is used to download ~10,000 tweets, classify them, and write the results to a PostgreSQL DB hosted on AWS RDS

## 6. Deployment
- An interactive Dash app is used to visualize the results. The main chart for the Dash app is created in Plotly [plotly_chart_components](src/deployment/plotly_chart_components.py)
- SQL query used to generate data for Dash app can be found in [generate_chart_data](src/deployment/generate_chart_data.py)
- All the Dash app components are in [dash_components](src/deployment/dash_components.py)
- The actual app is deployed on Elastic Beanstalk. AWS Codepipeline is used for CI/CD. The code to the app is in [application](application.py); the actual app can be found [here](http://twitterukraine-env.eba-ybme3mms.us-east-1.elasticbeanstalk.com/)


## 7. Issues
- Very high latency, when updating the main chart. Every callback queries new dataset from the DB, and it is slow. Please be patient for now :)
- The app is made for computer screens, no mobile version (yet?)

