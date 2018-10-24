
from oemof.solph import EnergySystem, Model
from renpass import options
from renpass import postprocessing as pp
import pprint


dispatch = False


if dispatch:
    es = EnergySystem.from_datapackage(
        'renpass/examples/dispatch/datapackage.json',
        attributemap={},
        typemap=options.typemap)
else:
    es = EnergySystem.from_datapackage(
        'renpass/examples/investment/datapackage.json',
        attributemap={},
        typemap=options.typemap)

# for n in es.nodes:
#     pprint.pprint(n.__dict__)
es.timeindex = es.timeindex[0:5]
m = Model(es)

m.pprint()
m.solve()

# get component results
cr = pp.component_results(es, m.results(), select='sequences')

# get bus results
br = pp.bus_results(es, m.results(), select='scalars')

# select on bus and reduce multiindex
br['bus0'].xs([es.groups['bus0'], 'invest'], level=[1, 2])







#supply = cr['load'].xs(['bus0', 'flow'], axis=1, level=[0, 2])
