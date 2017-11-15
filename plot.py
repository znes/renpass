# container for all plotting functions, maybe classes
import plotly.graph_objs as go
import plotly
import pandas as pd
import cufflinks as cf

def plot_prices(results):
    """

    Returns
    -------
    str
        Plotly div.
    """

    prices = results.slice_by(bus_label='DE_bus_el', type='other', obj_label='duals')
    prices = results.slice_by(obj_label='DE_excess')
    data = [go.Scatter(x=prices.index.get_level_values(3), y=prices['val'])]
    plotly.offline.plot(data, filename = 'basic-line', image='png')
    plotly.offline.plot(data, include_plotlyjs=False, output_type='div')
    return


def plot_all(results):
    # get countries used in scenario
    countrycodes = results.index.get_level_values(0).unique().str.split('_', 1)
    countrycodes = set([cc[0] for cc in countrycodes])
    countrycodes.remove('GL')
    # get technologies used in scenario. drop entries with powerlines, resources,
    # and duals
    techs = results.index.get_level_values(2).unique()
    techs = techs[techs.str.contains('powerline') == False]
    techs = techs[techs.str.contains('resource') == False]
    techs = techs[techs.str.contains('duals') == False]
    for cc in countrycodes:
        techs = techs.str.lstrip(cc)
    techs = list(techs.str.lstrip('_').unique())
# =============================================================================
#     drop multiple entries (e.g. hard_coal_0, hard_coal_1,..)
#     i = 0
#     for t in techs:
#         if techs[i][-1].isdigit():
#             techs[i] = techs[i][:-2]
#         i += 1
#     techs = list(set(techs))
# =============================================================================
    # plot hourly resolved generation for each country (use only one entry to test)
    timelines = {}
    for cc in countrycodes:
        plots = {}
        timelines[cc] = pd.DataFrame(index=results.index.get_level_values(3).unique())
        for t in techs:
            try:
                timelines[cc][t] = results.slice_unstacked(obj_label=cc + '_' + t,
                        type='to_bus', bus_label=cc + '_bus_el', formatted=True)
            except KeyError:
                continue
            except ValueError:
                continue
        timelines[cc] = timelines[cc].loc[:, (timelines[cc] != 0).any(axis=0)]
        # two lines below work, but do't show stacked numbers instead of single numbers when hovered with mouse.
        # compare last entry in: https://plot.ly/python/filled-area-plots/#stacked-area-chart-with-original-values 
        fig = timelines[cc][['wind_onshore', 'wind_offshore']].iplot(kind='area', fill=True, asFigure=True, hoverinfo='x+y')
        plotly.offline.plot(fig, filename='timeline', image='png')
# =============================================================================
#         trying to show correct numbers when hovering with mouse. taken from link above
#         for i in range(0, len(timelines[cc].ix[0])):
#             y_txt = [str(y0) for y0 in timelines[cc].ix[:, i]]
#             plots[i] = go.Scatter(x=timelines[cc].index, y=timelines[cc].ix[:, i], text=y_txt, hoverinfo='x+text')
#             
#         y_txt = [str(y0) for y0 in timelines[cc].ix[:, 0]]
#         plots[0] = [go.Scatter(x=timelines[cc].index, y=timelines[cc].ix[:, 0], text=y_txt, hoverinfo='x+text')]
#         #fig = go.Figure(plots)
#         plotly.offline.plot(plots, filename='timeline')
# =============================================================================
            
        
        
    # help to understand resultsdataframe    
    results.slice_by(obj_label='DE_excess')['val']
    results[results.index.get_level_values(2).str.contains('lignite') == True]
    results.index.get_level_values(2)[results.index.get_level_values(2).str.contains('hard_coal') == True].unique()
    
    eg['excess']=results.slice_unstacked(obj_label='DE_excess', type='to_bus', bus_label='DE_bus_el', formatted=True)
    
    results.slice_by(obj_label='DE_load')
    results.index.get_level_values(2).unique()