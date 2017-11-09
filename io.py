# from plot import Demand, ImportExport etc...

def export_html_report(results):
    # maybe use plotly.offline as described here to generate HTML divs --> second answer
    # and cufflinks for using pandas plotting functionality
    # https://stackoverflow.com/questions/36262748/python-save-plotly-plot-to-local-file-and-insert-into-html
    head = "<head> </head>"
    plots = []

    plots.append(plot_prices(results))

    head + div for div in plots
    # export to html

    pass
