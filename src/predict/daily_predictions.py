import pandas as pd
import numpy as np
from transformers import TFDistilBertModel
import tensorflow as tf
import src.database_manager as dm
import src.predict.daily_tweets_obtainer as dto
import src.preprocessor.preprocessor_pipelines as pp
import src.core as core
import importlib
from tensorflow.keras.models import load_model


def classify_daily_tweets(dataset: pd.DataFrame, input_ids: np.ndarray, attention_mask: np.ndarray) -> pd.DataFrame:
    '''Loads the best model, makes predictions on the input_ids and attention_mask, and returns a DataFrame of the original tweets with classification labels'''
    tf.keras.utils.get_custom_objects().update({'TFDistilBertModel': TFDistilBertModel})
    transformer_model = load_model(core.BEST_MODEL)
    logits = transformer_model.predict([input_ids, attention_mask])
    predicted = np.argmax(logits, axis = -1)
    dataset['label'] = predicted
    return dataset

def daily_tweets_classification_pipeline(hours_start, hours_end):
    '''Pipeline that does the following: 
                1. Connects to Tweepy
                2. Obtains daily tweets
                3. Preprocesses them
                4. Classifies them
                5. Writes them to the database'''
    
    connector = dto.TweepyConnector()
    daily_tweets = dto.obtain_daily_tweets(hours_start, hours_end,connector)
    new_tweets, input_ids, attention_masks = pp.preprocess_pipeline(daily_tweets)
    new_tweets_with_labels = classify_daily_tweets(new_tweets, input_ids, attention_masks)
    dm.write_to_db(new_tweets_with_labels)




