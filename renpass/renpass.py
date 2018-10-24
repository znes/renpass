# -*- coding: utf-8 -*-

from datetime import datetime
from itertools import chain
import logging
import os

from datapackage import Package
import pandas as pd

from oemof.tools import logger
from oemof.solph import Model, EnergySystem, Bus
from oemof.outputlib import processing, views

from . import facades, options

try:
    from docopt import docopt
except ImportError:
    print("Unable to load docopt. Is docopt installed?")

###############################################################################

HELP = """ renpass

Usage:
  renpass [options] DATAPACKAGE
  renpass -h | --help | --version

Examples:

  renpass -o glpk path/to/datapackage.json

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
        attributemap={},
        typemap=options.typemap)

    es._typemap = options.typemap

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

    if es.temporal is not None:
        m = Model(es, objective_weighting=es.temporal['weighting'])
    else:
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

def component_results(es, results, path, model):
    """ Writes results aggregated by component type
    """
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

def bus_results(es, results, path, model):
    """ Writes results aggregated for every bus of the energy system
    """
    buses = [b for b in es.nodes if isinstance(b, Bus)]
    for b in buses:
        bus_sequences = pd.concat([
            views.node(results, b, multiindex=True)['sequences']], axis=1)
        type_path = os.path.join(path, 'sequences')
        if not os.path.exists(type_path):
            os.makedirs(type_path)
        bus_sequences.to_csv(
            os.path.join(type_path, str(b) + '.csv'), sep=";")

def default_results(es, results, path, model):
    """ Write multiindex dataframe with all results from the solved `model`
    """
    processing.create_dataframe(model).to_csv(
        os.path.join(path, 'results.csv'), sep=";")

def write_results(es, m, p, **arguments):
    """Write results to CSV-files

    Parameters
    ----------
    es : :class:`oemof.solph.network.EnergySystem` object
        Energy system holding nodes, grouping functions and other important
        information.
    m : A solved :class:'oemof.solph.models.Model' object for dispatch or
     investment optimization
    p: datapackage.Package instance of the input datapackage
    **arguments : key word arguments
        Arguments passed from command line
    """

    # get the model name for processing and storing results from input dpkg
    modelname = p.descriptor['name'].replace(' ', '_')

    output_base_directory = os.path.join(
        arguments['--output-directory'], modelname)

    if not os.path.isdir(output_base_directory):
        os.makedirs(output_base_directory)

    meta_results = processing.meta_results(m)

    meta_results_path = os.path.join(output_base_directory, 'problem.csv')

    logging.info('Exporting solver information to {}'.format(
        os.path.abspath(meta_results_path)))

    pd.DataFrame({
        'objective': {
            modelname: meta_results['objective']},
        'solver_time': {
            modelname: meta_results['solver']['Time']},
        'constraints': {
            modelname: meta_results['problem']['Number of constraints']},
        'variables': {
            modelname: meta_results['problem']['Number of variables']}})\
                .to_csv(meta_results_path)

    results = processing.results(m)

    _write_results = {
        'default': default_results,
        'component': component_results,
        'bus': bus_results} \
        [arguments['--output-orient']]

    logging.info('Exporting results to {}'.format(
        os.path.abspath(output_base_directory)))

    _write_results(es, results, path=output_base_directory, model=m)

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
    arguments = docopt(HELP, version='renpass v0.3')

    logger.define_logging()

    main(**arguments)
