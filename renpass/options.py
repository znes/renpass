
from oemof.solph import Bus
from renpass.components import electrical
from renpass import facades

typemap = {
    'bus': Bus,
    'line': electrical.Line,
    'electricalbus': electrical.ElectricalBus,
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
