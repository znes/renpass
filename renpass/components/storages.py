""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application and work with the oemof datapackage - reader functionality

SPDX-License-Identifier: GPL-3.0-or-later
"""
from oemof.solph import Flow
from oemof.network import Source

from renpass.facades import Facade


class Storage(Source, Facade):
    """ Storage unit

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    storage_capacity: numeric
        The total capacity of the storage (e.g. in MWh)
    capacity: numeric
        Maximum production capacity (e.g. in MW)
    capacity_ratio: numeric
        Ratio between `storage_capacity` and `capacity`
    investment_cost: numeric
        Investment costs for the storage unit e.g in €/MWh-capacity
    commitable: boolean
        If True, Unit commitment is enforce with BigM-constraint
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs, _facade_requires_=['bus'])

        self.bus = kwargs.get('bus')

        self.storage_capacity = kwargs.get('storage_capacity')

        self.capacity = kwargs.get('capacity')

        self.capacity_cost = kwargs.get('capacity_cost')

        self.loss = kwargs.get('loss', 0)

        self.commitable = kwargs.get('commitable', False)

        self.edge_parameters = kwargs.get('edge_parameters', {})

        self.outputs.update({
            self.bus: Flow(nominal_value=self.capacity,
                           bidirectional=True,
                           min=-1)})
