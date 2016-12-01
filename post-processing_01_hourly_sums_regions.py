# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 2016

@author: doziimbos
"""
# %% import result complete csv and get just German data, those including DEdr
import os
from datetime import datetime
os.chdir('C:/Users/doziimbos/renpass_gis/')
import pandas as pd 

# %% configuration
scenario_name = 'scenario_morocco_2050_scenario_test001'
scenario_timestamp = '2016-12-01_09-50-21'
countrycode = 'MA'

scenario_path = 'results/' + scenario_name + '_' + scenario_timestamp + '_results_complete.csv'

df = pd.read_csv(scenario_path)

country_region = countrycode + 'dr'
idx = df.bus_label.str.contains(country_region)

#%% create dataframe and replace DEdr01 and so on (number: regular expresseion) with DE
df = df[idx]

df = df.replace('MAdr\d\d', value='MA', regex = True)

#%% sum up all the dispatch region to get hourly data for whole Germany for each technology
df = df.groupby(['bus_label','type','obj_label','datetime']).sum()


# %% slice dataframe into inputs, outputs and other and create columns for each obj_label

# slicing
idx = pd.IndexSlice

inputs = df.loc[idx[
            :,
            'input',
            :,
            :],:]

outputs = df.loc[idx[
            :,
            'output',
            :,
            :],:]

other = df.loc[idx[
            :,
            'other',
            :,
            :],:]

inputs = inputs.unstack('obj_label')
outputs = outputs.unstack('obj_label')
other = other.unstack('obj_label')
 
# %% reset the index to bus_label and type and get unique level values so the csv can write the columns next to each other

inputs.reset_index(level=['bus_label', 'type'], drop=True,
                               inplace=True)
inputs.columns = inputs.columns.get_level_values(1).unique()

outputs.reset_index(level=['bus_label', 'type'], drop=True,
                               inplace=True)
outputs.columns = outputs.columns.get_level_values(1).unique()

other.reset_index(level=['bus_label', 'type'], drop=True,
                               inplace=True)
other.columns = other.columns.get_level_values(1).unique()

#%%

 # rename redundant columns
inputs.rename(columns={countrycode + '_storage_pumped_hydro': countrycode + '_storage_pumped_hydro_out'},
               inplace=True)
inputs.rename(columns={countrycode + '_storage_a_caes': countrycode + '_storage_a_caes_out'},
               inplace=True)
inputs.rename(columns={countrycode + '_storage_hydrogen': countrycode + '_storage_hydrogen_out'},
               inplace=True)
inputs.rename(columns={countrycode + '_storage_lithium_ion': countrycode + '_storage_lithium_ion_out'},
               inplace=True)
inputs.rename(columns={countrycode + '_storage_redox_flow': countrycode + '_storage_redox_flow_out'},
               inplace=True)
outputs.rename(columns={countrycode + '_storage_pumped_hydro': countrycode + '_storage_pumped_hydro_in'},
                inplace=True)
outputs.rename(columns={countrycode + '_storage_a_caes': countrycode + '_storage_a_caes_in'},
               inplace=True)
outputs.rename(columns={countrycode + '_storage_hydrogen': countrycode + '_storage_hydrogen_in'},
               inplace=True)
outputs.rename(columns={countrycode + '_storage_lithium_ion': countrycode + '_storage_lithium_ion_in'},
               inplace=True)
outputs.rename(columns={countrycode + '_storage_redox_flow': countrycode + '_storage_redox_flow_in'},
               inplace=True)
other.rename(columns={countrycode + '_storage_pumped_hydro': countrycode + '_storage_pumped_hydro_level'},
              inplace=True)
other.rename(columns={countrycode + '_storage_a_caes': countrycode + '_storage_a_caes_level'},
               inplace=True)
other.rename(columns={countrycode + '_storage_hydrogen': countrycode + '_storage_hydrogen_level'},
               inplace=True)
other.rename(columns={countrycode + '_storage_lithium_ion': countrycode + '_storage_lithium_ion_level'},
               inplace=True)
other.rename(columns={countrycode + '_storage_redox_flow': countrycode + '_storage_redox_flow_level'},
               inplace=True)

# rename redundant columns
inputs.rename(columns={countrycode + '_storage_phs': countrycode + '_storage_phs_out'},
              inplace=True)
outputs.rename(columns={countrycode + '_storage_phs': countrycode + '_storage_phs_in'},
               inplace=True)
other.rename(columns={countrycode + '_storage_phs': countrycode + '_storage_phs_level'},
             inplace=True)
inputs.rename(columns={countrycode + '_reservoir': countrycode + '_storage_reservoir_out'},
              inplace=True)
outputs.rename(columns={countrycode + '_reservoir': countrycode + '_storage_reservoir_in'},
               inplace=True)
other.rename(columns={countrycode + '_reservoir': countrycode + '_storage_reservoir_level'},
             inplace=True)
inputs.rename(columns={countrycode + '_cspstorage': countrycode + '_storage_csp_out'},
              inplace=True)
outputs.rename(columns={countrycode + '_cspstorage': countrycode + '_storage_csp_in'},
               inplace=True)
other.rename(columns={countrycode + '_cspstorage': countrycode + '_storage_csp_level'},
             inplace=True)
                 
     # data from model in MWh
country_data = pd.concat([inputs, outputs, other], axis=1)

#%%
date = str(datetime.now())
date_date = date[0:10]
date_time = date[11:19]
date_time = date_time.replace(":", "-", 2)
date = date_date + '_' + date_time

     # sort columns and save as csv file
file_name = scenario_name + '_' + date + '_' + \
                 countrycode + '.csv'
country_data.sort_index(axis=1, inplace=True)
country_data.to_csv(os.path.join('results', file_name))

