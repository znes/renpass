# from plot import Demand, ImportExport etc...

def export_html_report(results):
    # maybe use plotly.offline as described here to generate HTML divs --> second answer
    # and cufflinks for using pandas plotting functionality
    # https://stackoverflow.com/questions/36262748/python-save-plotly-plot-to-local-file-and-insert-into-html

    from plot import (get_countrycodes_techs, get_prices, get_load,
                      get_hourly_dispatch, get_transmission, plot_gen_load_prices,
                      plot_hourly_dispatch, plot_yearly_sums, plot_transmission)


    plots = []

    #plots.append(plot_prices(results))
    countrycodes, techs = get_countrycodes_techs(results)
    prices = get_prices(results, countrycodes)
    load = get_load(results, countrycodes)
    timelines = get_hourly_dispatch(countrycodes, techs, results)
    transmission = get_transmission(results)
    plots.append(plot_hourly_dispatch(timelines))
    plots.append(plot_gen_load_prices(timelines, load, prices))
    plots.append(plot_yearly_sums(timelines, techs))
    plots.append(plot_transmission(transmission, countrycodes))

    head = """ <html><head> <script src="https://cdn.plot.ly/plotly-latest.min.js"></script> </head>"""

    #TODO Something is not working with hourly_dispatch
    tmp = plots[0]
    plots = plots[1:]

    html = head + "<body>" + "".join(plots) + "</body></html>"

    # export to html
    f = open('report.html', 'w')
    f.write(html)
    f.close()

    pass
