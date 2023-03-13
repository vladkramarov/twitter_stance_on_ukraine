import configparser
import pandas as pd
from dash import dcc, Dash, html, dependencies
from typing import Callable
import src.dash_app.chart_components as cc
import src.database_manager as dm
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def render_dash_chart():

    chart_data = dm.read_data_from_db()
    plotly_figure = cc.render_full_plotly_chart(chart_data)
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    y_axis_labels = {'daily_ratios': 'Daily Stance Ratio',
                     'cumulative_ratios': 'Cumulative Stance Ratio'}
    app.layout = html.Div([
        html.H1('Twitter\'s stance towards Ukraine'),
        html.H3(f'Data as of: {chart_data.created_at.max()}'),
        html.Div([
        html.H3('Search by Keyword', style={'text-align': 'center'}),
        dcc.Input(id = 'keyword_input', placeholder = 'Enter a keyword here and press Enter', value ='', type = 'text', debounce=True, n_submit=True,
                  style = {'display': 'block', 'margin': 'auto', 'text-align': 'center', 'width': '30%'}),
        dcc.RadioItems(id = 'radio_buttons', value='cumulative_ratios', 
                       options=[{'label': y_axis_labels[value], 'value': value} for value in y_axis_labels.keys()
                                ])]),
        html.Div(
            dcc.Graph(
                    id = 'output_chart', figure=plotly_figure), 
                    style={'display': 'inline-block', 'margin': 'auto', 'position': 'absolute', 'left': 290, 'right': 250, 'top': 250, 'bottom': 250})
])
    @app.callback(dependencies.Output('output_chart', 'figure'),
                [dependencies.Input('radio_buttons', 'value'),
                dependencies.Input('keyword_input', 'value')])
    def update_chart(input_value_1, keyword_value):
        if keyword_value:
            chart_data = dm.read_data_from_db(keyword_value)
            plotly_figure = cc.render_full_plotly_chart(chart_data, input_value_1)
            plotly_figure.update_layout(
                title = {
                'text': f'Tweets that mention {keyword_value}',
                'x': 0.47,
                'yanchor': 'top',
                })
        else:
            chart_data = dm.read_data_from_db()
            plotly_figure = cc.render_full_plotly_chart(chart_data, input_value_1)
        plotly_figure.update_yaxes(title = y_axis_labels[input_value_1])
        return plotly_figure    

    if __name__ == "__main__":
        app.run_server()

render_dash_chart()

    
