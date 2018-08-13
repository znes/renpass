
from oemof.solph import EnergySystem, Bus
from renpass import facades

typemap = {
    'bus': Bus,
    'extraction-turbine': facades.ExtractionTurbine,
    'demand': facades.Load,
    'dispatchable': facades.Dispatchable,
    'volatile': facades.Volatile,
    'storage': facades.Storage,
    'reservoir': facades.Reservoir,
    'backpressure': facades.BackpressureTurbine,
    'connection': facades.Connection,
    'conversion': facades.Conversion,
    'excess': facades.Excess,
    'shortage': facades.Shortage}

es = EnergySystem.from_datapackage(
    'renpass/examples/dispatch/datapackage.json',
    attributemap={},
    typemap=typemap)

es.nodes
