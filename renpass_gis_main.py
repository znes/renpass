# -*- coding: utf-8 -*-
""" renpass_gis

Usage:
  renpass_gis_main.py [options] DATAPACKAGE
  renpass_gis_main.py -h | --help | --version

Examples:

  renpass_gis_main.py -o glpk path/to/datapackage.json

Arguments:

  DATAPACKAGE                valid datapackage with input data

Options:

  -h --help                  Show this screen and exit.
  -o --solver=SOLVER         Solver to be used. [default: cbc]
     --output-directory=DIR  Directory to write results to. [default: results]
     --version               Show version.
"""

import os
import logging
import pandas as pd

from datapackage import Package
from datetime import datetime

import facades

from oemof.tools import logger
from oemof.solph import Model, EnergySystem, Bus
from oemof.outputlib import processing, views

try:
    from docopt import docopt
except ImportError:
    print("Unable to load docopt. Is docopt installed?")


###############################################################################

def stopwatch():
    if not hasattr(stopwatch, 'now'):
        stopwatch.now = datetime.now()
        return None
    last = stopwatch.now
    stopwatch.now = datetime.now()
    return str(stopwatch.now-last)[0:-4]


def create_energysystem(datapackage, **arguments):
    """Creates the energysystem.

    Parameters
    ----------
    datapackage: str
        path to datapackage metadata file in JSON format
    **arguments : key word arguments
        Arguments passed from command line
    """

    es = EnergySystem.from_datapackage(
        arguments['DATAPACKAGE'],
        attributemap={
            facades.Demand: {'demand-profiles': 'profile'},
            facades.Generator: {"generator-profiles": "profile"},
            facades.RunOfRiver: {"run-of-river-inflows": "inflow"}},
        typemap={
            'bus': Bus,
            'demand': facades.Demand,
            'generator': facades.Generator,
            'storage': facades.Storage,
            'reservoir': facades.Reservoir,
            'backpressure': facades.CHP,
            'connection': facades.Connection,
            'conversion': facades.Conversion,
            'runofriver': facades.RunOfRiver})

    return es


def compute(es=None, **arguments):
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

    m = Model(es)

    logging.info('Model creation time: ' + stopwatch())

    #m.receive_duals()

    m.solve(solver=arguments['--solver'], solve_kwargs={'tee': True})

    logging.info('Optimization time: ' + stopwatch())

    return m


def write_results(es, m, p, **arguments):
    """Write results to CSV-files

    Parameters
    ----------
    es : :class:`oemof.solph.network.EnergySystem` object
        Energy system holding nodes, grouping functions and other important
        information.
    m : A solved :class:'oemof.solph.models.Model' object for dispatch or
     investment optimization
    **arguments : key word arguments
        Arguments passed from command line
    p: datapackage.Package instance of the input datapackage
    """
    # output: create pandas dataframe with results

    results = processing.results(m)

    # postprocessing: write complete result dataframe to file system

    if not os.path.isdir(arguments['--output-directory']):
        os.mkdir(arguments['--output-directory'])

    output_base_directory = arguments['--output-directory']

    date = datetime.now().strftime("%Y-%m-%d %H-%M-%S").replace(' ', '_')

    filename = p.descriptor['name'].replace(' ', '_') + '.xls'

    xls_file = os.path.join(output_base_directory, filename)

    logging.info('Exporting result object to Excel.')

    writer = pd.ExcelWriter(xls_file, engine='xlsxwriter')

    # add regular optimization results
    nodes = sorted(set([item
                        for tup in results.keys()
                        for item in tup]))

    for n in nodes:
        if isinstance(n, (Bus, facades.Storage)):
            node_data = views.node(results, str(n), multiindex=True)

            n = str(n)[:20]  # trim string length to allowed chars for a worksheet
            if 'scalars' in node_data:
                node_data['scalars'].to_excel(writer, sheet_name=str(n)+'_scalars')
            if 'sequences' in node_data:
                node_data['sequences'].to_excel(writer, sheet_name=str(n)+'_sequences')

    writer.save()

    return True



def main(**arguments):
    """
    """
    logging.info('Starting renpass_gis!')

    stopwatch()

    p = Package(arguments['DATAPACKAGE'])

    # create energy system and pass nodes
    es = create_energysystem(arguments['DATAPACKAGE'], **arguments)

    # create optimization model and solve it
    m = compute(es=es, **arguments)

    # write results in output directory
    write_results(es, m=m, p=p, **arguments)

    logging.info('Done! \n Check the results')

    return



###############################################################################

if __name__ == '__main__':
    arguments = docopt(__doc__, version='renpass_gis v0.2')
    logger.define_logging()
    main(**arguments)
