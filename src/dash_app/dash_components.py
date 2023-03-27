import pandas as pd
from dash import dcc, Dash, html, dependencies
from typing import Callable, Dict, List
import src.dash_app.plotly_chart_components as pcc
import src.dash_app.generate_chart_data as gcd

chart_data = gcd.read_data_from_db()
EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
Y_AXIS_LABELS = {'daily_ratios': 'Daily Stance Ratio', 'cumulative_ratios': 'Cumulative Stance Ratio'}

def create_title():
    return html.H1('Twitter\'s stance towards Ukraine')

def create_subheading(chart_data = chart_data):
    return html.Div([
        html.H4(f'The stance is determined based on ~10,000 tweets in English that are collected daily'),
        html.H4(f'Data is gathered starting on {chart_data.created_at.min()} and until {chart_data.created_at.max()}')])

def create_search_bar():
    return html.Div([
        html.H4('Search by Keyword ', style={'text-align': 'center'}),
        dcc.Input(id = 'keyword_input', placeholder = 'Enter a keyword here and press Enter', value ='', type = 'text', debounce=True, n_submit=True,
                style = {'display': 'block', 'margin': 'auto', 'text-align': 'center', 'width': '30%'})])

def create_radio_items():
    return dcc.RadioItems(id = 'radio_buttons', value='cumulative_ratios', 
                    options=[{'label': Y_AXIS_LABELS[value], 'value': value} for value in Y_AXIS_LABELS.keys()
                                ])
def create_main_chart(render_full_plotly_chart: Callable = pcc.render_full_plotly_chart):
    return html.Div(
            dcc.Graph(
                    id = 'output_chart', figure=render_full_plotly_chart(chart_data)), 
                    style={'display': 'inline-block', 'margin': 'auto', 'position': 'absolute', 'left': 290, 'right': 250, 'top': 250, 'bottom': 220})

def create_layout():
    return html.Div([
        create_title(),
        create_subheading(),
        create_search_bar(),
        create_radio_items(),
        create_main_chart()])

