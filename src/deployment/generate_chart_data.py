import pandas as pd
from typing import Callable
import src.database_manager as dm
import src.core as core


def build_the_query(filter_keyword: str = '', table_name: str = core.TABLE_NAME) -> str:
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


def generate_chart_data(filter_keyword: str = '', table_name: str = core.TABLE_NAME, build_the_query: Callable = build_the_query) -> pd.DataFrame:
    '''Returns a DataFrame containing the queried data.'''
    query = build_the_query(filter_keyword)
    conn, cursor = dm.connect_to_db()
    values_to_replace_labels = {0: 'positive', 1: 'negative', 2: 'neutral'}
    data = pd.read_sql_query(query, conn)
    data['label'] = data['label'].replace(values_to_replace_labels)

    return data
