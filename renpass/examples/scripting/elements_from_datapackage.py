
from oemof.solph import EnergySystem, Model
import options
import pprint


dispatch = False
investment = True

if dispatch:
    es1 = EnergySystem.from_datapackage(
        'examples/dispatch/datapackage.json',
        attributemap={},
        typemap=options.typemap)

    for n in es1.nodes:
        pprint.pprint(n.__dict__)


if investment:
    es2 = EnergySystem.from_datapackage(
        'examples/investment/datapackage.json',
        attributemap={},
        typemap=options.typemap)

    for n in es2.nodes:
        pprint.pprint(n.__dict__)

    m = Model(es2)


m.solve()
