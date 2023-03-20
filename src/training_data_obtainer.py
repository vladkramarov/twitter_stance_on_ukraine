import snscrape.modules.twitter as snstwitter
import pandas as pd
from typing import List

class Gettweets:
  def __init__(self, since_date = None, until_date = None, lang = ":en", filter = '-filter:replies'):
    self.since_date = since_date
    self.until_date = until_date
    self.lang = lang
    self.filter = filter

  def build_query_to_search_from_users(self, user_list: List[str], words_mentioned: List[str]) -> str:
    users = '(' + ' OR '.join(['from:'+user for user in user_list]) + ')'
    keywords = '(' + ' OR ' .join([word for word in words_mentioned]) + ')'
    query = f'{keywords} users lang {self.lang} {self.filter} since:'{self.since_date}'
    return query

  def build_query_to_search_by_hashtags(self, hashtag_list) -> str:
    hashtags = '(' + ' OR '.join(['#'+hashtag for hashtag in hashtag_list])
    query = f'{hashtags} lang{self.lang} {self.filter} since:{self.since_date}'
    return query
  
  def build_query_to_search_by_keywords(self, keywords_first_set, keywords_second_set) -> str:

    keywords_1 = '(' + ' OR '.join(word for word in keywords_first_set) + ')'
    keywords_2 = ' OR '.join(f'({word})' for word in keywords_second_set)
    query = f'{keywords_1}  ({keywords_2}) lang{self.lang} {self.filter} since:{self.since_date} until:{self.until_date}'
    return query

  def get_tweets(self, query_list: List[str], limit: int, stance:str = None) -> pd.DataFrame:
    all_tweets = []
    stance_dict = {'positive':0, 'negative':1, 'neutral':2}

    for query in query_list:
      tweet_list = []
      for tweet in snstwitter.TwitterSearchScraper(query).get_items():
        if len(tweet_list) == limit:
          break
        else:
          tweet_list.append([tweet.id, tweet.date, tweet.user.username, tweet.content, tweet.likeCount, tweet.viewCount,  tweet.retweetCount, tweet.quoteCount])
      all_tweets.extend(tweet_list)
    tweets_df = pd.DataFrame(all_tweets, columns = ['id', 'date', 'username', 'content', 'like_count', 'impression_count','retweet_count', 'quote_count'])
    tweets_df['label'] = stance_dict[stance]

    tweets_df = tweets_df.drop_duplicates()

    return tweets_df
