from dash import dcc, Dash, html
from typing import Callable, Dict, List
import src.deployment.plotly_chart_components as pcc
import src.deployment.generate_chart_data as gcd
import dash_bootstrap_components as dbc
import datetime

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
        html.H4('Filter tweets by keywords of phrases', style={'text-align': 'center'}),
        dcc.Input(id = 'keyword_input', placeholder = 'Enter a keyword here and press Enter', value ='', type = 'text', debounce=True, n_submit=True,
                style = {'display': 'block', 'margin': 'auto', 'text-align': 'center', 'width': '100%'})])

def create_radio_items():
    '''Creates 2 buttons (radio items) that allow to toggle between daily and cumulative ratios'''
    return html.Div([
        html.H4('Choose daily or cumulative ratios', style={'text-align': 'center'}),
        dcc.RadioItems(id = 'radio_buttons', value='daily_ratios', 
                    options=[{'label': Y_AXIS_LABELS[value], 'value': value} for value in Y_AXIS_LABELS.keys()
                                ])])

def create_date_picker():
    '''Creates a button that allows to filter out all tweets but the ones that were created within the last 7 days'''
    return  html.Div([
        html.H4('Select query start date'),
        dcc.DatePickerSingle(
                id='date_picker_single', 
                min_date_allowed=datetime.date(2023, 2, 2), 
                max_date_allowed=datetime.date(2023, 4, 9), 
                initial_visible_month=datetime.date(2023, 3, 10),
                date=datetime.date(2023, 2, 2),
                style={'display': 'block', 'margin': 'auto', 'text-align': 'center', 'width': '100%'})])
def description_card(chart_data):
    """ """
    return html.Div(
        id="description-card",
        children=[
            html.H3("Twitter's Sentiment on the war in Ukraine"),
            html.H5("Based on ~10,000 english tweets collected daily"),
            html.H5(f'Tweets are collected starting on {chart_data.created_at.min()}'),
            html.Div(
                id="intro",
                children=".",
            ),
        ],
    )

def create_main_chart(chart_data, render_full_plotly_chart: Callable = pcc.render_full_plotly_chart):
    '''A function to render plotly chart with updated data'''
    return html.Div(
        style={'position': 'relative'},
        children=[
            html.Div(
                style={'position': 'absolute', 'top': '35%', 'left': '50%', 'transform': 'translate(-47%, -7%)'},
                children=[
                    dcc.Graph(
                        id='output_chart',
                        figure=render_full_plotly_chart(chart_data))])
        ]
    )
def create_ridge_plots(chart_data):
    return html.Div(
        style={'position': 'absolute', 'top': '35%', 'left': '50%', 'transform': 'translate(-10%, 50%)'},
        children=[
        dcc.Graph(id='ridge_plot',
                  figure = pcc.ridge_plot(chart_data))])

def create_layout(chart_data):
    '''A function that generates the whole layout'''
    return html.Div([
        html.Div(
            id='left_column',
            className='three columns',
            children=[
                description_card(chart_data), 
                html.Br(),
                create_radio_items(),
                html.Br(),
                create_search_bar(),
                html.Br(),
                create_date_picker(),
                html.P('Cumulative ratios will be recalculated based on selected date')
            ], 
            style={
                'background-color': '#f4f4f4',
                'margin-top': '20px',
                'padding': '0rem 2rem',
                'display': 'flex',
                'flex-direction': 'column',
                'align-items': 'center',
                'min-height': 'calc(100vh - 5.5rem)'
            }
        ), 
        html.Div(
            id='right_column',
            className='nine columns',
            children=[
                html.Br(),
                create_main_chart(chart_data),
                html.Br(),
                create_ridge_plots(chart_data)
            ], 
            style={
                'padding': '0rem 2rem',
                'min-height': 'calc(100vh - 5.5rem)'
            }
        ),
    ])


        # description_card(),
        # create_subheading(chart_data),
        # create_search_bar(),
        # create_radio_items(),
        # create_date_picker(),
        # # create_card(chart_data),
        # create_main_chart(chart_data)])

