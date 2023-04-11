import src.deployment.dash_components as dc
import src.database_manager as dm
import dash
from dash import dependencies
import src.deployment.generate_chart_data as gcd
import src.deployment.plotly_chart_components as pcc
from datetime import datetime, timedelta, date
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server
app.title='Twitter\'s Stance on Ukraine'
conn, cursor = dm.connect_to_db()

app.layout = dc.create_layout(gcd.generate_chart_data(conn))

@app.callback(
        dependencies.Output('output_chart', 'figure'), 
        [dependencies.Input('date_picker_single', 'date'),
        dependencies.Input('radio_buttons', 'value'),
         dependencies.Input('keyword_input', 'value')])
def update_chart(date_value, input_value_1, keyword_value):
    if date_value:
        start_date = date.fromisoformat(date_value).strftime('%Y-%m-%d')
        chart_data = gcd.generate_chart_data(conn, filter_keyword = keyword_value, query_start_date=start_date)
        plotly_figure = pcc.render_full_plotly_chart(chart_data, input_value_1)
        plotly_figure.update_layout(
            title={
            'text': f'Tweets that mention {keyword_value}' if keyword_value else 'All tweets',
            'x': 0.47,
            'yanchor': 'top',}
            )
    else:
        chart_data = gcd.generate_chart_data(conn, filter_keyword=keyword_value)
        plotly_figure = pcc.render_full_plotly_chart(chart_data, input_value_1)
        # dc.create_card(chart_data)
    plotly_figure.update_yaxes(title=dc.Y_AXIS_LABELS[input_value_1])
    
    return plotly_figure

if __name__ == '__main__':
    application.run(debug=True, port=8080)

