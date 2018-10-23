
from oemof.solph import EnergySystem, Model
from renpass import options, postprocessing
import pprint


dispatch = False
investment = True

if dispatch:
    es1 = EnergySystem.from_datapackage(
        'renpass/examples/dispatch/datapackage.json',
        attributemap={},
        typemap=options.typemap)

    for n in es1.nodes:
        pprint.pprint(n.__dict__)


if investment:
    es2 = EnergySystem.from_datapackage(
        'renpass/examples/investment/datapackage.json',
        attributemap={},
        typemap=options.typemap)

    for n in es2.nodes:
        pprint.pprint(n.__dict__)

    m = Model(es2)


m.solve()

postprocessing.system_info(es2)
