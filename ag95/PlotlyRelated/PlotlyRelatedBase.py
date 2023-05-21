from threading import Thread
from time import sleep
from typing import List,\
    Dict
from multiprocessing import Manager
from datetime import datetime,\
    timedelta
import plotly.graph_objects as go
from multiprocessing import Queue
from sys import stdin
from ag95 import configure_logger

class ScatterPlotDef:
    def __init__(self,
                 x_axis: List[List],
                 y_axis: List[List],
                 forced_y_limits: List[int] = None,
                 v_rects: List[Dict] = None,
                 h_rects: List[Dict] = None,
                 name: List = None,
                 force_show_until_current_datetime: bool = False,
                 grey_out_missing_data_until_current_datetime: bool = False):

        self.x_axis = x_axis
        self.y_axis = y_axis
        self.forced_y_limits = forced_y_limits
        self.v_rects = v_rects
        self.h_rects = h_rects
        self.name = name
        self.force_show_until_current_datetime = force_show_until_current_datetime
        self.grey_out_missing_data_until_current_datetime = grey_out_missing_data_until_current_datetime

        self.now = datetime.now()

class BarPlotDef:
    def __init__(self,
                 x_axis: List[List],
                 y_axis: List[List],
                 forced_y_limits: List[int] = None,
                 v_rects: List[Dict] = None,
                 h_rects: List[Dict] = None,
                 name: List = None,
                 force_show_until_current_datetime: bool = False,
                 grey_out_missing_data_until_current_datetime: bool = False,
                 forced_width: float = 0):

        self.x_axis = x_axis
        self.y_axis = y_axis
        self.forced_y_limits = forced_y_limits
        self.v_rects = v_rects
        self.h_rects = h_rects
        self.name = name
        self.force_show_until_current_datetime = force_show_until_current_datetime
        self.grey_out_missing_data_until_current_datetime = grey_out_missing_data_until_current_datetime
        self.forced_width = forced_width

        self.now = datetime.now()

class SinglePlot:
    def __init__(self,
                 plot: ScatterPlotDef | BarPlotDef):

        self.plot = plot

    def _return_html_plot(self,
                          plot_type: type(go.Scatter) | type(go.Bar),
                          show_fig: bool = False,
                          include_plotlyjs: bool = False):
        data = []
        for i in range(len(self.plot.x_axis)):
            kwargs = {'x': self.plot.x_axis[i],
                      'y': self.plot.y_axis[i]}
            if self.plot.name:
                kwargs.update({'name': self.plot.name[i]})
            if hasattr(self.plot, 'forced_width'):
                if self.plot.forced_width:
                    kwargs.update({'width': self.plot.forced_width})

            data.append(plot_type(**kwargs))

        fig = go.Figure(data=data)

        # add any eventual vertical or horizontal rectangles
        if self.plot.v_rects:
            for _ in self.plot.v_rects:
                fig.add_vrect(**_)
        if self.plot.h_rects:
            for _ in self.plot.h_rects:
                fig.add_hrect(**_)

        if any([self.plot.force_show_until_current_datetime, self.plot.grey_out_missing_data_until_current_datetime]):
            # limit the plot horizontally, to see the missing data until the current time
            oldest_datapoint_refined = min([min(_) for _ in self.plot.x_axis])-timedelta(seconds=5)
            newest_datapoint_refined = max([max(_) for _ in self.plot.x_axis])+timedelta(seconds=5)
            fig.update_layout(xaxis_range=[oldest_datapoint_refined, newest_datapoint_refined])

            if self.plot.force_show_until_current_datetime:
                # force show up until the current datetime
                fig.update_layout(xaxis_range=[oldest_datapoint_refined, self.plot.now])

            if self.plot.grey_out_missing_data_until_current_datetime:
                # mark the missing data up until the current datetime with grey
                fig.add_vrect(x0=max([max(_) for _ in self.plot.x_axis]),
                              x1=self.plot.now,
                              fillcolor='grey',
                              opacity=0.5)

        if self.plot.forced_y_limits:
            # force show only a certain y axis portion
            fig.update_layout(yaxis_range=[self.plot.forced_y_limits[0], self.plot.forced_y_limits[1]])

        if show_fig:
            fig.show()

        return fig.to_html(include_plotlyjs=include_plotlyjs)

    def return_html_ScatterPlot(self,
                                show_fig: bool = False,
                                include_plotlyjs: bool = False):
        return self._return_html_plot(plot_type=go.Scatter,
                                      show_fig=show_fig,
                                      include_plotlyjs=include_plotlyjs)

    def return_html_BarPlot(self,
                            show_fig: bool = False,
                            include_plotlyjs: bool = False):
        return self._return_html_plot(plot_type=go.Bar,
                                      show_fig=show_fig,
                                      include_plotlyjs=include_plotlyjs)