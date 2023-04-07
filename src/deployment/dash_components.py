from dash import dcc, Dash, html
from typing import Callable, Dict, List
import src.deployment.plotly_chart_components as pcc
import src.deployment.generate_chart_data as gcd
import dash_bootstrap_components as dbc

EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
Y_AXIS_LABELS = {'daily_ratios': 'Daily Stance Ratio', 'cumulative_ratios': 'Cumulative Stance Ratio'}
CARD_BACKGROUND_COLORS = {'positive': 'limegreen', 'negative': 'crimson', 'neutral': 'steelblue'}

def create_title():
    return html.H1('Twitter\'s stance towards Ukraine')

def create_subheading(chart_data):
    return html.Div([
        html.H4(f'The stance is determined based on ~10,000 tweets in English that are collected daily'),
        html.H4(f'Data is gathered starting on {chart_data.created_at.min()} and until {chart_data.created_at.max()}')])

def create_search_bar():
    '''Creates a search bar to filter tweets by a keyword'''
    return html.Div([
        html.H4('Search by Keyword ', style={'text-align': 'center'}),
        dcc.Input(id = 'keyword_input', placeholder = 'Enter a keyword here and press Enter', value ='', type = 'text', debounce=True, n_submit=True,
                style = {'display': 'block', 'margin': 'auto', 'text-align': 'center', 'width': '30%'})])

def create_radio_items():
    '''Creates 2 buttons (radio items) that allow to toggle between daily and cumulative ratios'''
    return dcc.RadioItems(id = 'radio_buttons', value='daily_ratios', 
                    options=[{'label': Y_AXIS_LABELS[value], 'value': value} for value in Y_AXIS_LABELS.keys()
                                ])

def create_relative_date_button():
    '''Creates a button that allows to filter out all tweets but the ones that were created within the last 7 days'''
    return html.Div([
        html.Div([
            html.Button('Last 7 Days', id='last-7-days-button', n_clicks=0)
        ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'flex-end'})
    ], style={'display': 'flex', 'justify-content': 'flex-end'})

def create_card(chart_data):
    highest_ratio, label = gcd.select_highest_ratio_and_label(chart_data)
    card_text = f'With {highest_ratio:.0%} {label} tweets'
    background_color = CARD_BACKGROUND_COLORS[label]
    return html.Div(
        [dbc.Card([
            dbc.CardBody([
                html.H3(f'{label.capitalize()}', className='text-center', id='card-label'),
                    html.P(card_text)],style={'margin': '10px'},id='card')],
        style={'backgroundColor': background_color, 'width': '18rem'}
    ),
    ])

def create_main_chart(chart_data, render_full_plotly_chart: Callable = pcc.render_full_plotly_chart):
    '''A function to render plotly chart with updated data'''
    return html.Div(
        style={'position': 'relative'},
        children=[
            html.Div(
                style={'position': 'absolute', 'top': '25%', 'left': '50%', 'transform': 'translate(-47%, -35%)'},
                children=[
                    dcc.Graph(
                        id='output_chart',
                        figure=render_full_plotly_chart(chart_data))])
        ]
    )
def create_layout(chart_data):
    '''A function that generates the whole layout'''
    return html.Div([
        create_title(),
        create_subheading(chart_data),
        create_search_bar(),
        create_radio_items(),
        create_relative_date_button(),
        create_card(chart_data),
        create_main_chart(chart_data)])

