import os
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from matplotlib import colors
import pandas as pd
import plotly.graph_objs as go

from renpass import options
from renpass.analysis import plots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

app.datapath = os.path.abspath('../../data/oemof-eu/results')
app.scenarios = os.listdir(app.datapath)
app.color_dict = {
    name: colors.to_hex(color) for name, color in options.techcolor.items()}


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.H1(children='Renpass Results Analysis'),

    dcc.Link('Analysis', href='/analysis'),

])


analysis_layout = html.Div(children=[
    html.H1(children='Renpass Results Analysis'),

    dcc.Link('Go back to startpage', href='/', className='six columns'),

    html.Div([
        html.Div([
            html.Label('Scenario'),
            dcc.Dropdown(
                id='scenario',
                options=[{
                    'label': s,
                    'value': s}
                         for s in app.scenarios],
                value=''
            )],
        style={'width': '20%'})
    ]),

    html.Div([
        html.Div([
            html.Label('Comapare with'),
            dcc.Dropdown(
                id='compare',
                options=[{
                    'label': s,
                    'value': s}
                         for s in app.scenarios],
                value=''
            )],
        style={'width': '20%'})
    ]),

    html.Div([
        html.Div(children=[
            dcc.Graph(
                id='stacked_plot1'
            )
        ], style={'width': '50%', 'display': 'inline-block'}),

        html.Div(children=[
            dcc.Graph(
                id='stacked_plot2'
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
    ], className="row"),

    html.H3(children='Hourly analysis per country'),

    html.Div([
        dcc.Dropdown(
            id='country',
            options=[{}],
            value='DE')
    ], style={'width': '20%'}),


    html.Div(children=[
        dcc.Graph(
            id='hourly_plot',
            figure = dict(
                layout = go.Layout(
                    barmode='stack',
                    title='Hourly Plot',
                    yaxis=dict(
                        title='Energy in MWh',
                        titlefont=dict(
                            size=16,
                            color='rgb(107, 107, 107)'
                        ),
                        tickfont=dict(
                            size=14,
                            color='rgb(107, 107, 107)'
                        )
                    )
                )
            )
        )
    ], className='six Columns',
       style={'width': '90%', 'height':'80vh'}),

])



@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/analysis':
         return analysis_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

@app.callback(
    dash.dependencies.Output('hourly_plot', 'figure'),
    [dash.dependencies.Input('scenario', 'value'),
     dash.dependencies.Input('country', 'value')])
def update_hourly_plot(scenario, country='DE'):
    """
    """
    return plots.hourly_plot(scenario, country)

@app.callback(dash.dependencies.Output('stacked_plot1', 'figure'),
              [dash.dependencies.Input('scenario', 'value')])
def update_stacked_plot(scenario):
    """
    """
    return plots.stacked_plot(scenario)

@app.callback(dash.dependencies.Output('stacked_plot2', 'figure'),
              [dash.dependencies.Input('compare', 'value')])
def update_stacked_plot(scenario):
    """
    """
    return plots.stacked_plot(scenario)

@app.callback(dash.dependencies.Output('country', 'options'),
              [dash.dependencies.Input('scenario', 'value')])
def update_country_list(scenario):
    """
    """
    with open(os.path.join(app.datapath, scenario, 'config.json')) as f:
        data = json.load(f)
    return [{'label': r, 'value': r} for r in data['regions']]


if __name__ == '__main__':
    app.run_server(debug=True)
