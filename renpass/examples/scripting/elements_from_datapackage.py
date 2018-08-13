
from oemof.solph import EnergySystem, Bus
import options

typemap = options.typemap

es = EnergySystem.from_datapackage(
    'examples/dispatch/datapackage.json',
    attributemap={},
    typemap=typemap)

es.nodes
