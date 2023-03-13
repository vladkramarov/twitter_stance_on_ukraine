import pandas as pd
import configparser
import psycopg2
from typing import Callable, Tuple
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

DB_NAME = config.get('DATABASE', 'database')
DB_USER = config.get('DATABASE', 'user')
DB_PASSWORD = config.get('DATABASE', 'password')
DB_HOST = config.get('DATABASE', 'host')
DB_TABLE_NAME = 'new_tweets_revised'

def connect_to_db() -> Tuple:
    '''Connects to the specified PostgreSQL database, returns a connection and cursor objects'''
    conn = psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD)
    cursor = conn.cursor()
    return conn, cursor

def create_db(table_name: str, connector_func: Callable = connect_to_db) -> None:
    '''Creates a new PostgreSQL table with the specified name'''
    conn, cursor = connector_func()
    cursor.execute(f'''CREATE TABLE {table_name} (
        tweet_id BIGINT PRIMARY KEY, author_id BIGINT, text TEXT, username TEXT, created_at TEXT, 
        like_count INT, impression_count INT, retweet_count INT, quote_count INT, label INT)''')
    conn.commit()
    cursor.close()
    conn.close()

def delete_db(table_name: str, connector_func: Callable = connect_to_db) -> None:
    '''Deletes the specified PostgreSQL table from the database'''
    conn, cursor = connector_func()
    cursor.execute(f'DROP TABLE {table_name}')
    conn.commit()
    cursor.close()
    conn.close()


def write_to_db(dataset_with_labels: pd.DataFrame, table_name: str = DB_TABLE_NAME, connector_func: Callable = connect_to_db) -> None:
    '''Writes a Pandas DataFrame to a PostreSQL table with the specified name'''
    conn, cursor = connector_func()
    for index, row in dataset_with_labels.iterrows():
        cursor.execute(f'''INSERT INTO {table_name} (tweet_id, author_id, text, created_at, like_count, impression_count, retweet_count, quote_count, label) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (tweet_id) DO NOTHING''',
        (row['tweet_id'], row['author_id'], row['text'], row['created_at'], row['like_count'], row['impression_count'], row['retweet_count'], row['quote_count'], row['label']))
    conn.commit()

def check_total_entries(table_name: str = DB_TABLE_NAME, connector_func: Callable = connect_to_db) -> int:
    conn, cursor = connector_func()
    query = f'SELECT COUNT (*) from {table_name}'
    cursor.execute(query)
    return cursor
    
    
def build_the_query(filter_keyword: str = '', table_name: str = DB_TABLE_NAME) -> str:
    '''Builds a PostgreSQL query to obtain data for the cumulative and daily tweet ratios. Allows to select the table name and a filter keyword/phrase'''

    return f'''WITH total_count AS (select created_at, COUNT(*) AS daily_total
                FROM {table_name}
                WHERE text ILIKE '%{filter_keyword}%'
                GROUP BY created_at),

                daily_counts_and_totals AS (
                    SELECT nt.created_at, label, COUNT(*) as daily_count, daily_total
                    FROM new_tweets_revised nt                  
                    JOIN total_count tc
                    ON tc.created_at = nt.created_at
                    WHERE nt.text ILIKE '%{filter_keyword}%'                      
                    GROUP BY nt.created_at, label, daily_total)

                SELECT *, 
                    SUM(daily_count) OVER ( PARTITION BY label ORDER BY created_at) as rolling_sum_per_label,
                    SUM(daily_count) OVER (ORDER BY created_at) as rolling_total,
                    ROUND(daily_count/daily_total::numeric, 2) as daily_ratios,
                    ROUND(SUM(daily_count) OVER ( PARTITION BY label ORDER BY created_at)/SUM(daily_count) OVER (ORDER BY created_at)::numeric,2) as cumulative_ratios
                    FROM daily_counts_and_totals'''


def read_data_from_db(filter_keyword: str = '', table_name: str = DB_TABLE_NAME, build_the_query: Callable = build_the_query):
    '''Returns a DataFrame containing the queried data.'''
    query = build_the_query(filter_keyword)
    conn, cursor = connect_to_db()
    values_to_replace_labels = {0: 'positive', 1: 'negative', 2: 'neutral'}
    data = pd.read_sql_query(query, conn)
    data['label'] = data['label'].replace(values_to_replace_labels)

    return data
