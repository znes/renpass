
from oemof.solph import EnergySystem, Model
import options
import pprint

es = EnergySystem.from_datapackage(
    'examples/dispatch/datapackage.json',
    attributemap={},
    typemap=options.typemap)

for n in es.nodes:
    pprint.pprint(n.__dict__)

m = Model(es)

m.pprint()
