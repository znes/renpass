# -*- coding: utf-8 -*-
""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application and work with the oemof datapackage - reader functionality

SPDX-License-Identifier: GPL-3.0-or-later
"""

import pandas as pd

from oemof.solph import EnergySystem, Model
from oemof.tabular import facades as fc


es = EnergySystem(timeindex=pd.date_range('2018', freq='H', periods=3))

# buses
el1 = fc.Bus('electricity1')


res = fc.Reservoir(capacity=10, profile=[400, 0, 0], bus=el1, storage_capacity=100,
                   efficiency=1)

#backup = fc.Dispatchable(capacity_cost=10, bus=el1)
#es.add(backup)

spillage = fc.Excess(bus=el1)
load = fc.Load('load', bus=el1, amount=10, profile=[0.5, 0.4, 0.3])


# if the datapackage reader is not used, subnodes have to be added by hand
es.add(el1, load, res, res.subnodes[0], spillage)


m = Model(es)

m.pprint()

m.solve()

m.results()

m.write('model.lp', io_options={'symbolic_solver_labels': True})
