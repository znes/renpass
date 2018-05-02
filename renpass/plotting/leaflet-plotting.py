# -*- coding: utf-8 -*-
"""
"""

from datapackage import Package
from geojson import FeatureCollection, Feature
import geopandas as gpd
import pandas as pd

import folium
from branca.colormap import linear
import vincent

from shapely.geometry import LineString


p = Package('../angus-datapackages/e-highway/datapackage.json')

types = ['dispatchable-generator', 'volatile-generator',
         'reservoir', 'run-of-river']


l = list()
for t in types:
   l.extend(p.get_resource(t).read(keyed=True))
df = pd.DataFrame.from_dict(l)
df = df.loc[:, ['bus', 'capacity', 'name']]
df.capacity = df.capacity.astype(float)

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


m = folium.Map(
    location=[49, 10],
    tiles='Mapbox Bright',
    zoom_start=5)

geojson_regions = FeatureCollection([
                    Feature(geometry=v.geometry,
                            properties={'name': k})
                    for k, v in regions.iterrows()])

colormap = linear.YlGn.scale(
    int(demand.amount.min()),
    int(demand.amount.max()))

folium.GeoJson(geojson_regions, name='Demand',
        style_function=lambda feature: {
        'fillColor': colormap(
            demand.loc[
                demand.bus == feature['properties']['name']].amount.values[0]),
        'color': 'black',
        'weight': 1,
        'dashArray': '5, 5',
        'fillOpacity': 0.9,
    }).add_to(m)

colormap.caption = 'Demand in TWh'
colormap.add_to(m)

geojson_lines = FeatureCollection([
                 Feature(geometry=v.geometry,
                         properties={'name': k})
                for k, v in conns_geo.iterrows()])

folium.GeoJson(geojson_lines, name='Transshipment capacities',
    style_function=lambda feature: {
        'fillColor': 'darkgray',
        'color': 'black',
        'weight': conns_geo.loc[feature['properties']['name']].capacity / 1e3,
        'dashArray': '5, 5',
        'fillOpacity': 0.9,}).add_to(m)

folium.LayerControl().add_to(m)

import altair as alt


for ix, row in regions.iterrows():
    popup = folium.Popup(max_width=3000)

    bar = alt.Chart(df.loc[df.bus==ix]).mark_bar().encode(
        x='name',
        y='capacity'
    )

    vega = folium.features.VegaLite(
        bar,
        width='100%',
        height='100%',
    )

    vega.add_to(popup)
    marker = folium.Marker(location=[
        list(row.geometry.centroid.coords[0])[1],
        list(row.geometry.centroid.coords[0])[0]],
                         icon=folium.Icon(icon_color='green'))
    popup.add_to(marker)
    marker.add_to(m)

m.save('map.html')
