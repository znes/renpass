# container for all plotting functions, maybe classes

def plot_prices(results):
    """

    Returns
    -------
    str
        Plotly div.
    """
    results.slice_by(bus_label='DE_bus_el', type='other', obj_label='duals')

    return
