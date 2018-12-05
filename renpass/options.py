
from oemof.solph import Bus
from renpass.components import electrical
from renpass import facades

typemap = {
    'bus': Bus,
    'line': electrical.Line,
    'electricalbus': electrical.ElectricalBus,
    'generator': facades.Generator,
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

techmap = {
    'extraction': 'extraction',
    'boiler_central': 'dispatchable',
    'hotwatertank_central': 'storage',
    'backpressure': 'backpressure',
    'boiler_decentral': 'dispatchable',
    'electricity_heatpump': 'conversion',
    'gas_heatpump': 'dispatchable',
    'hotwatertank_decentral': 'storage',
    'ocgt': 'dispatchable',
    'ccgt': 'dispatchable',
    'pv': 'volatile',
    'wind_onshore': 'volatile',
    'wind_offshore': 'volatile',
    'biomass': 'dispatchable',
    'battery': 'storage',
    'ror': 'volatile',
    'phs': 'storage',
    'reservoir': 'dispatchable'
}

techcolor = {
    # 'extraction': 'gray',
    # 'boiler_central': 'sandybrown',
    # 'hotwatertank_central': 'red',
    # 'backpressure': 'gray',
    # 'boiler_decentral': 'sandybrown',
    # 'electricity_heatpump': 'orange',
    # 'gas_heatpump': 'brown',
    # 'hotwatertank_decentral': 'red',
    'acaes': 'brown',
    'ocgt': 'gray',
    'ccgt': 'lightgray',
    'pv': 'gold',
    'wind_onshore': 'skyblue',
    'wind_offshore': 'darkblue',
    'biomass': 'olivedrab',
    'lithium_battery': 'lightsalmon',
    'ror': 'aqua',
    'phs': 'darkred',
    'reservoir': 'magenta'
}

carriercolor = {

}
