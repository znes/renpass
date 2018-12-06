# -*- coding: utf-8 -*-

""" This module is designed to contain classes that act as simplified / reduced
energy specific interfaces (facades) for solph components to simplify its
application and work with the oemof datapackage - reader functionality

SPDX-License-Identifier: GPL-3.0-or-later
"""

from renpass import facades as fc

from oemof.solph import EnergySystem, Model

import pandas as pd


# initialise oemof energy system object
es = EnergySystem(timeindex=pd.date_range('2018', freq='H', periods=3))

# buses
el1 = fc.Bus('electricity1')

el2 = fc.Bus('electricity2')

heat = fc.Bus('heat')

biomass = fc.Bus('biomass', balanced=False)

gas = fc.Bus('gas', balanced=False)

st = fc.Dispatchable('st', bus=el1, carrier='biogas', tech='st', capacity=10,
                     marginal_cost=[0.1, 5, 100],
                     edge_parameters={
                        'flow': 10,
                        'positive_gradient': {
                            'ub': 0.1,
                            'costs': 0.2}}, commitable=False)

wind = fc.Volatile('wt', bus=el1, carrier='wind', tech='wind',
                   capacity_cost=20, profile=[0.1, 0.2, 0],
                   edge_parameters={'summed_max':10})

sto = fc.Storage('sto', bus=el2, carrier='electricity', tech='battery',
                 commitable=False, capacity_cost=4, capacity_ratio=0.5)


conv = fc.Conversion('conv', from_bus=el2, to_bus=heat, efficiency=0.95,
                     capacity=2)

load = fc.Load('load', bus=el1, amount=1000, profile=[0.005, 0.00034, 0.0434])

conn = fc.Link('conn', from_bus=el1, to_bus=el2, loss=0.07, capacity=100)

es.add(el1, el2, heat, biomass, st, wind, sto, conv, load, conn, gas)

m = Model(es)

m.pprint()

m.write('model.lp', io_options={'symbolic_solver_labels': True})
