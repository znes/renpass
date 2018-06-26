# -*- coding: utf-8 -*-

""" This module contains functions to postprocess (aggregate, etc.) results
from the model.

SPDX-License-Identifier: GPL-3.0-or-later
"""

import pandas as pd


storage_results = pd.read_csv(
    'renpass/results/e-highway-X7-simple/sequences/storage.csv',
    sep=";", header=[0, 1, 2], index_col=0, parse_dates=True)

storages = ['pumped-storage-DE']

for s in storages:

    grouper = lambda x: (lambda fr, to, ty:
                         'output' if (fr == s and ty == 'flow') else
                         'input' if (to == s and ty == 'flow') else
                         'level' if (fr == s and ty != 'flow') else
                         None) (*x)

    df = storage_results.groupby(grouper, axis=1).sum()

    df['net_storage'] = df['input'] - df['output']
    df['input'] = df['net_storage'].apply(lambda row: row if row > 0 else 0)
    df['output'] = df['net_storage'].apply(lambda row: abs(row) if row < 0 else 0)

    # output.to_csv(
    # os.path.join(data_path, str(k) + '.csv'), sep=";",
    # date_format='%Y-%m-%dT%H:%M:%SZ')

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

# -----------------------------------------------------------------------
# Derived results
# -----------------------------------------------------------------------
# transshipment / network export
conns = _edges([n for n in es.nodes
                if isinstance(n, facades.Connection)])

data_path = os.path.join(
    package_root_directory, 'data')
if not os.path.exists(data_path):
    os.makedirs(data_path)

if conns:
    transshipment = pd.concat(
        [views.node(results, n, multiindex=True)['sequences'].\
            loc[:, (n, slice(None), 'flow')]
         for n in conns], axis=1)

    net_transshipment = pd.concat([
        transshipment.loc[:, (c, str(es.groups[c].from_bus), 'flow')] -
        transshipment.loc[:, (c, str(es.groups[c].to_bus), 'flow')]
        for c in conns], axis=1)
    net_transshipment.columns = conns.keys()

    net_transshipment.index.name = 'timeindex'
    net_transshipment.to_csv(
        os.path.join(data_path, 'transshipment.csv'),
                     sep=";", date_format='%Y-%m-%dT%H:%M:%SZ')

# storage output
storages = {
    n: views.node(results, n, multiindex=True)['sequences']
    for n in es.nodes if isinstance(n, facades.Storage)}

if storages:
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
        net_storage = v.input - v.output
        v.input = net_storage.apply(lambda row: row if row > 0 else 0)
        v.output = net_storage.apply(lambda row: abs(row) if row < 0 else 0)
        v.index.name = 'timeindex'
        v.to_csv(
            os.path.join(data_path, str(k) + '.csv'), sep=";",
            date_format='%Y-%m-%dT%H:%M:%SZ')

# TODO prettify / complete package (meta-data) creation
if arguments['--results'] == 'datapackage':
    # results package (rp)
    rp = Package()
    rp.infer(os.path.join(package_root_directory, 'data', '**/*.csv'))
    rp.descriptor['description'] = "Model results from renpass with version..."
    rp.descriptor['name'] = modelname + '-results'
    rp.commit()
    rp.save(os.path.join(package_root_directory, 'datapackage.json'))
