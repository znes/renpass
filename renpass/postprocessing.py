# -*- coding: utf-8 -*-

""" This module contains functions to postprocess (aggregate, etc.) results
from the model.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import os

import pandas as pd


def supply_results(path, types=['dispatchable', 'volatile'], bus=None):
    """
    """

    selection = pd.DataFrame()
    for t in types:
        result = pd.read_csv(
            os.path.join(path, t + '.csv'),
            sep=";", header=[0, 1, 2], index_col=0, parse_dates=True)
        selection = pd.concat(
            [selection,
             result.xs([bus, 'flow'], axis=1, level=[1,2])], axis=1)
    return selection

def demand_results(path, types=['load'], bus=None):
    """
    """

    selection = pd.DataFrame()
    for t in types:
        result = pd.read_csv(
            os.path.join(path, t + '.csv'),
            sep=";", header=[0, 1, 2], index_col=0, parse_dates=True)
        selection = pd.concat(
            [selection,
             result.xs([bus, 'flow'], axis=1, level=[0,2])], axis=1)
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
