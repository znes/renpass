# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 10:31:07 2016

@author: doziimchm
"""

# -*- coding: utf-8 -*-
import pdb
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from datetime import datetime
import os
os.chdir('C:/Users/doziimbos/renpass_gis/')

# global plotting options
plt.rcParams.update(plt.rcParamsDefault)
matplotlib.style.use('ggplot')
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['axes.facecolor'] = 'silver'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams.update({'font.size': 10})
plt.rcParams['image.cmap'] = 'Blues'

# %% configuration 
scenario_name = 'scenario_morocco_2050_scenario_test001'
scenario_timestamp01 = '2016-12-01_09-50-21' # Time when renpass_gis_main.py was run
scenario_timestamp02 = '2016-12-01_10-03-25' # Time when the national Mococcan result was generated
country01 = 'AL'
country02 = 'ES'
country03 = 'MA'
country04 = 'MR' 
country05 = 'PT'

file01 = scenario_name + '_' + scenario_timestamp01 + '_' + country01 + '.csv'
file02 = scenario_name + '_' + scenario_timestamp01 + '_' + country02 + '.csv'
file03 = scenario_name + '_' + scenario_timestamp02 + '_' + country03 + '.csv'
file04 = scenario_name + '_' + scenario_timestamp01 + '_' + country04 + '.csv'
file05 = scenario_name + '_' + scenario_timestamp01 + '_' + country05 + '.csv'


# For MA use script 'post-processing_01_hourly_sums_regions.py' to generate one csv for MA out of dprs
files = {
    country01: file01,
    country02: file02,
    country03: file03,
    country04: file04,
    country05: file05}


# define fuels 
fuels = ['run_of_river', 'storage_reservoir_out', 'biomass', 'solar', 'wind', 'csp_direct', 'storage_csp_out', 'geothermal', 'gas', 'hard_coal', 'oil', 'load', 'excess', 
         'shortage']


# create dataframe with fuels, import, export and storage as columns
results = pd.DataFrame(columns=fuels+['import', 'export', 'storage_in', 'storage_out', 'storage_level'])
all_powerlines = pd.DataFrame()

# loop through all countries
for k, v in files.items():
    df = pd.read_csv('results/' + v, parse_dates=[0],
                     index_col=0, keep_date_col=True)
    #df_tmp = pd.DataFrame()
    
    # create for every country the sum of each column
    sums_per_country = df.sum()

    
    # create sums_per_country without storage. Because the fuel 'hydro' is in storage (pumped_hydro and hydrogen) as well
    nostorage = [c for c in df.columns if 'storage' not in c and k in c]
    sums_per_country_fuels = sums_per_country[nostorage]
    # create results dataframe with countries as rows and fuels as columns         
    for f in fuels:
        results.ix[k, f] = sum([sums_per_country_fuels[i] for i in sums_per_country_fuels.index 
                      if f in i])
    
    # get imports and exports                      
    cols = [c for c in df.columns if 'powerline' in c and k in c]
    powerlines = sums_per_country[cols]
    results.ix[k, 'import'] = powerlines[[c for c in powerlines.index
                              if '_' + k + '_' in c]].sum()
    results.ix[k, 'export'] = powerlines[[c for c in powerlines.index
                          if c.startswith(k + '_')]].sum()
    
    # get storage summed up all technologies
    st = [c for c in df.columns if 'storage' in c and k in c]
    storages = sums_per_country[st]
    results.ix[k, 'storage_in'] = storages[[c for c in storages.index
                            if 'in' in c]].sum()
    results.ix[k, 'storage_out'] = storages[[c for c in storages.index
                            if 'out' in c]].sum()
    results.ix[k, 'storage_level'] = storages[[c for c in storages.index
                            if 'level' in c]].sum()
    
    #not yet solved: all transmission capacity into one dataframe. Does not work yet.. 
    #all_powerlines = all_powerlines.append(df[cols], ignore_index=True)
    
# MWh to TWh
results = results.divide(1000000)

# sort by row index   
results.sort_index(inplace=True)

################## plot fuels, imports, exports, load and storage stacked ############################################
# plot
results['load'] = results['load'].multiply(-1)
results['storage_in'] = results['storage_in'].multiply(-1)
results['export'] = results['export'].multiply(-1)
results['excess'] = results['excess'].multiply(-1)
results['csp'] = results['storage_csp_out'] + results['csp_direct']

# check whether balance fits
results.drop(['storage_level'], axis=1).sum(axis=1)

# rename columns
en_de = {'run_of_river': 'Run-of-the River Hydro Power',
         'storage_reservoir_out': 'Hydro Power with Reservoir',
         'biomass': 'Biomass',
         'solar': 'Solar PV',
         'wind': 'Wind',
         'csp': 'CSP',
         'geothermal': 'Geothermal',
         'gas': 'Natural Gas',
         'hard_coal': 'Hard Coal',
         'oil': 'Oil',
         'storage_in': 'Storage (Charge)',
         'storage_out': 'Storage (Discharge)',
         'import': 'Import',
         'export': 'Export',
         'load': 'Load',
         'shortage': 'Power Shortage',
         'excess': 'Power Surplus'}

results_de = results.rename(columns=en_de)

cols = ['Run-of-the River Hydro Power', 'Hydro Power with Reservoir', 'Biomass', 'Natural Gas', 'Hard Coal', 'Oil', 'Solar PV', 'Wind', 'CSP', 
        'Storage (Discharge)', 'Import', 'Power Shortage',
        'Load', 'Storage (Charge)', 'Export', 'Power Surplus']

results_de[cols].plot(kind='bar', stacked=True, cmap=cm.get_cmap('Spectral'))
#plt.title('Jährliche Stromproduktion nach Energieträgern')
plt.ylabel('Energy in TWh/a')
plt.legend(loc='lower center', bbox_to_anchor=(0.54, 1.04),
          ncol=5, fancybox=True, shadow=True)
plt.tight_layout()
plt.show()

#%% write results in csv
date = str(datetime.now())
date_date = date[0:10]
date_time = date[11:19]
date_time = date_time.replace(":", "-", 2)
date = date_date + '_' + date_time

     # sort columns and save as csv file
file_name = scenario_name + '_' + date + '_' + \
                 'all_countries' + '.csv'
results.sort_index(axis=1, inplace=True)
results.to_csv(os.path.join('results', file_name))

