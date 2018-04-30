# -*- coding: utf-8 -*-
"""
"""

from datapackage import Package
from geojson import FeatureCollection, Feature
import geopandas as gpd
import pandas as pd
import plotly.plotly as py
import plotly.offline as off
import plotly.graph_objs as go
from shapely.geometry import LineString


regions = gpd.read_file(
    '../angus-datapackages/e-highway/data/geometries/bus.geojson').\
        set_index('name')
conns = pd.read_csv(
    '../angus-datapackages/e-highway/data/elements/transshipment.csv',
    sep=";", index_col='name')

demand = pd.read_csv(
    '../angus-datapackages/e-highway/data/elements/demand.csv',
    sep=";", index_col='name')

conns_geo = conns.copy()

conns_geo['geometry'] = conns_geo.apply(
    lambda r: LineString([
        regions.loc[r['from_bus'], 'geometry'].centroid,
        regions.loc[r['to_bus'], 'geometry'].centroid]), axis=1)

# geometries = pd.concat([regions['geometry'], conns_geo['geometry']])


layout = go.Layout(
    title = 'Europe',
    geo = dict(
        resolution = 50,
        scope = 'europe',
        showframe = False,
        showcoastlines = True,
        showland = True,
        landcolor = "rgb(229, 229, 229)",
        countrycolor = "rgb(255, 255, 255)" ,
        coastlinecolor = "rgb(255, 255, 255)",
        projection = dict(
            type = 'Mercator'
        ),
        lonaxis = dict( range= [ -5, 25 ] ),
        lataxis = dict( range= [ 42, 65 ] ),
        domain = dict(
            x = [ 0, 1 ],
            y = [ 0, 1 ]
        )
    )
)



lines = [
    go.Scattergeo(
        lon=row.geometry.xy[0],
        lat=row.geometry.xy[1],
        hoverinfo = 'skip',
        name=ix,
        line = {
            'width': row.capacity/1000, 'color': 'darkgray'},
        mode='lines')
    for ix, row in conns_geo.iterrows()]

# for hover infor on mid one lines
mid_edge_trace = [
    go.Scattergeo(
        lon=[row.geometry.centroid.xy[0][0]],
        lat=[row.geometry.centroid.xy[1][0]],
        text="Line " + ix + " has capacity %.1f MW" % row.capacity,
        mode='markers',
        hoverinfo='text',
        showlegend=False,
        opacity=0)
    for ix, row in conns_geo.iterrows()]

# for hover infor on mid one lines
demand_traces = [
    go.Scattergeo(
        lon=[row.geometry.centroid.xy[0][0]],
        lat=[row.geometry.centroid.xy[1][0]],
        mode='markers',
        marker = dict(
            size = demand.loc[demand.bus == ix].amount/1e6,
            color = 'skyblue',
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'),
        hoverinfo='text',
        text="Demand " + str(float(demand.loc[demand.bus == ix].amount / 1e6)) + " TWh",
        showlegend=False,
        opacity=0.75)
    for ix, row in regions.iterrows()]

fig = go.Figure(layout=layout, data=lines+mid_edge_trace+demand_traces)

off.iplot(fig, filename='e-highway-transshipment-capacities.html')
