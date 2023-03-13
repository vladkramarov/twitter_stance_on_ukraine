import pandas as pd
import numpy as np
from transformers import TFDistilBertModel
import tensorflow as tf
import src.database_manager as dm
import src.daily_tweets_obtainer as dto
from tensorflow.keras.models import load_model
import src.preprocessor as pp
import src.core as core
import importlib
importlib.reload(dto)
importlib.reload(dm)

def classify_daily_tweets(dataset: pd.DataFrame, input_ids: np.ndarray, attention_mask: np.ndarray) -> pd.DataFrame:
    '''Loads the best model, makes predictions on the input_ids and attention_mask, and returns a DataFrame of the original tweets with classification labels'''
    tf.keras.utils.get_custom_objects().update({'TFDistilBertModel': TFDistilBertModel})
    transformer_model = load_model(core.BEST_MODEL)
    logits = transformer_model.predict([input_ids, attention_mask])
    predicted = np.argmax(logits, axis = -1)
    dataset['label'] = predicted
    return dataset

def daily_tweets_classification_pipeline():
    '''Pipeline that does the following: 
                1. Connects to Tweepy
                2. Obtains daily tweets
                3. Preprocesses them
                4. Classifies them
                5. Writes them to the db'''
    connector = dto.TweepyConnector()
    daily_tweets = dto.obtain_daily_tweets(connector)
    new_tweets, input_ids, attention_masks = pp.preprocess_pipeline(daily_tweets)
    new_tweets_with_labels = classify_daily_tweets(new_tweets, input_ids, attention_masks)
    dm.write_to_db(new_tweets_with_labels)
    
g = daily_tweets_classification_pipeline()


