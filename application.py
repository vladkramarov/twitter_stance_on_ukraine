import src.deployment.dash_components as dc
import src.database_manager as dm
import dash
from dash import dependencies
import src.deployment.generate_chart_data as gcd
import src.deployment.plotly_chart_components as pcc
from datetime import date
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server
app.title='Twitter\'s Stance on Ukraine'

conn, cursor = dm.connect_to_db()
chart_data = gcd.generate_chart_data(conn)
ridge_chart_data = chart_data.iloc[:, :5] #stored dataset just for the ridge chart, since it does not need to retrieve any additional information from the database. runs much faster
app.layout = dc.create_layout(chart_data)

@app.callback(
        dependencies.Output('output_chart', 'figure'), 
        [dependencies.Input('date_picker_single', 'date'),
        dependencies.Input('radio_buttons', 'value'),
         dependencies.Input('keyword_input', 'value')])
def update_main_chart(date_value, radio_button_input, keyword_value):
    '''Update the main chart based on the input values'''
    if date_value:
        start_date = date.fromisoformat(date_value).strftime('%Y-%m-%d')
        chart_data = gcd.generate_chart_data(conn, filter_keyword = keyword_value, query_start_date=start_date)
        plotly_figure = pcc.render_full_plotly_chart(chart_data, radio_button_input)
        plotly_figure.update_layout(
            title={
            'text': f'Tweets that mention {keyword_value}' if keyword_value else 'All tweets',
            'x': 0.47,
            'yanchor': 'top',}
            )
    else:
        chart_data = gcd.generate_chart_data(conn, filter_keyword=keyword_value)
        plotly_figure = pcc.render_full_plotly_chart(chart_data, radio_button_input)
    plotly_figure.update_yaxes(title=dc.Y_AXIS_LABELS[radio_button_input])
    
    return plotly_figure

@app.callback(
    dependencies.Output('ridge_plot', 'figure'),
    dependencies.Input('dropdown', 'value'))
def update_ridge_plots(dropdown_input):
    '''Callback to select a metric shown on the Ridge plot'''
    return pcc.ridge_plot(ridge_chart_data, dropdown_input, dc.RIDGE_TITLE_OPTION[dropdown_input])

if __name__ == '__main__':
    application.run(debug=True, port=8080)

