# -*- coding: utf-8 -*-

""" This module contains functions to postprocess (aggregate, etc.) results
from the model.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import os

import pandas as pd

from oemof.network import Bus
from oemof.outputlib import views
from . import facades

def read_results(path):
    """
    """
    pass


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
                if _seq_by_type:
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

def supply_results(path=None, types=['dispatchable', 'volatile',
                                     'backpressure', 'extraction', 'storage'],
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


def connection_net_results(path, hubs=[], store=True):
    """ Writes net results for connection components.

    path: str
        Path to connection component results.
    label: list
        List of hub labels.
    """

    connection_results = pd.read_csv(
        path, sep=";", header=[0, 1, 2], index_col=0, parse_dates=True)

    df = pd.DataFrame()

    for hub in hubs:
        ex = connection_results.loc[:, (hub, slice(None), 'flow')].sum(axis=1)
        im = connection_results.loc[:, (slice(None), hub, 'flow')].sum(axis=1)

        df[hub + '-' + 'net-import'] = im - ex

    if store:
        df.to_csv(
            os.path.join(os.path.dirname(path), 'connection-processed' + '.csv'),
            sep=";", date_format='%Y-%m-%dT%H:%M:%SZ')
    else:
        return df


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


def system_info(es, path=None):
    """
    """
    d = {}
    for n in es.nodes:
        d[n.label] = {
            'type': n.type,
            'tech': getattr(n, 'tech', None),
            'mapped_type': getattr(n, 'mapped_type', None),
            'carrier': getattr(n, 'carrier', None)
        }

    df = pd.DataFrame.from_dict(d, orient='index')

    if path:
        df.to_csv(os.path.join(path, 'es_information.csv'))
        return True
    else:
        return pd.DataFrame.from_dict(d, orient='index')
