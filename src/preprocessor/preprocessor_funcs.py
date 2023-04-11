import pandas as pd
import re
import configparser
import numpy as np
from transformers import DistilBertTokenizer
import src.core as core
from typing import Tuple

MIN_TWEET_LENGTH = 2
TEXT_COLUMN = 'text'
LABEL_COLUMN = 'label'

    
def persist_string_type(dataset: pd.DataFrame, text_feature: str = TEXT_COLUMN):
    return dataset[text_feature].astype(str)

def clean_tweets(tweet: str) -> str:
    '''Removes mentions, hashtags and links'''
    tweet = re.sub(r'@[A-Za-z0-9]+|#\w+\b', '', tweet)
    tweet = re.sub(r'\bhttps?\.+\b', '', tweet)
    return tweet

def replace_flag_emojis(tweet: str) -> str:
    '''Replaces Ukrainian and russian flags with country names'''
    ukrainian_flag = "🇺🇦"
    russian_flag = "🇷🇺"
    re.sub(ukrainian_flag+"+", 'ukraine', tweet)
    re.sub(russian_flag+"+", 'russia', tweet)
    return tweet
    
def remove_emojis(tweet: str) -> str:
    '''Removes all of the emojis from the tweets'''
    ascii_characters_only = [word.encode('ascii', 'ignore').decode('ascii') for word in tweet.split()]
    return " ".join(ascii_characters_only).strip()

def drop_short_tweets(dataset: pd.DataFrame, text_feature: str = TEXT_COLUMN) -> pd.DataFrame:
    '''Removes tweets that are shorter than the minimum tweet length words'''
    tweet_length = dataset[text_feature].apply(lambda row: len(str(row).split()))
    revised_dataset = dataset.loc[tweet_length > MIN_TWEET_LENGTH]
    return revised_dataset

def distilbert_tokenizer(dataset: pd.DataFrame, text_feature: str = TEXT_COLUMN) -> Tuple[np.ndarray, np.ndarray]:
    '''Applies distilbert tokenizer on the text column. Returns input ids and attention masks'''
    checkpoint = 'distilbert-base-uncased'
    tokenizer = DistilBertTokenizer.from_pretrained(checkpoint)
    encoded = dict(tokenizer(dataset[text_feature].to_list(), return_tensors = 'np', padding='max_length', truncation=True, max_length = core.MAX_LENGTH))
    input_ids, attention_mask = encoded['input_ids'], encoded['attention_mask']
    return input_ids, attention_mask



