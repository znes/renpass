
from oemof.solph import EnergySystem, Model
from renpass import options, system_constraints
import pprint


dispatch = True
investment = False

if dispatch:
    es = EnergySystem.from_datapackage(
        'renpass/examples/dispatch/datapackage.json',
        attributemap={},
        typemap=options.typemap)


if investment:
    es = EnergySystem.from_datapackage(
        'renpass/examples/investment/datapackage.json',
        attributemap={},
        typemap=options.typemap)


for n in es.nodes:
     pprint.pprint(n.__dict__)

m = Model(es)


m.solve()

system_constraints.min_renewable_share(m, 0.1)

m.min_renewable_share.pprint()
#m.write()
