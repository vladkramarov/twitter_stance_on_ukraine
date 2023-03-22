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
    

# conn, cursor = connect_to_db()
# query = "select created_at, COUNT(*)from new_tweets_revised group by created_at"
# cursor.execute(query)
# cursor.fetchall()