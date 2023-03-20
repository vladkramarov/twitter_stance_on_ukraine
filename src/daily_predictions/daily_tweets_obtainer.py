import pandas as pd
import tweepy
import configparser
from datetime import datetime, timedelta, timezone
from typing import List, Callable, Dict, Union, Tuple
from dataclasses import dataclass
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
KEYWORDS_FOR_DAILY_TWEETS = ['ukraine', 'ukrainian']
TWEET_LANGUAGE = 'en'
TWEET_FILTER = '-is:retweet'
DAILY_TWEET_LIMIT = 1000
PAGE_TWEET_LIMIT = 100

@dataclass
class TweepyConnector:
    '''A class that connects to Twitter API using Tweepy authentication data'''
    api_key: str = config.get('API', 'api_key')
    api_key_secret: str = config.get('API', 'api_key_secret')
    access_token: str = config.get('API', 'access_token')
    access_token_secret: str = config.get('API', 'ac_tok_secret')
    bearer_token: str = config.get('API', 'bearer_token')

    def authenticate(self):
        '''Authenticates the connection to Tweepy. Returns authenticated OAuthHandler, API and Client objects'''
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret, self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        client = tweepy.Client(self.bearer_token)
        return auth, api, client


def get_query_body(keywords: List[str] = KEYWORDS_FOR_DAILY_TWEETS, lang: str = TWEET_LANGUAGE, filter: str = TWEET_FILTER) -> str:
     '''Generates the body of the query using specified keywords, language and tweet filter'''
     combined_keywords = '(' + ' OR '.join([word for word in keywords]) + ')'
     query = f'{combined_keywords} lang:{lang} {filter}'
     return query

def get_tweet_fields(tweet: tweepy.Tweet) -> Dict[str, Union[int, str]]:
    '''Extracts specified tweet fields from a tweepy.Tweet type input'''
    return {
         'tweet_id': tweet.id,
         'author_id': tweet.author_id,
         'text': tweet.text,
         'created_at': str(tweet.created_at)[:11],
         'like_count': tweet.public_metrics['like_count'],
         'impression_count': tweet.public_metrics['impression_count'],
         'retweet_count': tweet.public_metrics['retweet_count'],
         'quote_count': tweet.public_metrics['quote_count']
         }
     
def get_dates_for_query() -> Tuple[str, str]:
    '''Generates the start and end dates for searching tweets for the current day'''
    query_start_date = (datetime.now(timezone.utc)-timedelta(days=2)).astimezone().isoformat()
    query_end_date = (datetime.now(timezone.utc).astimezone()-timedelta(days=1)).isoformat()
    return  query_start_date, query_end_date 
    
def obtain_daily_tweets(
        tweepy_connector: TweepyConnector, 
        get_query_body: Callable=get_query_body, 
        get_dates_for_query: Callable=get_dates_for_query,
        get_tweet_fields: Callable=get_tweet_fields, 
        max_results: int = PAGE_TWEET_LIMIT, 
        limit: int = DAILY_TWEET_LIMIT) -> pd.DataFrame:
    '''Searches for tweets posted on the current date. Returns a DataFrame'''
    _, _,  client = tweepy_connector.authenticate()
    query = get_query_body()
    query_start_date, query_end_date = get_dates_for_query()
    tweets = []
    for tweet in tweepy.Paginator(client.search_recent_tweets, query, tweet_fields=['context_annotations', 'created_at', 'public_metrics'], 
                                  expansions=['author_id'], max_results=max_results, 
                                  start_time=query_start_date, end_time=query_end_date).flatten(limit=limit):
        tweet_dict = get_tweet_fields(tweet)
        tweets.append(tweet_dict)
        
    return pd.DataFrame(tweets)

