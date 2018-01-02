# -*- coding: utf-8 -*-

import requests
import os
from .plot import *


def get_from_url(**arguments):
    """ Download CSV-files and save them in the current working directory.

    Returns
    -----
    arguments: dict
        Updated arguments dictionary pointing to the new file-paths.
    """

    for n in ['NODE_DATA', 'SEQ_DATA']:
        r = requests.get(arguments[n])

        try:
            assert r.status_code == 200
            path = os.path.basename(arguments[n])
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            arguments[n] = path
        except AssertionError:
            print('Could not retrieve %s.' % n)

    return arguments


def html_report(rdf, path='.', fname='report.html'):
    """ Create an HTML-formatted report in the current working directory in
    order to better understand the results

    Parameters
    ----------
    rdf: oemof.outputlib.ResultsDataFrame
        DataFrame holding optimization results.
    path: str
        HTML-file path.
    fname : str
        HTML-file name.
    """
    plots = []

    countrycodes, techs = get_countrycodes_techs(rdf)
    prices = get_prices(rdf, countrycodes)
    load = get_load(rdf, countrycodes)
    timelines = get_hourly_dispatch(countrycodes, techs, rdf)
    transmission = get_transmission(rdf)
    plots.extend(plot_hourly_dispatch(timelines).tolist())
    plots.extend(plot_gen_load_prices(timelines, load, prices).tolist())
    plots.append(plot_yearly_sums(timelines, techs))
    plots.append(plot_transmission(transmission, countrycodes))

    head = """ <html><head>
               <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
               </head> """

    plots = [p for p in plots if isinstance(p, str)]
    html = head + "<body>" + "".join(plots) + "</body></html>"

    # export to html
    f = open(os.path.join(path, fname), 'w')
    f.write(html)
    f.close()
