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


class Facade(Node):
    """
    Parameters
    ----------
    _facade_requires_ : list of str
        A list of required attributes. The constructor checks whether these are
        present as keywort arguments or whether they are already present on
        self (which means they have been set by constructors of subclasses) and
        raises an error if he doesn't find them.
    """
    def __init__(self, *args, **kwargs):
        """
        """

        self.type = type(self)

        self.tech = kwargs.get('tech')

        self.carrier = kwargs.get('carrier')

        required = kwargs.pop("_facade_requires_", [])
        super().__init__(*args, **kwargs)
        self.subnodes = []
        for r in required:
            if r in kwargs:
                setattr(self, r, kwargs[r])
            elif not hasattr(self, r):
                raise AttributeError(
                        ("Missing required attribute `{}` for `{}` " +
                         "object with name/label `{!r}`.")
                        .format(r, type(self).__name__, self.label))

    def _investment(self):
        if self.capacity is None:
            if self.capacity_cost is None:
                msg = ("If you don't set `capacity`, you need to set attribute " +
                       "`capacity_cost` of component {}!")
                raise ValueError(msg.format(self.label))
            else:
                # TODO: calculate ep_costs from specific capex
                if isinstance(self, GenericStorage):
                    self.investment = Investment(
                    ep_costs=self.storage_capacity_cost)
                else:
                    self.investment = Investment(
                        ep_costs=self.capacity_cost,
                        maximum=getattr(self, 'capacity_potential', float('+inf')))
        else:
            self.investment = None
        return self.investment

    def _commitable(self):
        if getattr(self, 'commitable', False):
            nonconvex = NonConvex(
                            # min=getattr(self, 'pmin', 0),
                            max=getattr(self, 'pmax', self.capacity)
                        )
        else:
            nonconvex = None
        return nonconvex


class Reservoir(GenericStorage, Facade):
    """ Reservoir storage unit

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    storage_capacity: numeric
        The total storage capacity of the storage (e.g. in MWh)
    capacity: numeric
        Installed production capacity of the turbine installed at the
        reservoir
    efficiency: numeric
        Efficiency of the turbine converting inflow (in MWel) to electricity
        production
    inflow: array-like
        Absolute profile of water inflow into the storage
    capacity_cost: numeric
        Investment costs for the storage capacity! i.e. unit for example
        €/MW installed capacity not per MWh
    spillage: boolean
        If True, spillage of water will be possible, otherwise water is forced
        to storage. Default: True
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs,
                        _facade_requires_=['bus', 'inflow', 'efficiency'])

        self.storage_capacity = kwargs.get('storage_capacity')

        self.capacity = kwargs.get('capacity')

        self.efficiency = kwargs.get('efficiency')

        self.nominal_capacity = self.storage_capacity

        self.capacity_cost = kwargs.get('capacity_cost')

        self.storage_capacity_cost = kwargs.get('storage_capacity_cost')

        self.spillage = kwargs.get('spillage', True)

        self.input_edge_parameters = kwargs.get('input_edge_parameters', {})

        self.output_edge_parameters = kwargs.get('output_edge_parameters', {})

        investment = self._investment()

        reservoir_bus = Bus(label="reservoir-bus-" + self.label)
        inflow = Source(
            label="inflow" + self.label,
            outputs={
                reservoir_bus: Flow(nominal_value=1,
                                    actual_value=self.inflow,
                                    fixed=True)})
        if self.spillage:
            f = Flow()
        else:
            f = Flow(actual_value=0, fixed=True)

        spillage = Sink(label="spillage" + self.label,
                        inputs={reservoir_bus: f})
        self.inputs.update({
            reservoir_bus: Flow(**self.input_edge_parameters)})

        self.outputs.update({
            self.bus: Flow(investment=investment,
                            **self.output_edge_parameters)})

        self.subnodes = (reservoir_bus, inflow, spillage)


class Dispatchable(Source, Facade):
    """ Dispatchable element with one output for example a gas-turbine

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the generator is connected to
    tech: string
        Description of technoglogy (for example: ST, GT, OCGT, ...)
    carrier: string
        Carrier of input used for production (for example gas, coal, ...)
    capacity: numeric
        The installed power of the generator (e.g. in MW).
    profile: array-like
        Profile of the output such that profile[t] * installed yields output
        for timestep t
    marginal_cost: numeric
        Marginal cost for one unit of produced output, i.e. for a powerplant:
        mc = fuel_cost + co2_cost + ... (in Euro / MWh) if timestep length is
        one hour.
    capacity_cost: numeric (optional)
        Investment costs per unit of capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        generators capacity.
    commitable: boolean
        Indicates if element is commitable
    pmin: numeric
        Minimal electrical production capacity (0 <= pmin <= 1)
    edge_paramerters: dict (optional)
    capacity_potential: numeric
        Max install capacity if investment
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         _facade_requires_=['bus', 'carrier', 'tech'])

        self.carrier = kwargs.get('carrier')

        self.profile = kwargs.get('profile')

        self.capacity = kwargs.get('capacity')

        self.capacity_potential = kwargs.get('capacity_potential')

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.capacity_cost = kwargs.get('capacity_cost')

        self.edge_parameters = kwargs.get('edge_parameters', {})

        self.commitable = kwargs.get('commitable', False)

        self.pmin = kwargs.get('pmin', 0.5)
        self.pmin = kwargs.get('pmin', 0)

        f = Flow(nominal_value=self.capacity,
                 variable_costs=self.marginal_cost,
                 actual_value=self.profile,
                 investment=self._investment(),
                 nonconvex=self._commitable(),
                 min=self.pmin,
                 **self.edge_parameters)

        self.outputs.update({self.bus: f})


class Volatile(Source, Facade):
    """ Volatile element with one output for example a wind turbine

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the generator is connected to
    tech: string
        Description of technoglogy (for example: ST, GT, OCGT, ...)
    carrier: string
        Carrier of input used for production (for example gas, coal, ...)
    capacity: numeric
        The installed power of the generator (e.g. in MW).
    profile: array-like
        Profile of the output such that profile[t] * installed yields output
        for timestep t
    marginal_cost: numeric
        Marginal cost for one unit of produced output, i.e. for a powerplant:
        mc = fuel_cost + co2_cost + ... (in Euro / MWh) if timestep length is
        one hour.
    capacity_cost: numeric (optional)
        Investment costs per unit of capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        generators capacity.
    edge_paramerters: dict (optional)
    capacity_potential: numeric
        Max install capacity if investment
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         _facade_requires_=['bus', 'carrier', 'tech'])

        self.carrier = kwargs.get('carrier')

        self.profile = kwargs.get('profile')

        self.capacity = kwargs.get('capacity')

        self.capacity_potential = kwargs.get('capacity_potential')

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.capacity_cost = kwargs.get('capacity_cost')

        self.edge_parameters = kwargs.get('edge_parameters', {})


        f = Flow(nominal_value=self.capacity,
                 variable_costs=self.marginal_cost,
                 actual_value=self.profile,
                 investment=self._investment(),
                 fixed=True,
                 **self.edge_parameters)

        self.outputs.update({self.bus: f})


class ExtractionTurbine(ExtractionTurbineCHP, Facade):
    """ Combined Heat and Power (extraction) unit with one input and
    two outputs.

    Parameters
    ----------
    electricity_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        electrical output
    heat_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        thermal output
    carrier: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        input
    carrier_cost: numeric
        Cost per unit of used input carrier
    capacity: numeric
        The electrical capacity of the chp unit (e.g. in MW) in full extraction
        mode.
    electric_efficiency:
        Electrical efficiency of the chp unit in full backpressure mode
    thermal_efficiency:
        Thermal efficiency of the chp unit in full backpressure mode
    condensing_efficiency:
        Electrical efficiency if turbine operates in full extraction mode
    marginal_cost: numeric
        Marginal cost for one unit of produced electrical output
        E.g. for a powerplant:
        marginal cost =fuel cost + operational cost + co2 cost (in Euro / MWh)
        if timestep length is one hour.
    commitable: boolean
        Indicates whether unit is commitable
    pmin: numeric
        Minimal electrical production capacity (0 <= pmin <= 1)
    capacity_cost: numeric
        Investment costs per unit of electrical capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(conversion_factor_full_condensation={},
                         *args,
                         **kwargs,
                         _facade_requires_=[
                             'carrier', 'electricity_bus', 'heat_bus',
                             'thermal_efficiency', 'electric_efficiency',
                             'condensing_efficiency'])

        self.carrier = kwargs.get('carrier')

        self.carrier_cost = kwargs.get('carrier_cost', 0)

        self.capacity = kwargs.get('capacity')

        self.condensing_efficiency = sequence(self.condensing_efficiency)

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.capacity_cost = kwargs.get('capacity_cost')

        self.electricity_bus = kwargs.get('electricity_bus')

        self.heat_bus = kwargs.get('heat_bus')

        self.pmin = kwargs.get('pmin', 0)

        self.conversion_factors.update({
            self.carrier: sequence(1),
            self.electricity_bus: sequence(self.electric_efficiency),
            self.heat_bus: sequence(self.thermal_efficiency)})

        self.inputs.update({
            self.carrier: Flow(variable_cost=self.carrier_cost)})

        self.outputs.update({
            self.electricity_bus: Flow(nominal_value=self.capacity,
                                       variable_costs=self.marginal_cost,
                                       min=self.pmin,
                                       nonconvex=self._commitable(),
                                       investment=self._investment()),
            self.heat_bus: Flow()})

        self.conversion_factor_full_condensation.update({
            self.electricity_bus: self.condensing_efficiency})


class BackpressureTurbine(Transformer, Facade):
    """ Combined Heat and Power (backpressure) unit with one input and
    two outputs.

    Parameters
    ----------
    electricity_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        electrical output
    heat_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        thermal output
    carrier: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        input
    carrier_cost: numeric
        Input carrier cost of the backpressure unit
    capacity: numeric
        The electrical capacity of the chp unit (e.g. in MW).
    electric_efficiency:
        Electrical efficiency of the chp unit
    thermal_efficiency:
        Thermal efficiency of the chp unit
    marginal_cost: numeric
        Marginal cost for one unit of produced electrical output
        E.g. for a powerplant:
        marginal cost =fuel cost + operational cost + co2 cost (in Euro / MWh)
        if timestep length is one hour.
    capacity_cost: numeric
        Investment costs per unit of electrical capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
    commitable: boolean
        Indicating whether unit is commitable
    pmin: numeric
        Minimal electrical production capacity (0 <= pmin <= 1)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         _facade_requires_=[
                             'carrier', 'electricity_bus', 'heat_bus',
                             'thermal_efficiency', 'electric_efficiency'])

        self.electricity_bus = kwargs.get('electricity_bus')

        self.heat_bus = kwargs.get('heat_bus')

        self.capacity = kwargs.get('capacity')

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.carrier = kwargs.get('carrier')

        self.carrier_cost = kwargs.get('carrier_cost', 0)

        self.capacity_cost = kwargs.get('capacity_cost')

        self.commitable = kwargs.get('commitable', False)

        self.pmin = kwargs.get('pmin', 0)

        self.conversion_factors.update({
            self.carrier: sequence(1),
            self.electricity_bus: sequence(self.electric_efficiency),
            self.heat_bus: sequence(self.thermal_efficiency)})

        self.inputs.update({
            self.carrier: Flow(variable_costs=self.carrier_cost)})

        self.outputs.update({
            self.electricity_bus: Flow(nominal_value=self.capacity,
                                       variable_costs=self.marginal_cost,
                                       min=self.pmin,
                                       investment=self._investment(),
                                       nonconvex=self._commitable()),
            self.heat_bus: Flow()})


class Conversion(Transformer, Facade):
    """ Conversion unit with one input and one output.

    Parameters
    ----------
    from_bus: oemof.solph.Bus
        An oemof bus instance where the conversion unit is connected to with
        its input.
    to_bus: oemof.solph.Bus
        An oemof bus instance where the conversion unit is connected to with
        its output.
    capacity: numeric
        The conversion capacity (output side) of the unit.
    efficiency: numeric
        Efficiency of the conversion unit (0 <= efficiency <= 1). Default: 1
    marginal_cost: numeric
        Marginal cost for one unit of produced output. Default: 0
    capacity_cost: numeric
        Investment costs per unit of output capacity.
        If capacity is not set, this value will be used for optimizing the
        conversion output capacity.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         _facade_requires_=['from_bus', 'to_bus'])


        self.capacity = kwargs.get('capacity')

        self.efficiency = kwargs.get('efficiency', 1)

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.capacity_cost = kwargs.get('capacity_cost')

        self.input_edge_parameters = kwargs.get('input_edge_parameters', {})

        self.output_edge_parameters = kwargs.get('output_edge_parameters', {})


        self.conversion_factors.update({
            self.from_bus: sequence(1),
            self.to_bus: sequence(self.efficiency)})

        self.inputs.update({
            self.from_bus: Flow(**self.input_edge_parameters)})

        self.outputs.update({
            self.to_bus: Flow(nominal_value=self.capacity,
                              variable_costs=self.marginal_cost,
                              investment=self._investment(),
                              nonconex=self._commitable(),
                              **self.output_edge_parameters)})


class Load(Sink, Facade):
    """ Load object with one input

    Parameters
    ----------
    bus: oemof.solph.Bus
         An oemof bus instance where the demand is connected to.
    amount: numeric
         The total amount for the timehorzion (e.g. in MWh)
    profile: array-like
          Load profile with normed values such that `profile[t] * amount`
          yields the load in timestep t (e.g. in MWh)
    edge_parameters: dirct (optional)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         _facade_requires_=['bus', 'amount', 'profile'])

        self.amount = kwargs.get('amount')

        self.profile = kwargs.get('profile')

        self.edge_parameters = kwargs.get('edge_parameters', {})

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.inputs.update({self.bus: Flow(nominal_value=self.amount,
                                           actual_value=self.profile,
                                           fixed=True,
                                           variable_cost=self.marginal_cost,
                                           **self.edge_parameters)})


class Storage(GenericStorage, Facade):
    """ Storage unit

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    storage_capacity: numeric
        The total capacity of the storage (e.g. in MWh
    capacity: numeric
        Maximum production capacity (e.g. in MW)
    capacity_ratio: numeric
        Ratio between `storage_capacity` and `capacity`
    efficiency: numeric
        efficiency of charging and discharging process
    capacity_cost: numeric
        Investment costs for the storage unit e.g in €/MW-capacity
    storage_capacity_cost: numeric
        Investment costs for the storage unit e.g in €/MWh-capacity
    loss: numeric
        Standing loss per timestep in % of capacity
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs, _facade_requires_=['bus'])

        self.storage_capacity = kwargs.get('storage_capacity')

        self.capacity = kwargs.get('capacity')

        self.nominal_capacity = self.storage_capacity

        self.capacity_cost = kwargs.get('capacity_cost')

        self.storage_capacity_cost = kwargs.get('storage_capacity_cost')

        self.loss = sequence(kwargs.get('loss', 0))

        self.inflow_conversion_factor = sequence(
            kwargs.get('efficiency', 1))

        self.outflow_conversion_factor = sequence(
            kwargs.get('efficiency', 1))

        # make it investment but don't set costs (set below for flow (power))
        self.investment = self._investment()

        self.input_edge_parameters = kwargs.get('input_edge_parameters', {})

        self.output_edge_parameters = kwargs.get('output_edge_parameters', {})

        if self.investment:
            if self._commitable():
                raise AttributeError('Commitment and Investment not compatible!')
            elif kwargs.get('capacity_ratio') is None:
                raise AttributeError(
                    ("You need to set attr `capacity_ratio` for "
                     "component {}").format(self.label))
            else:
                self.invest_relation_input_capacity =  kwargs.get('capacity_ratio')
                self.invest_relation_output_capacity = kwargs.get('capacity_ratio')
                self.invest_relation_input_output = 1

            # set capacity costs at one of the flows
            fi = Flow(investment=Investment(
                        ep_costs=self.capacity_cost,
                        maximum=getattr(self,
                                        'capacity_potential',
                                        float('+inf'))),
                 **self.input_edge_parameters)
            # set investment, but no costs (as relation input / output = 1)
            fo = Flow(investment=Investment(),
                      **self.output_edge_parameters)
            # required for correct grouping in oemof.solph.components
            self._invest_group = True
        else:
            investment = None

            fi = Flow(nominal_value=self.capacity,
                      **self.input_edge_parameters)
            fo = Flow(nominal_value=self.capacity,
                      **self.output_edge_parameters)

        self.inputs.update({self.bus: fi})

        self.outputs.update({self.bus: fo})

        # annoying oemof stuff, that requires _set_flows() to provide a
        # drepreciated warning
        self._set_flows('Ignore this warning...')


class Connection(Link, Facade):
    """ Bi-direction connection for two buses (e.g. to model transshipment)

    Parameters
    ----------
    from_bus: oemof.solph.Bus
        An oemof bus instance where the connection unit is connected to with
        its input.
    to_bus: oemof.solph.Bus
        An oemof bus instance where the connection unit is connected to with
        its output.
    capacity: numeric
        The maximal capacity (output side each) of the unit. If not set, attr
        `investment_cost` needs to be set.
    loss:
        Relative loss through the connection (default: 0)
    capacity_cost: numeric
        Investment costs per unit of output capacity.
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         _facade_requires_=['from_bus', 'to_bus'])

        self.capacity = kwargs.get('capacity')

        self.loss = kwargs.get('loss', 0)

        self.capacity_cost = kwargs.get('capacity_cost')

        investment = self._investment()

        self.inputs.update({
            self.from_bus: Flow(),
            self.to_bus: Flow()})

        self.outputs.update({
            self.from_bus: Flow(nominal_value=self.capacity,
                                investment=investment),
            self.to_bus: Flow(nominal_value=self.capacity,
                              investment=investment)})

        self.conversion_factors.update({
            (self.from_bus, self.to_bus): sequence((1 - self.loss)),
            (self.to_bus, self.from_bus): sequence((1 - self.loss))})


class Excess(Sink, Facade):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, _facade_requires_=['bus'])

        self.bus = kwargs.get('bus')

        self.marginal_cost = kwargs.get('marginal_cost')

        self.inputs.update({
            self.bus: Flow(variable_costs=self.marginal_cost)})

class Shortage(Dispatchable):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Generator(Dispatchable):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
