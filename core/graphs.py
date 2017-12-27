from plotly.offline import plot
from plotly.graph_objs import *

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext as _


no_margin = Margin(l=0, r=0, b=0, t=0, pad=0)
no_margin_with_padding = Margin(l=60, r=0, b=0, t=30, pad=0)

def plot_web(xys, title, variable, unit, names=None, xaxis_title=_('time'), mode="lines+markers"):
    '''Plot time series'''
    data = [Scatter(x=xy[0], y=xy[1], mode=mode) for xy in xys]
    if not names is None:
        for i in range(len(data)):
            data[i].name = names[i]
    return plot({
        'data': data,
        'layout': Layout(
            title=title,
            margin=no_margin_with_padding,
            legend=dict(orientation="h"),
            xaxis={'title':xaxis_title},
            yaxis={'title': "%s (%s)"%(str(variable), str(unit))}
        )}, auto_open=False, output_type='div')

def box_plot(xys, title, variable, unit, names=[], xaxis_title=_('time')):
    '''Funtion that plot boxplot'''
    data = [Scatter(x=xys[0][0], y=xys[0][1], mode='markers')]
    data.extend([Box(x=xy[0], y=xy[1], whiskerwidth=50, marker=dict(size=2)) for xy in xys[1:]])
    if names:
        for i in range(len(data)):
            data[i].name = names[i]
    return plot({
        'data': data,
        'layout': Layout(
            title=title,
            margin=no_margin_with_padding,
            legend=dict(orientation="h"),
            xaxis={'title':xaxis_title},
            yaxis={'title': "%s (%s)"%(str(variable), str(unit))}
        )}, auto_open=False, output_type='div')

def plot_polar(xys, title, variable, unit, names=[]):
    data = [Scatter(t=[d.strftime("%Y") for d in xy[0]], r=xy[1],mode='lines+markers',marker=dict(opacity=0.7)) for xy in xys]
    if names:
        for i in range(len(data)):
            data[i].name=names[i]
    return plot({
                    'data':data,
                    'layout':Layout(title=title,orientation=-90,xaxis={'title':_('time')},)

                },auto_open=False, output_type='div')

def plot_map(lat, lon, text):
    '''Plot map of stations'''
    mpt = 'pk.eyJ1IjoiYWRlbHNvbmpyIiwiYSI6ImNqNTV0czRkejBnMnkzMnBtdXdsbmRlbDcifQ.Ox8xbLTD_cD7h3uEz13avQ'
    data = Data([
        Scattermapbox(
            lat=lat,
            lon=lon,
            mode='markers',
            marker=Marker(size=14, color='rgb(0, 50, 40)'),
            text=text
        )
    ])
    layout = Layout(
        autosize=True,
        margin=no_margin,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mpt,
            bearing=0,
            center=dict(lat=float(lat[0]), lon=float(lon[0])),
            pitch=0,
            zoom=7
        )
    )
    fig = dict(data=data, layout=layout)
    return plot(fig, auto_open=False, output_type='div')
