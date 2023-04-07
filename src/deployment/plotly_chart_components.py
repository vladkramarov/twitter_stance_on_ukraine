import pandas as pd
import importlib.util
import plotly.express as px
import src.core as core
import importlib
importlib.reload(core)


def render_plotly_chart(data_for_graph: pd.DataFrame='', y_axis: str = 'daily_ratios'):
    '''Initializes a plotly chart with pre-defined colors for each line'''
    color_map = {
        'positive': '#27ae60',
        'negative': '#c0392b',
        'neutral': '#2980b9'
    }
    fig = px.line(data_for_graph, x='created_at', y=y_axis, color = 'label', color_discrete_map=color_map)
    fig.update_xaxes(title = 'Date')
    fig.update_yaxes(title = 'Cumulative Stance Ratio')
    fig.update_layout(width = 1200, height = 600)
    
    return fig

def add_date_buttons(plotly_object):
    '''Adds date buttons to the chart that allow to zoom in on a certain day range'''
    date_buttons = [
    {'count': 7, 'step': 'day', 'stepmode': 'backward', 'label': '7D'},
    {'count':14, 'step': 'day', 'stepmode': 'backward', 'label': '14D'},
    {'count': 21, 'step': 'day', 'stepmode': 'backward', 'label': '21D'},
    {'count': 1, 'step': 'month', 'stepmode':'backward', 'label': '1M'}]
    plotly_object.update_layout({'xaxis': {'rangeselector': {'buttons': date_buttons}}})

    return plotly_object

def render_full_plotly_chart(data, y_axis = 'daily_ratios'):
    fig = render_plotly_chart(data, y_axis)
    fig = add_date_buttons(fig)
    return fig

