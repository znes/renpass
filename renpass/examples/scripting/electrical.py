# -*- coding: utf-8 -*-

""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application and work with the oemof datapackage - reader functionality

SPDX-License-Identifier: GPL-3.0-or-later

This example is based on one of the PyPSA examples:

https://www.pypsa.org/examples/minimal_example_lopf.html

Thanks at Tom, Jonas and others!
"""


from renpass import facades as fc
from renpass.components import electrical as elec

from oemof.solph import EnergySystem, Model
from oemof.network import Bus, Node, Edge

import pandas as pd


# initialise oemof energy system object
es = EnergySystem()

el0 = elec.ElectricalBus('el0')
el1 = elec.ElectricalBus('el1')
el2 = elec.ElectricalBus('el2')

line0 = elec.Line(from_bus=el0, to_bus=el1, capacity=60, reactance=0.0001)
line1 = elec.Line(from_bus=el1, to_bus=el2, capacity=60, reactance=0.0001)
line2 = elec.Line(from_bus=el2, to_bus=el0, capacity=60, reactance=0.0001)

gen0 = fc.Dispatchable("gen0", capacity=100, bus=el0, marginal_cost=50,
                       carrier='coal')
gen1 = fc.Dispatchable("gen1", capacity=100, bus=el1, marginal_cost=25,
                       carrier='gas')

load0 = fc.Load("load0", bus=el2, amount=100, profile=[1])

es.add(el0, el1, el2, line0, line1, line2, gen0, gen1, load0)

m = Model(es)

m.solve()

m.write('lopf-model.lp')
