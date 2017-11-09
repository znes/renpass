# container for all plotting functions, maybe classes

def plot_prices(results):
    """

    Returns
    -------
    str
        Plotly div.
    """
    import plotly.graph_objs as go
    import plotly
    
    prices = results.slice_by(bus_label='DE_bus_el', type='other', obj_label='duals')
    data = [go.Scatter(x=prices.index.get_level_values(3), y=prices['val'])]
    plotly.offline.plot(data, include_plotlyjs=False, output_type='div')
    return
