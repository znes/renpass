# -*- coding: utf-8 -*-
"""

SPDX-License-Identifier: GPL-3.0-or-later
"""
import os
import re

from datapackage import Package
import pandas as pd
import pyomo.environ as po

def temporal_cluster_constraints(m, period_length=24):
    """ Set the storage level of every storage to it's initial capacity
    at every first hour of a cluster period.
    """

    m.PERIOD_STARTS = m.es.timeindex[0::period_length]
    m.START_END = {
        m.es.timeindex.get_loc(t):
        m.es.timeindex.get_loc(t + pd.Timedelta(hours=period_length-1))
        for t in m.PERIOD_STARTS}

    m.STORAGES = []
    if hasattr(m, 'GenericInvestmentStorageBlock'):
        m.STORAGES += [s for s in m.GenericInvestmentStorageBlock.INVESTSTORAGES]
    if hasattr(m, 'GenericStorageBlock'):
        m.STORAGES += [s for s in m.GenericStorageBlock.STORAGES]

    m.period_bounds = po.Constraint(m.STORAGES, m.START_END.keys())
    def _period_bounds(m):
        for t in m.START_END:
            for n in m.STORAGES:
                if n.capacity is None:
                    lhs = m.GenericInvestmentStorageBlock.capacity[n, t]
                    rhs = m.GenericInvestmentStorageBlock.capacity[n, m.START_END[t]]
                else:
                    lhs = m.GenericStorageBlock.capacity[n, t]
                    rhs = m.GenericStorageBlock.capacity[n, m.START_END[t]]
                m.period_bounds.add((n, t), (lhs == rhs))
    m.period_bounds_build = po.BuildAction(rule=_period_bounds)
