# -*- coding: utf-8 -*-
"""

SPDX-License-Identifier: GPL-3.0-or-later
"""
import os
import re

from datapackage import Package
import pandas as pd
import pyomo.environ as po

import tsam.timeseriesaggregation as tsam


def temporal_clustering(datapackage, n_cluster):
    """
    """
    package_root_path = os.path.dirname(datapackage)
    package_json_path = os.path.basename(datapackage)

    p = Package(datapackage)

    sequence_resources = [
        r for r in p.resources
        if re.match(r'^data/sequences/.*$', r.descriptor['path'])]

    dfs = {
        r.name: pd.DataFrame(r.read(keyed='True')).set_index('timeindex').astype(float)
        for r in sequence_resources}
    sequences = pd.concat(dfs.values(), axis=1)

    aggregation = tsam.TimeSeriesAggregation(
        sequences,
        noTypicalPeriods=n_cluster,
        rescaleClusterPeriods=False,
        hoursPerPeriod=24,
        clusterMethod='hierarchical')

    clustered_sequences = aggregation.createTypicalPeriods()

    cluster_weights = {}

    for n, w in aggregation.clusterPeriodNoOccur.items():
        cluster_weights[aggregation.clusterCenterIndices[n]] = w

    clustered_timeindex = pd.Series(
        {d:cluster_weights[d.dayofyear]
         for d in sequences.index
         if d.dayofyear in aggregation.clusterCenterIndices}, name='weighting')
    clustered_timeindex.index.name = 'timeindex'

    #for r in sequence_resources:
#        dfs[r.name].loc[clustered_timeindex.index].to_csv(
#            os.path.join(package_root_path, r.descriptor['path']))

    clustered_timeindex.to_csv(
        os.path.join(package_root_path, 'data/sequences', 'timeindex_weights.csv'),
        header=True, sep=";", date_format='%Y-%m-%dT%H:%M:%SZ')

    return clustered_timeindex


def cluster_period(m, period_length=24):
    """ Set the storage level of every storage to it's initial capacity
    at every first hour of a cluster period.
    """

    m.PERDIOD_STARTS = m.timeindex.index[0::period_length]

    def day_rule(m, n, t):
        """
        Sets the soc of the every first hour to the soc of the last hour
        of the day (i.e. + 23 hours)
        """
        return (
            m.GenericInvestmentStorageBlock.capacity[n, t] ==
            m.GenericInvestmentStorageBlock.capacity[n, t + pd.Timedelta(hours=period_length-1)])

        return expr
    m.temporal_cluster_period_bounds = po.Constraint(
        m.GenericInvestmentStorageBlock.INVESTSTORAGES,
        m.PERIOD_STARTS,
        rule=rule)
