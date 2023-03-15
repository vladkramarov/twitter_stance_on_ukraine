# twitter_stance_on_ukraine

# 1. Running the code
- Install Python 3.10.0 or above
- Install packages shows in the requirements file

# 2. Data for Training, Testing and Validating
- Data for training, validating, and testing is located in the [dataset](dataset) folder
- Snscrape was used to gather the data

# 3. Preprocessing
- All the text preprocessing functions can be found in [preprocessor](src/preprocessor.py) module

# 4. Training a Model
- To define a model, use [model_compiler](src/training/model_compiler.py)
- To train a model, use [train_module](src/training/train_module.py)
    - Separate classes are used to train and evaluate the models shown in [class_train](src/training/class_train.py)
    - Validation and test results for each model are automatically logged to the [logs](models/logs) folder
    - Results for all models can be viewed via Tensorboard

# 5. Classifying Daily Tweets
- [daily_predictions](src/daily_predictions.py) is used to download ~10,000 tweets, classify them, and write the results to a database




