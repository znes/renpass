# -*- coding: utf-8 -*-
import json
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

from renpass import options
from renpass.analysis.main import app

def hourly_plot(scenario, bus):
    """
    """
    datapath = app.datapath

    df = pd.read_csv(
        os.path.join(datapath, scenario, 'output', bus + '.csv'),
        index_col=[0], parse_dates=True)

    #df = df.resample('1D').mean()
    x = df.index
    # kind of a hack to get only the technologies
    df.columns = [c.strip(bus[0:3]) for c in df.columns]

    flexibility = ['import', 'acaes', 'phs', 'lithium_battery']

    # create plot
    layout = go.Layout(
        barmode='stack',
        title='Hourly supply and demand in {} for scenario {}'.format(bus, scenario),
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

    data = []


    for c in df:
        if c in flexibility:
            data.append(
                go.Scatter(
                    x = x,
                    y = df[c].clip(lower=0),
                    name=c,
                    stackgroup='positive',
                    line=dict(width=0, color=app.color_dict.get(c, 'black'))
                )
            )
            data.append(
                go.Scatter(
                    x = x,
                    y = df[c].clip(upper=0),
                    name=c+'-charge',
                    stackgroup='negative',
                    line=dict(width=0, color=app.color_dict.get(c, 'black')),
                    showlegend= False
                )
            )
        elif 'load' in c:
            # append load
            data.append(
                go.Scatter(
                    x = x,
                    y = df[c],
                    name = c,
                    line=dict(width=3, color='darkred')
                )
            )
        elif 'excess' in c:
            pass
        else:
            data.append(
                go.Scatter(
                    x = x,
                    y = df[c],
                    name=c,
                    stackgroup='positive',
                    line=dict(width=0, color=app.color_dict[c])
                )
            )

    return {'data': data, 'layout': layout}


def stacked_plot(scenario):
    """
    """
    df = pd.read_csv(
        os.path.join(app.datapath, scenario, 'output', 'capacities.csv'),
        index_col=0)

    return {
        'data': [go.Bar(
            x = row.index,
            y = row.values,
            name = idx,
            marker=dict(color=app.color_dict[idx])
       ) for idx, row in df.iterrows()],
       'layout': go.Layout(
            barmode='stack',
            title="Installed capacities for scenario {}".format(scenario)
       )
    }


#datapath = os.path.abspath('../../data/oemof-eu/results')
