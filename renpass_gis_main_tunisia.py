# -*- coding: utf-8 -*-
""" renpass_gis

Usage:
  renpass_gis_main_tunisia.py [options] NODE_DATA SEQ_DATA
  renpass_gis_main_tunisia.py -h | --help | --version

Examples:

  renpass_gis_main_tunisia.py -o cbc path/to/scenario.csv path/to/scenario_seq.csv

Arguments:

  NODE_DATA                  CSV-file containing data for nodes and flows.
  SEQ_DATA                   CSV-file with data for sequences.

Options:

  -h --help                  Show this screen and exit.
  -o --solver=SOLVER         Solver to be used. [default: cbc]
     --output-directory=DIR  Directory to write results to. [default: results]
     --date-from=TIMESTAMP   Start [default: '2014-01-01 00:00:00']
     --date-to=TIMESTAMP     End interval. [default: '2014-12-31 23:00:00']
     --version               Show version.

Full example 
  renpass_gis_main_tunisia.py -o cbc --date-from="2050-01-01 00:00:00" --date-to="2050-12-31 23:00:00" scenarios/tunisia_2050_scenario_a.csv scenarios/tunisia_2050_seq.csv
"""

import os
import logging
import pandas as pd

from datetime import datetime
from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph import NodesFromCSV
from oemof.outputlib import ResultsDataFrame
from docopt import docopt


###############################################################################
date = str(datetime.now())

### ANNOTATION: all comments marked with three hashtags have been added in January 2017

##arguments = {'NODE_DATA':'scenarios/tunisia_2050_scenario_a.csv',
#        'SEQ_DATA':'scenarios/tunisia_2050_seq.csv',
#       '-o cbci',
#      '--date-from':'2050-01-01 00:00:00',
#     '--date-to':'2050-01-31 23:00:00'}
             
             
def stopwatch():
    if not hasattr(stopwatch, 'now'):
        stopwatch.now = datetime.now()
        return None
    last = stopwatch.now
    stopwatch.now = datetime.now()
    return str(stopwatch.now-last)[0:-4]


def create_nodes(**arguments):
    """Creates nodes with their respective sequences

    Parameters
    ----------
    **arguments : key word arguments
        Arguments passed from command line
    """
    nodes = NodesFromCSV(file_nodes_flows=arguments['NODE_DATA'],
                         file_nodes_flows_sequences=arguments['SEQ_DATA'],
                         delimiter=',')

    return nodes


def create_energysystem(nodes, **arguments):
    """Creates the energysystem.

    Parameters
    ----------
    nodes:
        A list of entities that comprise the energy system
    **arguments : key word arguments
        Arguments passed from command line
    """

    datetime_index = pd.date_range(arguments['--date-from'],
                                   arguments['--date-to'],
                                   freq='60min')

    es = EnergySystem(entities=nodes,
                      groupings=GROUPINGS,
                      timeindex=datetime_index)

    return es


def simulate(es=None, **arguments):
    """Creates the optimization model, solves it and writes back results to
    energy system object

    Parameters
    ----------
    es : :class:`oemof.solph.network.EnergySystem` object
        Energy system holding nodes, grouping functions and other important
        information.
    **arguments : key word arguments
        Arguments passed from command line
    """

    om = OperationalModel(es)

    logging.info('OM creation time: ' + stopwatch())

    om.receive_duals()

    om.solve(solver=arguments['--solver'], solve_kwargs={'tee': True})

    logging.info('Optimization time: ' + stopwatch())

    return om


def write_results(es, om, **arguments):
    """Write results to CSV-files

    Parameters
    ----------
    es : :class:`oemof.solph.network.EnergySystem` object
        Energy system holding nodes, grouping functions and other important
        information.
    om : :class:'oemof.solph.models.OperationalModel' object for operational
        simulation with optimized dispatch
    **arguments : key word arguments
        Arguments passed from command line

    """
    # output: create pandas dataframe with results

    results = ResultsDataFrame(energy_system=es)

    # postprocessing: write complete result dataframe to file system

    if not os.path.isdir(arguments['--output-directory']):
        os.mkdir(arguments['--output-directory'])

    results_path = arguments['--output-directory']

###    date = str(datetime.now())

    #results_path = 'results/'

###    date = str(datetime.now())
    global date
    date_date = date[0:10]
    date_time = date[11:19]
    date_time = date_time.replace(":", "-", 2)
    date = date_date + '_' + date_time
    
    scenario_year = arguments['--date-from'][0:4]
    print("Scenario year: " + scenario_year)
    
    file_name = 'scenario_' + os.path.basename(arguments['NODE_DATA']).replace('.csv', '_') + date + '_' + \
                'results_complete.csv'
    
    results.to_csv(os.path.join(results_path, file_name))
    
    
    #  postprocessing: write dispatch and prices for all regions to file system
    
    # country codes
    country_codes = ['TNdr01', 'TNdr02', 'TNdr03', 'TNdr04', 'DZ', 'LY', 'IT', 'FR']
    
    for cc in country_codes:
    
        # build single dataframe for electric busses
        inputs = results.slice_unstacked(bus_label=cc + '_bus_el', type='to_bus',
                                         date_from=arguments['--date-from'], date_to=arguments['--date-to'],
                                         formatted=True)
    
        outputs = results.slice_unstacked(bus_label=cc + '_bus_el', type='from_bus',
                                          date_from=arguments['--date-from'], date_to=arguments['--date-to'],
                                          formatted=True)
    
        other = results.slice_unstacked(bus_label=cc + '_bus_el', type='other',
                                        date_from=arguments['--date-from'], date_to=arguments['--date-to'],
                                        formatted=True)
    
        # rename redundant columns
        inputs.rename(columns={cc + '_storage_phs': cc + '_storage_phs_out'},
                      inplace=True)
        outputs.rename(columns={cc + '_storage_phs': cc + '_storage_phs_in'},
                       inplace=True)
        other.rename(columns={cc + '_storage_phs': cc + '_storage_phs_level'},
                     inplace=True)
        inputs.rename(columns={cc + '_storage_battery': cc + '_storage_battery_out'},
                      inplace=True)
        outputs.rename(columns={cc + '_storage_battery': cc + '_storage_battery_in'},
                       inplace=True)
        other.rename(columns={cc + '_storage_battery': cc + '_storage_battery_level'},
                     inplace=True)
        inputs.rename(columns={cc + '_reservoir': cc + '_storage_reservoir_out'},
                      inplace=True)
        outputs.rename(columns={cc + '_reservoir': cc + '_storage_reservoir_in'},
                       inplace=True)
        other.rename(columns={cc + '_reservoir': cc + '_storage_reservoir_level'},
                     inplace=True)
        inputs.rename(columns={cc + '_cspstorage': cc + '_storage_csp_out'},
                      inplace=True)
        outputs.rename(columns={cc + '_cspstorage': cc + '_storage_csp_in'},
                       inplace=True)
        other.rename(columns={cc + '_cspstorage': cc + '_storage_csp_level'},
                     inplace=True)
    
        # data from model in MWh
        country_data = pd.concat([inputs, outputs, other], axis=1)
    
        # sort columns and save as csv file
        file_name = 'scenario_' + os.path.basename(arguments['NODE_DATA']).replace('.csv', '_') + date + '_' +\
                    cc + '.csv'
        country_data.sort_index(axis=1, inplace=True)
        country_data.to_csv(os.path.join(results_path, file_name))
        
    return


def main(**arguments):
    """
    """
    logging.info('Starting renpass_gis!')

    stopwatch()

    # create nodes from csv
    nodes = create_nodes(**arguments)

    # create energy system and pass nodes
    es = create_energysystem(nodes.values(), **arguments)

    # create optimization model and solve it
    om = simulate(es=es, **arguments)

    # write results in output directory
    write_results(es=es, om=om, **arguments)
    logging.info('Done! \n Check the results')

    return


###############################################################################

if __name__ == '__main__':
    arguments = docopt(__doc__, version='renpass_gis v0.1')
    print(arguments)
    logger.define_logging()
    main(**arguments)

###############################################################################

### Postprocessing: preparation
region01 = 'TNdr01'
region02 = 'TNdr02'
region03 = 'TNdr03'
region04 = 'TNdr04'
country01 = 'DZ'
country02 = 'LY'
country03 = 'IT'
country04 = 'FR' 
countrycode = 'TN'


### 1st postprocessing: summarize regional results to national result

# %% import result complete csv and get just national data, those including all regions
import os
###from datetime import datetime
os.chdir('/home/virtuallinux/renpass_gis/')
import pandas as pd 

# %% configuration
scenario_name = os.path.basename(arguments['NODE_DATA']).replace('.csv', '_')

scenario_timestamp = date

scenario_path = 'results/scenario_' + scenario_name + date + '_results_complete.csv'
df = pd.read_csv(scenario_path)

country_region = countrycode + 'dr'
idx = df.bus_label.str.contains(country_region)

#%% create dataframe and replace TNdr01 and so on (number: regular expresseion) with TN
df = df[idx]

df = df.replace('TNdr\d\d', value='TN', regex = True)

#%% sum up all the dispatch region to get hourly data for whole Tunisia for each technology
df = df.groupby(['bus_label','type','obj_label','datetime']).sum()


# %% slice dataframe into inputs, outputs and other and create columns for each obj_label

# slicing
idx = pd.IndexSlice

inputs = df.loc[idx[
            :,
            'to_bus',
            :,
            :],:]

outputs = df.loc[idx[
            :,
            'to_bus',
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
inputs.rename(columns={countrycode + '_storage_battery': countrycode + '_storage_battery_out'},
              inplace=True)
outputs.rename(columns={countrycode + '_storage_battery': countrycode + '_storage_batterxy_in'},
               inplace=True)
other.rename(columns={countrycode + '_storage_battery': countrycode + '_storage_battery_level'},
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
###date = str(datetime.now())
date_date = date[0:10]
date_time = date[11:19]
date_time = date_time.replace(":", "-", 2)
date = date_date + '_' + date_time

# sort columns and save as csv file
file_name = 'scenario_' + scenario_name + date + '_' + \
                 countrycode + '.csv'
country_data.sort_index(axis=1, inplace=True)
country_data.to_csv(os.path.join('results', file_name))


###############################################################################

### 2nd postprocessing: summarize regional results to annual sums and plot regional annual results

import pdb
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm

import os
os.chdir('/home/virtuallinux/renpass_gis')

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


file_name01 = 'scenario_' + scenario_name + scenario_timestamp + '_' + region01 + '.csv'
file_name02 = 'scenario_' + scenario_name + scenario_timestamp + '_' + region02 + '.csv'
file_name03 = 'scenario_' + scenario_name + scenario_timestamp + '_' + region03 + '.csv'
file_name04 = 'scenario_' + scenario_name + scenario_timestamp + '_' + region04 + '.csv'

files = {
    region01: file_name01,
    region02: file_name02,
    region03: file_name03,
    region04: file_name04}


# define fuels 
fuels = ['run_of_river', 'reservoir_out', 'biomass', 'solar', 'wind', 'geothermal',
         'gas', 'hard_coal', 'oil', 'csp_direct', 'storage_csp_out', 'storage_reservoir_out',
         'load', 'excess', 
         'shortage']


# create dataframe with fuels, import, export and storage as columns
results = pd.DataFrame(columns=fuels+['import', 'export', 'storage_phs_in', 'storage_phs_out', 'storage_phs_level', 
    'storage_battery_in', 'storage_battery_out', 'storage_battery_level'])
all_powerlines = pd.DataFrame()

# loop through all countries
for k, v in files.items():
    df = pd.read_csv('results/' + v, parse_dates=[0],
                     index_col=0, keep_date_col=True)
    
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
        
# MWh to TWh
results = results.divide(1000000)

# sort by row index   
results.sort_index(inplace=True)

################## plot fuels, imports, exports, load and storage stacked ############################################
# plot
results['load'] = results['load'].multiply(-1)
results['storage_phs_in'] = results['storage_phs_in'].multiply(-1)
results['storage_battery_in'] = results['storage_battery_in'].multiply(-1)
results['export'] = results['export'].multiply(-1)
results['excess'] = results['excess'].multiply(-1)
results['csp'] = results['csp_direct'] + results['storage_csp_out']

# check if balance fits
results.drop(['storage_level'], axis=1).sum(axis=1)

# rename columns
en_de = {'run_of_river': 'Run-of-the-River Hydro Power',
         'storage_reservoir_out': 'Hydro Power with Reservoir',
         'biomass': 'Biomass',
         'solar': 'Solar PV',
         'wind': 'Wind',
         'geothermal': 'Geothermal',
         'gas': 'Natural Gas',
         'hard_coal': 'Hard Coal',
         'oil': 'Oil',
         'storage_phs_in': 'PHStorage (Charge)',
         'storage_phs_out': 'PHStorage (Discharge)',
         'storage_battery_in': 'Battery storage (Charge)',
         'storage_battery_out': 'Battery storage (Discharge)',
         'csp': 'CSP',
         'import': 'Import',
         'export': 'Export',
         'load': 'Load',
         'shortage': 'Power Shortage',
         'excess': 'Power Surplus'}

results_de = results.rename(columns=en_de)

cols = ['Run-of-the-River Hydro Power', 'Hydro Power with Reservoir', 'Biomass', 'Solar PV', 'Wind', 
    'Natural Gas', 'Hard Coal', 'Oil', 
    'PHStorage (Charge)', 
    'PHStorage (Discharge)',
    'Battery storage (Charge)',
    'Battery storage (Discharge)',
    'CSP', 'Import', 'Export', 'Load', 'Power Shortage', 'Power Surplus']

results_de[cols].plot(kind='bar', stacked=True, cmap=cm.get_cmap('Spectral'))
plt.title('Annual power production by energy source')
plt.ylabel('Energy in TWh')
#plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
#          ncol=5, fancybox=True, shadow=True)

plt.legend()
plt.tight_layout()

#%% write results in csv
###date = str(datetime.now())
###date_date = date[0:10]
###date_time = date[11:19]
###date_time = date_time.replace(":", "-", 2)
###date = date_date + '_' + date_time

     # sort columns and save as csv file
file_name = 'scenario_' + scenario_name + date + '_' + \
                 'all_regions_annual_sums'
file_name_full = file_name + '.csv'

results.sort_index(axis=1, inplace=True)
results.to_csv(os.path.join('results', file_name_full))

fig1 = plt.gcf()
###plt.show()
plt.draw()
fig1.savefig("results/" + file_name +".png", dpi=100)

#NEW 
# create dataframe with fuels, import, export and storage as columns
resultsmax = pd.DataFrame(columns=fuels+['import', 'export', 'storage_phs_in', 'storage_phs_out', 'storage_phs_level', 
    'storage_battery_in', 'storage_battery_out', 'storage_battery_level'])
all_powerlines = pd.DataFrame()
# loop through all countries
for k, v in files.items():
    df = pd.read_csv('results/' + v, parse_dates=[0],
                     index_col=0, keep_date_col=True)
    
    # create for every country maximum values of each column
    max_per_country = df.max()
    
    max_per_country_fuels = df.max()
    
    # create resultsmax dataframe with countries as rows and fuels as columns         
    for f in fuels:
        resultsmax.ix[k, f] = [max_per_country_fuels[i] for i in max_per_country_fuels.index 
                      if f in i]

# sort by row index   
resultsmax.sort_index(inplace=True)

print(resultsmax)
     # sort columns and save as csv file
file_name = 'scenario_' + scenario_name + date + '_' + \
                 'all_regions_annual_max'
file_name_full = file_name + '.csv'

resultsmax.sort_index(axis=1, inplace=True)
resultsmax.to_csv(os.path.join('results', file_name_full))

###############################################################################

### 3rd postprocessing: summarize country results to annual sums and plot annual results

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

file01 = 'scenario_' + scenario_name + date + '_' + country01 + '.csv'
file02 = 'scenario_' + scenario_name + date + '_' + country02 + '.csv'
file03 = 'scenario_' + scenario_name + date + '_' + country03 + '.csv'
file04 = 'scenario_' + scenario_name + date + '_' + country04 + '.csv'

files = {
    country01: file01,
    country02: file02,
    country03: file03,
    country04: file04}


# define fuels 
fuels = ['run_of_river', 'storage_reservoir_out', 'biomass', 'solar', 'wind', 'csp_direct', 'storage_csp_out', 'storage_battery_out', 'geothermal', 'gas', 'hard_coal', 'oil', 'load', 'excess', 
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
#plt.title('Annual power generation (by fuels)')
plt.ylabel('Energy in TWh/a')
#plt.legend(loc='lower center', bbox_to_anchor=(0.54, 1.04),
#          ncol=5, fancybox=True, shadow=True)
plt.legend()
plt.tight_layout()

#%% write results in csv

     # sort columns and save as csv file
file_name = 'scenario' + '_' + scenario_name + date + '_' + \
                 'all_countries_annual_sums'
file_name_full = file_name + '.csv'
results.sort_index(axis=1, inplace=True)
results.to_csv(os.path.join('results', file_name_full))

fig2 = plt.gcf()
###plt.show()
plt.draw()
fig2.savefig("results/" + file_name +".png", dpi=100)


###############################################################################

### 4th postprocessing: hourly resolved plot

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
file = 'results/scenario_' + scenario_name + date + '_' + countrycode + '.csv'

df_raw = pd.read_csv(file, parse_dates=[0], index_col=0, keep_date_col=True)
df_raw.head()
df_raw.columns



# %% dispatch plot 

# country code
cc = countrycode

# get fossil and renewable power plants
fuels = ['run_of_river', 'biomass', 'solar', 
         'wind', 'hydro_reservoir', 'csp_direct', 'storage_csp_out', 'storage_battery_out', 'gas', 'hard_coal', 'oil', 'storage_out', 'shortage']

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
#plt.legend(loc='lower center', bbox_to_anchor=(0.54, 1.04),
#          ncol=5, fancybox=True, shadow=True)
plt.legend()
plt.xlabel('Date')
plt.ylabel('Power in  GW')
plt.ylim(0, max(dispatch_de.sum(axis=1)))

file_name = 'scenario' + '_' + scenario_name + date + '_' + \
                 cc + '_hourly_resolved'

fig3 = plt.gcf()
plt.show()
plt.draw()
fig3.savefig("results/" + file_name +".png", dpi=100)

