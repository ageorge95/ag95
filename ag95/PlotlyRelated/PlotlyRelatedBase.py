from typing import List,\
    Dict
import plotly.graph_objects as go
from datetime import datetime,\
    timedelta
from plotly.subplots import make_subplots

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

class MultiRowPlot:
    def __init__(self,
                 plots: List[ScatterPlotDef] | List[BarPlotDef]):

        self.plots = plots

    def _return_html_plot(self,
                          plot_type: type(go.Scatter) | type(go.Bar),
                          show_fig: bool = False,
                          include_plotlyjs: bool = False):

        fig = make_subplots(rows=len(self.plots),
                            cols=1,
                            shared_xaxes=True,
                            # subplot_titles=initial_subplot_titles
                            )

        for row_id, plot in enumerate(self.plots, 1):
            traces = []
            for i in range(len(plot.x_axis)):
                kwargs = {'x': plot.x_axis[i],
                          'y': plot.y_axis[i]}
                if plot.name:
                    kwargs.update({'name': plot.name[i]})
                if hasattr(plot, 'forced_width'):
                    if plot.forced_width:
                        kwargs.update({'width': plot.forced_width})

                traces.append(plot_type(**kwargs))

            fig.add_traces(traces,
                           rows=row_id,
                           cols=1)
            if plot.v_rects:
                for _ in plot.v_rects:
                    fig.add_vrect(**_ | {'row': row_id,
                                         'col': 1})
            if plot.h_rects:
                for _ in plot.h_rects:
                    fig.add_hrect(**_ | {'row': row_id,
                                         'col': 1})

            if plot.forced_y_limits:
                fig.update_yaxes(range=[plot.forced_y_limits[0], plot.forced_y_limits[1]],
                                 row=row_id,
                                 col=1)

            if any([plot.force_show_until_current_datetime, plot.grey_out_missing_data_until_current_datetime]):
                # limit the plot horizontally, to see the missing data until the current time
                oldest_datapoint_refined = min([min(_) for _ in plot.x_axis])-timedelta(seconds=5)
                newest_datapoint_refined = max([max(_) for _ in plot.x_axis])+timedelta(seconds=5)
                fig.update_xaxes(range=[oldest_datapoint_refined, newest_datapoint_refined],
                                 row=row_id,
                                 col=1)

                if plot.force_show_until_current_datetime:
                    # force show up until the current datetime
                    fig.update_layout(xaxis_range=[oldest_datapoint_refined, plot.now])

                if plot.grey_out_missing_data_until_current_datetime:
                    # mark the missing data up until the current datetime with grey
                    fig.add_vrect(x0=max([max(_) for _ in plot.x_axis]),
                                  x1=plot.now,
                                  fillcolor='grey',
                                  opacity=0.5,
                                  row=row_id,
                                  col=1)

        # force show the x axis to show on all subplots
        # xaxis{n}_showticklabels is needed for each axis in order to show the x axis, when the shared_axes is ON
        if len(self.plots) > 1:
            force_show_x_axis_args = dict([[f'xaxis{i}_showticklabels', True] for i, _ in enumerate(range(2,len(self.plots)+1),1)])
            fig.update_layout(**force_show_x_axis_args)

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