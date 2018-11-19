from oemof.outputlib import views, processing
from oemof.solph import EnergySystem, Model

from renpass import options
from renpass import postprocessing as pp

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

m.solve()

# get component results
cr = pp.component_results(es, m.results(), select='sequences')

# get bus results
br = pp.bus_results(es, m.results(), select='scalars')

# select on bus and reduce multiindex
br['bus0'].xs([es.groups['bus0'], 'invest'], level=[1, 2])

pp.supply_results(results=m.results(), es=es, bus=['heat-bus'])

pp.supply_results(results=m.results(), es=es, bus=['bus0', 'bus1'])

pp.demand_results(results=m.results(), es=es, bus=['bus0', 'bus1'])

views.node_input_by_type(m.results(), node_type=options.typemap['storage'],
                         droplevel=[2])

views.node_output_by_type(m.results(), node_type=options.typemap['storage'],
                         droplevel=[2])

views.node_weight_by_type(m.results(), node_type=options.typemap['storage'])

views.net_storage_flow(results=m.results(), node_type=options.typemap['storage'])



views.node(processing.parameter_as_dict(es), es.nodes[0], multiindex=True)['scalars']

pp.bus_results(es, m.results(), select='scalars', aggregate=True)
