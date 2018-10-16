# -*- coding: utf-8 -*-

""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application and work with the oemof datapackage - reader functionality

SPDX-License-Identifier: GPL-3.0-or-later
"""
import logging

from pyomo.core.base.block import SimpleBlock
from pyomo.environ import Var, Constraint, Set, BuildAction

from oemof.network import Node, Edge, Transformer
from oemof.solph import Flow, Bus
from oemof.solph.plumbing import sequence

from renpass.facades import Facade

class ElectricalBus(Bus):
    """
    Parameters
    -----------
    slack: boolean
        True if object is slack bus of network
    v_max: numeric
        Maximum value of voltage angle at electrical bus
    v_min: numeric
        Mininum value of voltag angle at electrical bus
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.slack = kwargs.get('slack', False)

        self.v_max = kwargs.get('v_max', 1000)

        self.v_min = kwargs.get('v_min', -1000)


class Line(Facade, Flow):
    """
    Paramters
    ---------
    from_bus: ElectricalBus object
        Bus where the input of the Line object is connected to
    to_bus: ElectricalBus object
        Bus where the output of the Line object is connected to
    reactance: numeric
        Reactance of Line object
    capacity: numeric
        Capacity of the Line object
    capacity_cost: numeric
        Cost of capacity for 1 Unit of capacity
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.from_bus = kwargs.get('from_bus')

        self.to_bus = kwargs.get('to_bus')

        self.reactance = sequence(kwargs.get('reactance', 0.00001))

        self.capacity = kwargs.get('capacity')

        self.capacity_cost = kwargs.get('capacity_cost')

        # oemof related attribute setting of 'Flow-object'
        self.input = self.from_bus

        self.output = self.to_bus

        self.bidirectional = True

        self.nominal_value = self.capacity

        self.min = sequence(-1)

        self.investment = self._investment()

    def constraint_group(self):
        return ElectricalLineConstraints


class ElectricalLineConstraints(SimpleBlock):
    """
    """

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        """
        if group is None:
            return None

        m = self.parent_block()

        # create voltage angle variables
        self.ELECTRICAL_BUSES = Set(initialize=[n for n in m.es.nodes
                                    if isinstance(n, ElectricalBus)])

        def _voltage_angle_bounds(block, b, t):
            return b.v_min, b.v_max
        self.voltage_angle = Var(self.ELECTRICAL_BUSES, m.TIMESTEPS,
                                    bounds=_voltage_angle_bounds)

        if True not in [b.slack for b in self.ELECTRICAL_BUSES]:
            # TODO: Make this robust to select the same slack bus for
            # the same problems
            bus = [b for b in self.ELECTRICAL_BUSES][0]
            logging.info(
                "No slack bus set,setting bus {0} as slack bus".format(
                    bus.label))
            bus.slack = True

        def _voltage_angle_relation(block):
            for t in m.TIMESTEPS:
                for n in group:
                    if n.input.slack is True:
                        self.voltage_angle[n.output, t].value = 0
                        self.voltage_angle[n.output, t].fix()
                    try:
                        lhs = m.flow[n.input, n.output, t]
                        rhs = 1 / n.reactance[t] * (
                            self.voltage_angle[n.input, t] -
                            self.voltage_angle[n.output, t])
                    except:
                        raise ValueError("Error in constraint creation",
                                         "of node {}".format(n.label))
                    block.electrical_flow.add((n, t), (lhs == rhs))

        self.electrical_flow = Constraint(group, m.TIMESTEPS, noruleinit=True)

        self.electrical_flow_build = BuildAction(
                                         rule=_voltage_angle_relation)
