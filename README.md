# twitter_stance_on_ukraine

# 1. Running the code
- Install Python 3.10.0 or above
- Install packages shows in the requirements file (tensorflow-macos is used because the code was written on a MacBook)


# 2. Training Data
- Data for training, validating, and testing is located in the [dataset](dataset) folder
- Code for collecting and labeling training data can be found in ... (soon to be added)
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

# 3. Preprocessing
- All the text preprocessing functions can be found in [preprocessor_funcs](src/preprocessor/preprocessor_funcs.py) module
- Preprocessing pipelines can be found in [preprocessor_pipelines](src/preprocessor/preprocessor_pipelines.py) module

# 4. Training a Model
- To define a model, use [model_compiler](src/training/model_compiler.py)
- To train a model, use [train_module](src/training/train_module.py)
    - Separate classes are used to train and evaluate the models shown in [class_train](src/training/class_train.py)
    - Validation and test results for each model are automatically logged to the [logs](models/logs) folder
    - Results for all models can be viewed via Tensorboard

# 5. Classifying Daily Tweets
- [daily_predictions](src/daily_predictions.py) is used to download ~10,000 tweets, classify them, and write the results to a database




