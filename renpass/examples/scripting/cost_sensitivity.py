from oemof.outputlib import views, processing
from oemof.solph import EnergySystem, Model

from renpass import options
from renpass import postprocessing as pp

objective = {}

es = EnergySystem.from_datapackage(
    'renpass/examples/investment/datapackage.json',
    attributemap={},
    typemap=options.typemap)

m = Model(es)

capacity_costs = [0, 1000]

for c in capacity_costs:
    es.groups['bp'].capacity_cost = c
    es.groups['bp'].update()
    m.flows = m.es.flows() # should not be necessary (oemof bug! )

    m._add_objective(update=True)
    m.solve()

    objective[c] = m.objective()
