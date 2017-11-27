# from plot import Demand, ImportExport etc...

def export_html_report(results):
    # maybe use plotly.offline as described here to generate HTML divs --> second answer
    # and cufflinks for using pandas plotting functionality
    # https://stackoverflow.com/questions/36262748/python-save-plotly-plot-to-local-file-and-insert-into-html
    
    from plot import (get_countrycodes_techs, get_hourly_dispatch, get_transmission,
                      plot_hourly_dispatch, plot_yearly_sums, plot_transmission)

    head = "<head> </head>"
    plots = []

    plots.append(plot_prices(results))
    countrycodes, techs = get_countrycodes_techs(results)
    timelines = get_hourly_dispatch(countrycodes, techs, results)
    transmission = get_transmission(results)
    plot_hourly_dispatch(timelines)
    plot_yearly_sums(timelines, techs)
    plot_transmission(transmission, countrycodes)
    

    head + div for div in plots
    # export to html

    pass
