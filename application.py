import configparser
import pandas as pd
from dash import  Dash, dependencies
import src.dash_app.dash_components as dc
import src.dash_app.plotly_chart_components as pcc
import src.dash_app.generate_chart_data as gcd
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
application = Dash(__name__, external_stylesheets=dc.EXTERNAL_STYLESHEETS)
application.layout = dc.create_layout()
@application.callback(dependencies.Output('output_chart', 'figure'),
                    [dependencies.Input('radio_buttons', 'value'),
                        dependencies.Input('keyword_input', 'value')])
def update_chart(input_value_1, keyword_value):
    if keyword_value:
        chart_data = gcd.read_data_from_db(keyword_value)
        plotly_figure = pcc.render_full_plotly_chart(chart_data, input_value_1)
        plotly_figure.update_layout(
            title={
                'text': f'Tweets that mention {keyword_value}',
                'x': 0.47,
                'yanchor': 'top',
            })
    else:
        chart_data = gcd.read_data_from_db()
        plotly_figure = pcc.render_full_plotly_chart(chart_data, input_value_1)
    plotly_figure.update_yaxes(title=dc.Y_AXIS_LABELS[input_value_1])
    return plotly_figure


if __name__ =="__main__":
    application.run_server(host = "0.0.0.0", port=8000)


