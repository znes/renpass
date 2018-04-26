# -*- coding: utf-8 -*-
""" renpass

Usage:
  renpass.py [options] DATAPACKAGE
  renpass.py -h | --help | --version

Examples:

  renpass_gis_main.py -o glpk path/to/datapackage.json

Arguments:

  DATAPACKAGE                valid datapackage with input data

Options:

  -h --help                  Show this screen and exit.
  -o --solver=SOLVER         Solver to be used. [default: cbc]
     --output-directory=DIR  Directory to write results to. [default: results]
     --output-orient=ORIENT  Bus- or component-oriented results. [default: component]
     --version               Show version.
     --results=RESULTS       How should results be saved [default: datapackage]
  -s --safe                  If argument --safe is set, results will not be
                             overwritten
  -d --debug                 If set debug mode is turned on
     --t_start=T_START       Start timestep of simulation [default: 0]
     --t_end=T_END           End timestep of simulation, default is last
                             timestep of datapackage timeindex [default: -1]
"""

from datapackage import Package
from datetime import datetime
from itertools import chain
import logging
import os
import pandas as pd

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

    typemap = {
        'bus': facades.Hub,
        'extraction-turbine': facades.ExtractionTurbine,
        'demand': facades.Demand,
        'generator': facades.Generator,
        'storage': facades.Storage,
        'reservoir': facades.Reservoir,
        'backpressure': facades.Backpressure,
        'connection': facades.Connection,
        'conversion': facades.Conversion,
        'runofriver': facades.Generator,
        'excess': facades.Excess}

    es = EnergySystem.from_datapackage(
        arguments['DATAPACKAGE'],
        attributemap={
            facades.Demand: {'demand-profiles': 'profile'},
            facades.Generator: {"generator-profiles": "profile"},
            facades.RunOfRiver: {"run-of-river-inflows": "inflow"}},
        typemap=typemap)

    es._typemap = typemap

    end = es.timeindex.get_loc(es.timeindex[int(arguments['--t_end'])]) + 1

    es.timeindex = es.timeindex[int(arguments['--t_start']):end]

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

    m.receive_duals()

    if arguments['--debug']:
        filename  = 'renpass_model.lp'
        logging.info('Writing lp-file to {}.'.format(filename))
        m.write(filename,
                io_options={'symbolic_solver_labels': True})

    m.solve(solver=arguments['--solver'], solve_kwargs={'tee': True})

    logging.info('Optimization time: ' + stopwatch())

    return m

def links(es):
    """
    """
    buses = [n for n in es.nodes if isinstance(n, facades.Connection)]
    links = list()
    for b in buses:
        for i in b.inputs:
            for o in b.outputs:
                if o != i:
                    links.append((i, o))
    return links

def _edges(nodes):
    """
    """
    edges = {}
    for n in nodes:
        edges[str(n)] = []
        for o in n.outputs:
            edges[str(n)].append((n, o))
        for i in n.inputs:
            edges[str(n)].append((i, n))
    return edges

def component_results(es, results, path):
    for k,v in es._typemap.items():
        if type(k) == str:
            _seq_by_type = [
                views.node(results, n, multiindex=True)['sequences']
                for n in es.nodes if isinstance(n, v) and not isinstance(n, Bus)]
            if _seq_by_type:
                seq_by_type =  pd.concat(_seq_by_type, axis=1)
                type_path = os.path.join(path, 'sequences')
                if not os.path.exists(type_path):
                    os.makedirs(type_path)
                seq_by_type.to_csv(
                    os.path.join(type_path, str(k) + '.csv'), sep=";")

            _sca_by_type = [
                views.node(results, n, multiindex=True).get('scalars')
                for n in es.nodes if isinstance(n, v) and not isinstance(n, Bus)]

            if [x for x in _sca_by_type if x is not None]:
                sca_by_type =  pd.concat(_sca_by_type)
                type_path = os.path.join(path, 'scalars')
                if not os.path.exists(type_path):
                    os.makedirs(type_path)
                sca_by_type.to_csv(
                    os.path.join(type_path, str(k) + '.csv'), header=True,
                                 sep=";")

def bus_results(es, results, path):
    buses = [b for b in es.nodes if isinstance(b, Bus)]
    for b in buses:
        bus_sequences = pd.concat([
            views.node(results, b, multiindex=True)['sequences']], axis=1)
        type_path = os.path.join(path, 'sequences')
        if not os.path.exists(type_path):
            os.makedirs(type_path)
        bus_sequences.to_csv(
            os.path.join(type_path, str(b) + '.csv'), sep=";")


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

    modelname = p.descriptor['name'].replace(' ', '_')

    logging.info('Exporting result object to CSV.')

    package_root_directory = os.path.join(output_base_directory, modelname)


    # -----------------------------------------------------------------------
    # Default results
    # -----------------------------------------------------------------------
    _write_results = {'component': component_results, 'bus': bus_results} \
        [arguments['--output-orient']]
    _write_results(es, results, path=package_root_directory)

    # -----------------------------------------------------------------------
    # Derived results
    # -----------------------------------------------------------------------
    # transshipment / network export
    conns = _edges([n for n in es.nodes
                    if isinstance(n, facades.Connection)])

    transshipment = pd.concat(
        [views.node(results, n, multiindex=True)['sequences'].\
            loc[:, (n, slice(None), 'flow')]
         for n in conns], axis=1).groupby(level=['from'], axis=1).sum()

    transshipment_path = os.path.join(
        package_root_directory, 'data', 'derived')
    if not os.path.exists(transshipment_path):
        os.makedirs(transshipment_path)

    transshipment.to_csv(
        os.path.join(transshipment_path, 'transshipment.csv'), sep=";")

    # storage output
    storages = {
        n: views.node(results, n, multiindex=True)['sequences']
        for n in es.nodes if isinstance(n, facades.Storage)}
    storage_edges = _edges(storages.keys())
    for k, v in storages.items():
        # TODO: prettify column renaming
        new_columns = []
        for tup in tuple(v.columns):
            if k == tup[0] and tup[2] == 'flow':
                new_columns.append('output')
            elif k == tup[1] and tup[2] == 'flow':
                new_columns.append('input')
            else:
                new_columns.append('level')
        v.columns = new_columns
        v.to_csv(
            os.path.join(transshipment_path, str(k) + '.csv'), sep=";")

    # TODO prettify / complete package (meta-data) creation
    if arguments['--results'] == 'datapackage':
        # results package (rp)
        rp = Package()
        rp.infer(os.path.join(package_root_directory, 'data', 'derived', '**/*.csv'))
        rp.descriptor['description'] = "Model results from renpass with version..."
        rp.descriptor['name'] = modelname + '-results'
        rp.commit()
        rp.save(os.path.join(package_root_directory, 'datapackage.json'))

    return True



def main(**arguments):
    """
    """
    logging.info('Starting renpass!')

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
    arguments = docopt(__doc__, version='renpass v0.2')
    logger.define_logging()
    main(**arguments)
