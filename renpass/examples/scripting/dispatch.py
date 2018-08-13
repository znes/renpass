

from renpass.facades import Dispatchable, Volatile, Storage, BackpressureTurbine

from oemof.solph import EnergySystem, Model
from oemof.network import Bus

import pandas as pd


# initialise oemof energy system object
es = EnergySystem(timeindex=pd.date_range('2018', freq='H', periods=3))

# create some elements
el = Bus('electricity')

heat = Bus('heat')

biomass = Bus('biomass')


st = Dispatchable('st', bus=el, carrier='biogas', tech='st', capacity=10,
                   marginal_cost=[0.1, 5, 100],
                   edge_parameters={'flow': 10}, commitable=False)

wind = Volatile('wt', bus=el, carrier='wind', tech='wind', capacity=10,
                profile=[0.1, 0.2, 0])

sto = Storage('sto', bus=el, carrier='electricity', tech='battery',
              commitable=False,
              storage_capacity=10, capacity=1)

bp = BackpressureTurbine('bp', carrier=biomass,
                          tech='bp',
                          commitable=False,
                          electricity_bus=el, heat_bus=heat,
                          capacity=10,
                          thermal_efficiency=0.4,
                          electric_efficiency=0.44)

es.add(el, heat, biomass, bp, st, wind, sto)

m = Model(es)

m.pprint()
