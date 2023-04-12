import pandas as pd
import src.database_manager as dm
import src.core as core
import datetime

def build_the_query(filter_keyword: str = '', table_name: str = core.TABLE_NAME, query_start_date: str = '2023-02-01') -> str:
    '''Builds a PostgreSQL query to obtain data for the cumulative and daily tweet ratios. Allows to select the table name and a filter keyword/phrase'''

    return f'''WITH total_count AS (select created_at, COUNT(*) AS daily_total
                FROM {table_name}
                WHERE text ILIKE '%{filter_keyword}%' AND created_at > '{query_start_date}'
                GROUP BY created_at),
                daily_counts_and_totals AS (
                    SELECT nt.created_at, label, COUNT(*) as daily_count, daily_total, SUM(like_count) as total_likes
                    FROM new_tweets_revised nt                  
                    JOIN total_count tc
                    ON tc.created_at = nt.created_at
                    WHERE nt.text ILIKE '%{filter_keyword}%'                  
                    GROUP BY nt.created_at, label, daily_total)
                SELECT created_at, label,
                    ROUND(total_likes/daily_count::numeric, 2) as likes_per_post,
                    ROUND(daily_count/daily_total::numeric, 2) as daily_ratios,
                    ROUND(SUM(daily_count) OVER ( PARTITION BY label ORDER BY created_at)/SUM(daily_count) OVER (ORDER BY created_at)::numeric,2) as cumulative_ratios
                    FROM daily_counts_and_totals'''


def generate_chart_data(db_connector, filter_keyword: str = '', table_name: str = core.TABLE_NAME, query_start_date: str = '2023-02-01') -> pd.DataFrame:
    '''Returns a DataFrame containing the queried data.'''
    query = build_the_query(filter_keyword, query_start_date=query_start_date)
    values_to_replace_labels = {0: 'positive', 1: 'negative', 2: 'neutral'}
    data = pd.read_sql_query(query, db_connector)
    data['label'] = data['label'].replace(values_to_replace_labels)

    return data

def select_highest_ratio_and_label(data):
    '''Returns the label with the highest cumulative ratio as well as the actual ratio. Used for the Card Visual'''
    latest_data = data[data['created_at']==data['created_at'].max()]
    highest_ratio_row = latest_data.loc[latest_data['cumulative_ratios'].idxmax()]

    return highest_ratio_row['cumulative_ratios'], highest_ratio_row['label']

