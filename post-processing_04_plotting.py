# -*- coding: utf-8 -*-
import pdb
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm

import os
os.chdir('C:/Users/doziimbos/renpass_gis/')

# global plotting options
plt.rcParams.update(plt.rcParamsDefault)
matplotlib.style.use('ggplot')
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['axes.facecolor'] = 'lightgray'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams.update({'font.size': 10})
plt.rcParams['image.cmap'] = 'Blues'
#
# read file to be plotted
file = ('results/scenario_morocco_2050_scenario_test005_2016-12-01_21-47-36_MA.csv')

df_raw = pd.read_csv(file, parse_dates=[0], index_col=0, keep_date_col=True)
df_raw.head()
df_raw.columns



# %% dispatch plot 

# country code
cc = 'MA'

# get fossil and renewable power plants
fuels = ['run_of_river', 'biomass', 'solar', 
         'wind', 'hydro_reservoir', 'csp_direct', 'storage_csp_out', 'gas', 'hard_coal', 'oil', 'storage_out', 'shortage']

dispatch = pd.DataFrame()

for f in fuels:
    cols = [c for c in df_raw.columns if f in c and cc in c]
    dispatch[f] = df_raw[cols].sum(axis=1)

dispatch.index = df_raw.index

# get imports and exports and aggregate columns
cols = [c for c in df_raw.columns if 'powerline' in c and cc in c]
powerlines = df_raw[cols]

exports = powerlines[[c for c in powerlines.columns
                      if c.startswith(cc + '_')]]

imports = powerlines[[c for c in powerlines.columns
                      if '_' + cc + '_' in c]]


dispatch['imports'] = imports.sum(axis=1)
dispatch['exports'] = exports.sum(axis=1)
dispatch['net_imports'] = dispatch.imports - dispatch.exports
dispatch['net_exports'] = dispatch.exports - dispatch.imports


# get storage and aggregate columns
# punped hydro storage
phs_in = df_raw[[c for c in df_raw.columns if 'storage_pumped_hydro_in' in c and cc in c]]
phs_out = df_raw[[c for c in df_raw.columns if 'storage_pumped_hydro_out' in c and cc in c]]
phs_level = df_raw[[c for c in df_raw.columns if 'storage_pumped_hydro_level' in c and cc in c]]

dispatch['phs_in'] = phs_in.sum(axis=1)
dispatch['phs_out'] = phs_out.sum(axis=1)
dispatch['phs_level'] = phs_level.sum(axis=1)

# agreggate all storage technologies in one column 'storage_'
dispatch['storage_in'] = dispatch['phs_in']
dispatch['storage_out'] = dispatch['phs_out']
dispatch['storage_level'] = dispatch['phs_level']

dispatch['csp'] = dispatch['csp_direct'] + dispatch['storage_csp_out']

# delete values close to zero
for x in range(0,len(dispatch)):
    #print(dispatch['shortage'][x])
    if dispatch['shortage'][x] < 0.000001:
        if dispatch['shortage'][x] > -0.0000001:
            dispatch['shortage'][x] = 0;
    if dispatch['biomass'][x] < 0.000001:
        if dispatch['biomass'][x] > -0.0000001:
            dispatch['biomass'][x] = 0;
    if dispatch['hard_coal'][x] < 0.000001:
        if dispatch['hard_coal'][x] > -0.0000001:
            dispatch['hard_coal'][x] = 0;
            
# MW to GW
dispatch = dispatch.divide(1000)

#%%
# translation
dispatch_de = dispatch[
    ['run_of_river', 'biomass', 'solar', 'wind', 'hydro_reservoir', 'csp', 'gas', 'hard_coal', 'oil', 'storage_out', 'shortage']]

# dict with new column names
en_de = {'run_of_river': 'Run-of-the-River Hydro Power',
         'biomass': 'Biomass',
         'solar': 'Solar PV',
         'wind': 'Wind',
         'hydro_reservoir': 'Hydro Power with Reservoir',
         'csp': 'CSP',
         'gas': 'Natural Gas',
         'hard_coal': 'Hard Coal',
         'oil': 'Oil', 
         'storage_out': 'Storage (Discharge)',
         'shortage': 'Power Shortage'}
dispatch_de = dispatch_de.rename(columns=en_de)

dispatch_de[['Run-of-the-River Hydro Power', 'Biomass', 'Solar PV', 'Wind', 'Hydro Power with Reservoir', 'CSP', 'Natural Gas', 'Hard Coal', 'Oil', 'Storage (Discharge)', 'Power Shortage']][0:24*365] \
             .plot(kind='area', stacked=True, linewidth=0, legend='reverse',
                   cmap=cm.get_cmap('Spectral'))
plt.legend(loc='lower center', bbox_to_anchor=(0.54, 1.04),
          ncol=5, fancybox=True, shadow=True)
plt.xlabel('Date')
plt.ylabel('Power in  GW')
plt.ylim(0, max(dispatch_de.sum(axis=1)))
plt.show()
