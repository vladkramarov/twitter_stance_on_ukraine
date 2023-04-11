import pandas as pd
import numpy as np
from transformers import TFDistilBertModel
import tensorflow as tf
import src.database_manager as dm
import src.predict.daily_tweets_obtainer as dto
from tensorflow.keras.models import load_model
import src.preprocessor.preprocessor_pipelines as pp
import src.core as core
import importlib
importlib.reload(dto)
importlib.reload(dm)
importlib.reload(core)

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
                5. Writes them to the db'''
    
    connector = dto.TweepyConnector()
    daily_tweets = dto.obtain_daily_tweets(hours_start, hours_end,connector)
    new_tweets, input_ids, attention_masks = pp.preprocess_pipeline(daily_tweets)
    new_tweets_with_labels = classify_daily_tweets(new_tweets, input_ids, attention_masks)
    dm.write_to_db(new_tweets_with_labels)

daily_tweets_classification_pipeline(hours_start=167, hours_end=6*24)
daily_tweets_classification_pipeline(hours_start=6*24, hours_end=5*24)
daily_tweets_classification_pipeline(hours_start=5*24, hours_end=4*24)
# daily_tweets_classification_pipeline(hours_start=24, hours_end=)
# backfill_tweets_with_labels = pd.read_csv('backfill_tweets.csv')
# backfill_tweets_with_labels.rename(columns={'id':'tweet_id', 'username':'author_id'}, inplace=True)
# backfill_tweets_with_labels['author_id'] =0
# tweets_to_db = backfill_tweets_with_labels[150000:]
# tweets_to_db.dropna(inplace=True)
# dm.write_to_db(tweets_to_db)
