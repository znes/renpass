# -*- coding: utf-8 -*-

""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application and work with the oemof datapackage - reader functionality

SPDX-License-Identifier: GPL-3.0-or-later
"""

import pandas as pd

from oemof.solph import EnergySystem, Model
from oeomf.tabular import facades as fc

from renpass.components import storages as st


es = EnergySystem(timeindex=pd.date_range('2018', freq='H', periods=3))

bus = fc.Bus('bus')

residual_load = fc.Volatile('residual_load', bus=bus, capacity=100,
                            profile=[0.1, -0.4, 0.4])

storage = st.Storage('st', bus=bus, storage_capacity=100, capacity=10)

slack = fc.Shortage('slack', bus=bus, capacity=10e10, marginal_cost=1000,
                    edge_parameters={'min':-1})


es.add(bus, residual_load, storage, slack)

m = Model(es)

m.write('storage-model.lp', io_options={'symbolic_solver_labels': True})
