import pandas as pd
import psycopg2
from typing import Callable, Tuple
import os
import src.core as core
DB_USER = os.environ['db_user']
DB_NAME = os.environ['db_name']
DB_PASSWORD = os.environ['db_password']
DB_HOST = os.environ['db_host']

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

def write_to_db(dataset_with_labels: pd.DataFrame, table_name: str = core.TABLE_NAME, connector_func: Callable = connect_to_db) -> None:
    '''Writes a Pandas DataFrame to a PostreSQL table with the specified name'''
    conn, cursor = connector_func()
    for index, row in dataset_with_labels.iterrows():
        cursor.execute(f'''INSERT INTO {table_name} (tweet_id, author_id, text, created_at, like_count, impression_count, retweet_count, quote_count, label) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (tweet_id) DO NOTHING''',
        (row['tweet_id'], row['author_id'], row['text'], row['created_at'], row['like_count'], row['impression_count'], row['retweet_count'], row['quote_count'], row['label']))
    conn.commit()
    conn.close()

def check_total_entries(table_name: str = core.TABLE_NAME, connector_func: Callable = connect_to_db) -> int:
    conn, cursor = connector_func()
    query = f'SELECT COUNT (*) from {table_name}'
    cursor.execute(query)
    return cursor.fetchall()

def check_tweets_per_day(table_name: str = core.TABLE_NAME, connector_func: Callable = connect_to_db):
    conn, cursor = connector_func()
    query = f'SELECT created_at, COUNT (*) from {table_name} GROUP BY created_at'
    cursor.execute(query)
    return cursor.fetchall()


