# -*- coding: utf-8 -*-

""" This module contains functions to postprocess (aggregate, etc.) results
from the model.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import os

import pandas as pd

from oemof.network import Bus
from oemof.solph.components import GenericStorage
from oemof.outputlib import views, processing
from . import facades, components

def read_results(path):
    """
    """
    pass


def line_results(es, results, select='sequences'):
    """
    """
    lines = [l for l in es.nodes
             if isinstance(l, components.electrical.Line)]

    df = pd.concat([results[line.input, line.output][select]
                    for line in lines], axis=1)

    df.columns = [line.input.label + '-' + line.output.label for line in lines]

    return df


def component_results(es, results, select='sequences'):
    """ Aggregated by component type
    """

    c = {}

    for k, v in es.typemap.items():
        if type(k) == str:
            if select == 'sequences':
                _seq_by_type = [
                    views.node(results, n, multiindex=True).get('sequences')
                    for n in es.nodes if isinstance(n, v) and not isinstance(n, Bus)]
                # check if dataframes / series have been returned
                if any([isinstance(i, (pd.DataFrame, pd.Series))
                       for i in _seq_by_type]):
                    seq_by_type =  pd.concat(_seq_by_type, axis=1)
                    c[str(k)] = seq_by_type

            if select == 'scalars':
                _sca_by_type = [
                    views.node(results, n, multiindex=True).get('scalars')
                    for n in es.nodes if isinstance(n, v) and not isinstance(n, Bus)]

                if [x for x in _sca_by_type if x is not None]:
                    sca_by_type =  pd.concat(_sca_by_type)
                    c[str(k)] = _sca_by_type

    return c

def bus_results(es, results, select='sequences', aggregate=False):
    """ Aggregated for every bus of the energy system
    """
    br = {}

    buses = [b for b in es.nodes if isinstance(b, Bus)]

    for b in buses:
        if select == 'sequences':
            bus_sequences = pd.concat([
                views.node(results, b, multiindex=True).get('sequences',
                                                            pd.DataFrame())], axis=1)
            br[str(b)] = bus_sequences
        if select == 'scalars':
            br[str(b)] = views.node(results, b, multiindex=True).get('scalars')

    if aggregate:
        if select == 'sequences':
            axis = 1
        else:
            axis = 0
        br = pd.concat([b for b in br.values()], axis=axis)

    return br

def supply_results(path=None, types=['dispatchable', 'volatile', 'conversion',
                                     'backpressure', 'extraction', 'storage',
                                     'generator', 'reservoir'],
                   bus=None, results=None, es=None):
    """
    """
    if path is None and results is None:
        raise ValueError('You need to specifiy either path or results!')

    selection = pd.DataFrame()

    if path:
        for t in types:
            result = pd.read_csv(
                os.path.join(path, t + '.csv'),
                sep=";", header=[0, 1, 2], index_col=0, parse_dates=True)

            selection = pd.concat(
                [selection,
                 result.xs([bus, 'flow'], axis=1, level=[1,2])], axis=1)

    else:
        for t in types:
            if t == 'storage':
                df = views.net_storage_flow(results,
                                            node_type=es.typemap[t])
                if df is not None:
                    selection = pd.concat([selection, df], axis=1)
            else:
                df = views.node_output_by_type(results,
                                               node_type=es.typemap[t])
                if df is not None:
                    selection = pd.concat([selection, df], axis=1)

        selection = selection.loc[:, (slice(None),
                                      [es.groups[b] for b in bus],
                                      ['flow', 'net_flow'])]
    return selection

def demand_results(path=None, types=['load'], bus=None, results=None, es=None):
    """
    """

    selection = pd.DataFrame()
    if path:
        for t in types:
            result = pd.read_csv(
                os.path.join(path, t + '.csv'),
                sep=";", header=[0, 1, 2], index_col=0, parse_dates=True)
            selection = pd.concat(
                [selection,
                 result.xs([bus, 'flow'], axis=1, level=[0,2])], axis=1)
    else:
        for t in types:
            selection = pd.concat(
                [selection,
                 views.node_input_by_type(results, node_type=es.typemap[t])],
                 axis=1)

        selection = selection.loc[:, ([es.groups[b] for b in bus],
                                     slice(None),
                                     ['flow'])]

    return selection

def storage_net_results(path, labels=[], store=True):
    """ Writes net results for storage components.

    path: str
        Path to storage component results.
    labels: list
        List of storage component labels.
    """

    storage_results = pd.read_csv(
        path, sep=";", header=[0, 1, 2], index_col=0, parse_dates=True)

    if not labels:
        x = storage_results.xs('capacity', axis=1, level=2).columns.values
        label = [s for s,t in x]

    dataframes = []

    for l in labels:

        grouper = lambda x: (lambda fr, to, ty:
                            'output' if (fr == l and ty == 'flow') else
                            'input' if (to == l and ty == 'flow') else
                            'level' if (fr == l and ty != 'flow') else
                            None) (*x)

        subset = storage_results.groupby(grouper, axis=1).sum()
        subset['net_input'] = subset['input'] - subset['output']
        subset['input'] = subset['net_input'].apply(lambda row: row if row > 0 else 0)
        subset['output'] = subset['net_input'].apply(lambda row: abs(row) if row < 0 else 0)
        subset.columns = pd.MultiIndex.from_product([[l], subset.columns])

        dataframes.append(subset)

    df = pd.concat(dataframes, axis=1)

    if store:
        df.to_csv(
            os.path.join(os.path.dirname(path), 'storage-processed' + '.csv'),
            sep=";", date_format='%Y-%m-%dT%H:%M:%SZ')
    else:
        return df


def link_net_results(path, hubs=[], store=True):
    """ Writes net results for link components.

    path: str
        Path to link component results.
    label: list
        List of hub labels.
    """

    link_results = pd.read_csv(
        path, sep=";", header=[0, 1, 2], index_col=0, parse_dates=True)

    df = pd.DataFrame()

    for hub in hubs:
        ex = link_results.loc[:, (hub, slice(None), 'flow')].sum(axis=1)
        im = link_results.loc[:, (slice(None), hub, 'flow')].sum(axis=1)

        df[hub + '-' + 'net-import'] = im - ex

    if store:
        df.to_csv(
            os.path.join(os.path.dirname(path), 'link-processed' + '.csv'),
            sep=";", date_format='%Y-%m-%dT%H:%M:%SZ')
    else:
        return df


def links(es):
    """
    """
    buses = [n for n in es.nodes if isinstance(n, facades.Link)]
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

def write_results(es, results, results_path):
    """
    """
    writer = pd.ExcelWriter(os.path.join(results_path, 'results.xlsx'))

    buses = [b.label for b in es.nodes if isinstance(b, Bus)]

    # write suppy results with net-import per bus
    link_results = component_results(es, results).get('link')

    for b in buses.index:
        supply = supply_results(results=results, es=es, bus=[b])
        supply.columns = supply.columns.droplevel([1, 2])

        if link_results is not None and \
            es.groups[b] in list(link_results.columns.levels[0]):
            ex = link_results.loc[:, (es.groups[b], slice(None), 'flow')].sum(axis=1)
            im = link_results.loc[:, (slice(None), es.groups[b], 'flow')].sum(axis=1)
            supply['net_import'] =  im - ex

        supply.to_excel(writer, 'supply-' + b)

    # write installed capacities (including exogenously defined ones)
    all = bus_results(es, results, select='scalars', aggregate=True)
    all.name = 'value'
    endogenous = all.reset_index()
    endogenous['tech'] = [
        getattr(t, 'tech', np.nan) for t in all.index.get_level_values(0)]

    d = dict()
    for node in es.nodes:
        if not isinstance(node, (Bus, Sink)):
            if getattr(node, 'capacity', None) is not None:
                key = (node, [n for n in node.outputs.keys()][0], 'capacity', node.tech)
                d[key] = {'value': node.capacity}
    exogenous = pd.DataFrame.from_dict(d, orient='index').dropna()
    exogenous.index = exogenous.index.set_names(['from', 'to', 'type', 'tech'])

    capacities = pd.concat(
        [endogenous, exogenous.reset_index()]).groupby(['to', 'tech']).sum().unstack('to')
    capacities.columns = capacities.columns.droplevel(0)
    capacities.to_excel(writer, 'capacities')

    demand = demand_results(results=results, es=es, bus=buses)
    demand.columns = demand.columns.droplevel([0, 2])
    demand.to_excel(writer, 'load')

    duals = bus_results(es, results, aggregate=True).xs('duals', level=2, axis=1)
    duals.columns = duals.columns.droplevel(1)
    (duals.T / m.objective_weighting).T.to_excel(writer, 'shadow_prices')

    excess = component_results(es, results, select='sequences')['excess']
    excess.columns = excess.columns.droplevel([1, 2])
    excess.to_excel(writer, 'excess')

    filling_levels = views.node_weight_by_type(results, GenericStorage)
    filling_levels.columns = filling_levels.columns.droplevel(1)
    filling_levels.to_excel(writer, 'filling_levels')

    writer.save()
