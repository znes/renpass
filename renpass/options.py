
from oemof.solph import Bus
from renpass import components, facades

typemap = {
    'bus': Bus,
    'line': components.electrical.Line,
    'electricalbus': components.electrical.ElectricalBus,
    'extraction': facades.ExtractionTurbine,
    'load': facades.Load,
    'dispatchable': facades.Dispatchable,
    'volatile': facades.Volatile,
    'storage': facades.Storage,
    'reservoir': facades.Reservoir,
    'backpressure': facades.BackpressureTurbine,
    'connection': facades.Connection,
    'conversion': facades.Conversion,
    'excess': facades.Excess,
    'shortage': facades.Shortage}
