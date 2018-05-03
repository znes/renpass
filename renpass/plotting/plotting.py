# -*- coding: utf-8 -*-
"""
"""

from datapackage import Package

import pandas as pd
import plotly.plotly as py
import plotly.offline as off
import plotly.graph_objs as go


p = Package('../angus-datapackages/e-highway/datapackage.json')

types = ['dispatchable-generator', 'volatile-generator',
         'reservoir', 'run-of-river']


l = list()
for t in types:
   l.extend(p.get_resource(t).read(keyed=True))
df = pd.DataFrame.from_dict(l)

df['tech'] = [i[0:-3] for i in df['name']]
buses = [r['name'] for r in p.get_resource('bus').read(keyed=True)]

colors = {
    'pv': 'rgb(255,255,153)',
    'wind': 'rgb(0,191,255)',
    'ocgt': 'rgb(105,105,105)',
    'biomass': 'rgb(107,142,35)',
    'run-of-river': 'rgb(138,43,226)',
    'reservoir': 'rgb(127,255,212)'}

data= [
    go.Bar(
        marker = {
            'color': colors.get(tech)},
        name=tech,
        x=df.loc[df['tech']==tech, 'bus'],
        y=df.loc[df['tech'] == tech, 'capacity'])
    for tech in df['tech'].unique()]

layout = go.Layout(
    barmode='stack',
    title='Installed capacities',
    yaxis=dict(
        title='Installed capacity in MW',
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

fig = go.Figure(data=data, layout=layout)

off.plot(fig, filename='e-highway-capacities.html')
