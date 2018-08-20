# -*- coding: utf-8 -*-

""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application and work with the oemof datapackage - reader functionality

SPDX-License-Identifier: GPL-3.0-or-later
"""

from oemof.network import Node
from oemof.solph import (Source, Flow, Investment, NonConvex, Sink, Transformer,
                         Bus)
from oemof.solph.components import GenericStorage, ExtractionTurbineCHP
from oemof.solph.custom import Link
from oemof.solph.plumbing import sequence

from renpass import facades
import pyomo.environ as po


def min_renewable_share(m, share=0.5):
    """
    """
    renewable_carrier = ['biomass', 'biogas', 'wind', 'solar', 'waste']

    renewables = [f for f in m.es.flows()
                  if f[0].carrier in renewable_carrier
                  and f[1].carrier == 'electricity']

    flexibility_types = ['storage', 'connection', 'transshipment', 'battery']

    total = [f for f in m.es.flows()
             if f[1].carrier == 'electricity'
             and getattr(f[0], 'tech', None) not in flexibility_types
             and getattr(f[1], 'tech', None) not in flexibility_types]

    def _rule(m):
        """
        """
        renewable_production = sum(m.flow[i, o, t]
                                  for i,o in renewables
                                  for t in m.TIMESTEPS)
        total_production = sum(m.flow[i, o, t]
                               for i, o  in total
                               for t in m.TIMESTEPS)

        return (renewable_production >= total_production * share)
    m.min_renewable_share = po.Constraint(rule=_rule)

    return m
