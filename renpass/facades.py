# -*- coding: utf-8 -*-

""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application and work with the oemof datapackage - reader functionality

SPDX-License-Identifier: GPL-3.0-or-later
"""
from oemof.network import Node
from oemof.solph import Source, Flow, Investment, Sink, Transformer, Bus
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


        # for r in required:
        #     if getattr(self, r) is None:
        #         raise ValueError(
        #             ("Missing attribute `{}` for facade of type `{}` with" +
        #              " name/label `{}`.").format(r, type(self), self.label)

    def _investment(self):
        if self.capacity is None:
            if self.investment_cost is None:
                msg = ("If you don't set `capacity`, you need to set attribute " +
                       "`investment_cost` of component {}!")
                raise ValueError(msg.format(self.label))
            else:
                # TODO: calculate ep_costs from specific capex
                investment = Investment(ep_costs=self.investment_cost)
        else:
            investment = None

        return investment


class Reservoir(GenericStorage, Facade):
    """ Reservoir storage unit

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    capacity: numeric
        The total capacity of the storage (e.g. in MWh)
    power: numeric
        Power of ther turbine installed at the reservoir
    inflow: array-like
        Absolute profile of water inflow into the storage
    investment_cost: numeric
        Investment costs for the storage capacity! unit e.g in €/MW-capacity
    spillage: boolean
        If True, spillage of water will be possible, otherwise water is forced
        to storage. Default: True
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs, _facade_requires_=['bus', 'inflow'])

        self.capacity = kwargs.get('capacity')

        self.power = kwargs.get('power')

        self.nominal_capacity = self.capacity

        self.investment_cost = kwargs.get('investment_cost')

        self.spillage = kwargs.get('spillage', True)

        self.investment = self._investment()

        self.input_edge_parameters = kwargs.get('input_edge_parameters', {})

        self.output_edge_parameters = kwargs.get('output_edge_parameters', {})

        if self.investment:
            investment = Investment()
        else:
            investment = None

        reservoir_bus = Bus(label="reservoir-bus-" + self.label)
        inflow = Source(
            label="inflow" + self.label,
            outputs={
                reservoir_bus: Flow(nominal_value=1,
                            #i/max(self.inflow) for i in self.inflow
                            actual_value=self.inflow,
                            fixed=True)})
        if self.spillage:
            spillage = Sink(label="spillage" + self.label,
                            inputs={reservoir_bus: Flow()})
        else:
            water_spillage = None

        self.inputs.update({
            reservoir_bus: Flow(investment=investment,
                                **self.input_edge_parameters)})

        self.outputs.update({
            self.bus: Flow(investment=investment,
                            **self.output_edge_parameters)})

        self.subnodes = (reservoir_bus, inflow, spillage)


class Generator(Source, Facade):
    """ Generator unit with one output, e.g. gas-turbine, wind-turbine, etc.

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the generator is connected to
    capacity: numeric
        The capacity of the generator (e.g. in MW).
    dispatchable: boolean
        If False the generator will be a must run unit based on the specified
        `profile` and (default is True).
    profile: array-like
        Profile of the output such that profile[t] * capacity yields output for
        timestep t
    marginal_cost: numeric
        Marginal cost for one unit of produced output
        E.g. for a powerplant:
        marginal cost =fuel cost + operational cost + co2 cost (in Euro / MWh)
        if timestep length is one hour.
    investment_cost: numeric
        Investment costs per unit of capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        generators capacity.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, _facade_requires_=['bus'])

        self.profile = kwargs.get('profile')

        self.capacity = kwargs.get('capacity')

        self.dispatchable = kwargs.get('dispatchable', True)

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.investment_cost = kwargs.get('investment_cost')

        self.edge_parameters = kwargs.get('edge_parameters', {})

        investment = self._investment()

        f = Flow(nominal_value=self.capacity,
                 variable_costs=self.marginal_cost,
                 actual_value=self.profile,
                 investment=investment,
                 fixed=not self.dispatchable,
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
    fuel_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        intput
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
    investment_cost: numeric
        Investment costs per unit of electrical capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(conversion_factor_full_condensation={},
                         *args,
                         **kwargs,
                         _facade_requires_=[
                             'fuel_bus', 'electricity_bus', 'heat_bus',
                             'thermal_efficiency', 'electric_efficiency',
                             'condensing_efficiency'])

        self.capacity = kwargs.get('capacity')

        self.condesing_efficiency = sequence(self.condensing_efficiency)

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.investment_cost = kwargs.get('investment_cost')

        investment = self._investment()

        self.conversion_factors.update({
            self.fuel_bus: sequence(1),
            self.electricity_bus: sequence(self.electric_efficiency),
            self.heat_bus: sequence(self.thermal_efficiency)})

        self.inputs.update({
            self.fuel_bus: Flow()})

        self.outputs.update({
            self.electricity_bus: Flow(nominal_value=self.capacity,
                                       variable_costs=self.marginal_cost,
                                       investment=investment),
            self.heat_bus: Flow()})

        self.conversion_factor_full_condensation.update({
            self.electricity_bus: self.condesing_efficiency})


class Backpressure(Transformer, Facade):
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
    fuel_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        intput
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
    investment_cost: numeric
        Investment costs per unit of electrical capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         _facade_requires_=[
                             'fuel_bus', 'electricity_bus', 'heat_bus',
                             'thermal_efficiency', 'electric_efficiency'])

        self.capacity = kwargs.get('capacity')

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.fuel_cost = kwargs.get('fuel_cost', 0)

        self.investment_cost = kwargs.get('investment_cost')

        investment = self._investment()

        self.conversion_factors.update({
            self.fuel_bus: sequence(1),
            self.electricity_bus: sequence(self.electric_efficiency),
            self.heat_bus: sequence(self.thermal_efficiency)})

        self.inputs.update({
            self.fuel_bus: Flow(variable_costs=self.fuel_cost)})

        self.outputs.update({
            self.electricity_bus: Flow(nominal_value=self.capacity,
                                       variable_costs=self.marginal_cost,
                                       investment=investment),
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
    efficiency:
        Efficiency of the conversion unit (0 <= efficiency <= 1). Default: 1
    marginal_cost: numeric
        Marginal cost for one unit of produced output. Default: 0
    investment_cost: numeric
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

        self.investment_cost = kwargs.get('investment_cost')

        self.input_edge_parameters = kwargs.get('input_edge_parameters', {})

        self.output_edge_parameters = kwargs.get('output_edge_parameters', {})

        investment = self._investment()

        self.conversion_factors.update({
            self.from_bus: sequence(1),
            self.to_bus: sequence(self.efficiency)})

        self.inputs.update({
            self.from_bus: Flow(**self.input_edge_parameters)})

        self.outputs.update({
            self.to_bus: Flow(nominal_value=self.capacity,
                              variable_costs=self.marginal_cost,
                              **self.output_edge_parameters)})


class Excess(Sink, Facade):
    """ Excess slack with one input

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the demand is connected to.
    marginal_cost: numeric
        Marginal cost for one unit of produced output. Default: 0
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, _facade_requires_=['bus'])

        self.marginal_cost = kwargs.get('marginal_cost', 0)

        self.inputs.update(
            {self.bus: Flow(variable_costs=self.marginal_cost)})



class Demand(Sink, Facade):
    """ Demand object with one input

     Parameters
     ----------
     bus: oemof.solph.Bus
         An oemof bus instance where the demand is connected to.
     amount: numeric
         The total amount for the timehorzion (e.g. in MWh)
     profile: array-like
          Demand profile with normed values such that `profile[t] * amount`
          yields the demand in timestep t (e.g. in MWh)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         _facade_requires_=['bus', 'amount', 'profile'])

        self.edge_parameters = kwargs.get('edge_parameters', {})

        self.inputs.update({self.bus: Flow(nominal_value=self.amount,
                                           actual_value=self.profile,
                                           fixed=True,
                                           **self.edge_parameters)})


class Storage(GenericStorage, Facade):
    """ Storage unit

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    capacity: numeric
        The total capacity of the storage (e.g. in MWh)
    power: numeric
        Max in/out power of storage. Either set this attribute OR `c_rate`.
        If you do not specify `capacity` and set `investment_cost`, use
        `c_rate` instead of power
    ep_ratio: numeric (optional)
        Ratio between energy and power output of the storage. Needs to be
        set if attr `investment_cost` is set.
    investment_cost: numeric
        Investment costs for the storage unit e.g in €/MWh-capacity
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs, _facade_requires_=['bus'])

        self.capacity = kwargs.get('capacity')

        self.power = kwargs.get('power')

        self.nominal_capacity = self.capacity

        self.investment_cost = kwargs.get('investment_cost')

        self.capacity_loss = sequence(kwargs.get('loss', 0))

        self.inflow_conversion_factor = sequence(
            kwargs.get('charge_efficiency', 1))

        self.outflow_conversion_factor = sequence(
            kwargs.get('discharge_efficiency', 1))

        self.investment = self._investment()

        self.input_edge_parameters = kwargs.get('input_edge_parameters', {})

        self.output_edge_parameters = kwargs.get('output_edge_parameters', {})

        if self.investment:
            if kwargs.get('ep_ratio') is None:
                raise AttributeError(
                    ("You need to set attr `ep_ratio` for "
                     "component {}").format(self.label))
            else:
                self.invest_relation_input_capacity =  kwargs.get('ep_ratio')
                self.invest_relation_output_capacity = kwargs.get('ep_ratio')

            investment = Investment()
            fi = Flow(investment=investment,
                 **self.input_edge_parameters)
            fo = Flow(investment=investment,
                      **self.output_edge_parameters)
            # required for correct grouping in oemof.solph.components
            self._invest_group = True
        else:
            investment = None
            fi = Flow(investment=investment, nominal_value=self.power,
                      **self.input_edge_parameters)
            fo = Flow(investment=investment, nominal_value=self.power,
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
    investment_cost: numeric
        Investment costs per unit of output capacity.
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         _facade_requires_=['from_bus', 'to_bus'])

        self.capacity = kwargs.get('capacity')

        self.loss = kwargs.get('loss', 0)

        self.investment_cost = kwargs.get('investment_cost')

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


class RunOfRiver(Generator):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Boiler(Generator):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
