import pandas as pd
import importlib.util
import plotly.express as px
import plotly.graph_objects as go
import src.core as core
import importlib
importlib.reload(core)

color_map = {
        'positive': 'rgb(5, 200, 50)',
        'negative': 'rgb(200, 10, 10)',
        'neutral': 'rgb(10, 125, 200)'
        }
def render_plotly_chart(chart_data: pd.DataFrame='', y_axis: str = 'daily_ratios'):
    '''Initializes a plotly chart with pre-defined colors for each line'''

    fig = px.line(chart_data, x='created_at', y=y_axis, color = 'label', color_discrete_map=color_map)
    fig.update_xaxes(title = 'Date')
    fig.update_yaxes(title = 'Cumulative Stance Ratio')
    fig.update_layout(width = 1000, height = 500)
    
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

def render_full_plotly_chart(chart_data, y_axis = 'daily_ratios'):
    fig = render_plotly_chart(chart_data, y_axis)
    fig = add_date_buttons(fig)
    return fig


def ridge_plot(chart_data, metric_to_display='avg_likes_per_post', metric_label='Likes'):
    fig = go.Figure()
    for i in color_map:
        fig.add_trace(go.Violin(x=chart_data.loc[chart_data['label']==i][metric_to_display], line_color=color_map[i], name=f'{i.capitalize()}',hovertemplate='Median: %{y:.2f}<extra></extra>'))

    fig.update_traces(orientation='h', side='positive', width=3, points=False)
    fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
    fig.update_layout(width = 800, height = 400, margin=dict(l=50, r=50, t=50, b=50))
    fig.update_layout(title={'text':f'Ridge Plot of Average {metric_label} per Tweet', 'x': 0.47, 'yanchor': 'top'})
    fig.update_layout(xaxis=dict(range=[0, None]))
    return fig