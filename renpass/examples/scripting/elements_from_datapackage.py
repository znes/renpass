
from oemof.solph import EnergySystem, Model
import options
import pprint

es1 = EnergySystem.from_datapackage(
    'examples/dispatch/datapackage.json',
    attributemap={},
    typemap=options.typemap)

for n in es1.nodes:
    pprint.pprint(n.__dict__)


# investment example
es2 = EnergySystem.from_datapackage(
    'examples/investment/datapackage.json',
    attributemap={},
    typemap=options.typemap)

for n in es2.nodes:
    pprint.pprint(n.__dict__)

m = Model(es2)

m.pprint()
