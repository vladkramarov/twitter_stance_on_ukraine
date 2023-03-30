import src.deployment.dash_components as dc
import dash
from dash import dependencies
import src.deployment.generate_chart_data as gcd
import src.deployment.plotly_chart_components as pcc
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server
app.title='Twitter\'s Stance on Ukraine'
app.layout = dc.create_layout()
@app.callback(dependencies.Output('output_chart', 'figure'),
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
if __name__ == '__main__':
    application.run(debug=True, port=8080)