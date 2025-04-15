from typing import (List,
                    Dict,
                    Literal)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import (datetime,
                      timedelta)

class ScatterPlotDef:
    def __init__(self,
                 x_axis: List[List],
                 y_axis: List[List],
                 colors: List[str] | bool = None,
                 title: str | bool = None,
                 forced_y_limits: List[int] = None,
                 v_rects: List[Dict] = None,
                 h_rects: List[Dict] = None,
                 name: List = None,
                 force_show_until_current_datetime: bool = False,
                 grey_out_missing_data_until_current_datetime: bool = False,
                 fill_method: List[Literal["tonexty", "tozeroy"]] | bool = None):

        self.x_axis = x_axis
        self.y_axis = y_axis
        self.colors = colors
        self.title = title
        self.forced_y_limits = forced_y_limits
        self.v_rects = v_rects
        self.h_rects = h_rects
        self.name = name
        self.force_show_until_current_datetime = force_show_until_current_datetime
        self.grey_out_missing_data_until_current_datetime = grey_out_missing_data_until_current_datetime
        self.fill_method = fill_method

        self.now = datetime.now()

class BarPlotDef:
    def __init__(self,
                 x_axis: List[List],
                 y_axis: List[List],
                 colors: List[str] | bool = None,
                 title: str | bool = None,
                 forced_y_limits: List[int] = None,
                 v_rects: List[Dict] = None,
                 h_rects: List[Dict] = None,
                 name: List = None,
                 force_show_until_current_datetime: bool = False,
                 grey_out_missing_data_until_current_datetime: bool = False,
                 forced_width: float = 0):

        self.x_axis = x_axis
        self.y_axis = y_axis
        self.colors = colors
        self.title = title
        self.forced_y_limits = forced_y_limits
        self.v_rects = v_rects
        self.h_rects = h_rects
        self.name = name
        self.force_show_until_current_datetime = force_show_until_current_datetime
        self.grey_out_missing_data_until_current_datetime = grey_out_missing_data_until_current_datetime
        self.forced_width = forced_width

        self.now = datetime.now()

class HistogramPlotDef:
    def __init__(self,
                 x_axis: List[List],
                 y_axis: List[List],
                 colors: List[str] | bool = None,
                 title: str | bool = None,
                 forced_y_limits: List[int] = None,
                 v_rects: List[Dict] = None,
                 h_rects: List[Dict] = None,
                 name: List = None,
                 force_show_until_current_datetime: bool = False,
                 grey_out_missing_data_until_current_datetime: bool = False,
                 forced_width: float = 0):

        self.x_axis = x_axis
        self.y_axis = y_axis
        self.colors = colors
        self.title = title
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
                 plot: ScatterPlotDef | BarPlotDef | HistogramPlotDef):

        self.plot = plot

    def _return_html_plot(self,
                          plot_type: type(go.Scatter) | type(go.Bar) | type(go.Histogram),
                          show_fig: bool = False,
                          include_plotlyjs: bool = False):
        data = []
        for i in range(len(self.plot.x_axis)):
            kwargs = {'x': self.plot.x_axis[i],
                      'y': self.plot.y_axis[i]}
            if self.plot.name:
                kwargs |= ({'name': self.plot.name[i]})
            if self.plot.colors:
                if plot_type.__name__ is go.Scatter.__name__:
                    kwargs |= ({'line': {'color': self.plot.colors[i]}})
                elif (plot_type.__name__ is go.Bar.__name__ or
                      plot_type.__name__ is go.Histogram.__name__):
                    kwargs |= ({'marker_color': self.plot.colors[i]})
            if hasattr(self.plot, 'forced_width'):
                if self.plot.forced_width:
                    kwargs |= ({'width': self.plot.forced_width})
            # fill method for scatter plots
            if hasattr(self.plot, 'fill_method'):
                if self.plot.fill_method:
                    kwargs |= ({'fill': self.plot.fill_method[i]})

            data.append(plot_type(**kwargs))

        fig = go.Figure(data=data,
                        layout={'title_text': self.plot.title})

        # add any eventual vertical or horizontal rectangles
        if self.plot.v_rects:
            for _ in self.plot.v_rects:
                fig.add_vrect(**_)
        if self.plot.h_rects:
            for _ in self.plot.h_rects:
                fig.add_hrect(**_)

        update_args = {}

        if any([self.plot.force_show_until_current_datetime, self.plot.grey_out_missing_data_until_current_datetime]):
            oldest_datapoint_refined = min([min(_) for _ in self.plot.x_axis])-timedelta(seconds=5)
            newest_datapoint_refined = max([max(_) for _ in self.plot.x_axis])+timedelta(seconds=5)

            if self.plot.force_show_until_current_datetime and not self.plot.grey_out_missing_data_until_current_datetime:
                # force show up until the current datetime
                update_args |= {'xaxis_range': [oldest_datapoint_refined, self.plot.now]}

            if self.plot.grey_out_missing_data_until_current_datetime and not self.plot.force_show_until_current_datetime:
                # limit the plot horizontally, to see the missing data until the current time
                update_args |= {'xaxis_range': [oldest_datapoint_refined, newest_datapoint_refined]}

                # mark the missing data up until the current datetime with grey
                fig.add_vrect(x0=max([max(_) for _ in self.plot.x_axis]),
                              x1=self.plot.now,
                              fillcolor='grey',
                              opacity=0.5)

            if self.plot.force_show_until_current_datetime and self.plot.grey_out_missing_data_until_current_datetime:
                # force show up until the current datetime
                update_args |= {'xaxis_range': [oldest_datapoint_refined, self.plot.now]}

                # mark the missing data up until the current datetime with grey
                fig.add_vrect(x0=max([max(_) for _ in self.plot.x_axis]),
                              x1=self.plot.now,
                              fillcolor='grey',
                              opacity=0.5)

        if self.plot.forced_y_limits:
            # force show only a certain y axis portion
            update_args |= {'yaxis_range': [self.plot.forced_y_limits[0], self.plot.forced_y_limits[1]]}

        # remove the excessive white margins
        update_args |= {'margin': dict(l=25, r=25, t=25, b=25)}

        # update data on hover by default
        update_args |= {'hovermode': 'x'}

        fig.update_layout(**update_args)

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

    def return_html_HistogramPlot(self,
                                  show_fig: bool = False,
                                  include_plotlyjs: bool = False):
        return self._return_html_plot(plot_type=go.Histogram,
                                      show_fig=show_fig,
                                      include_plotlyjs=include_plotlyjs)

class MultiRowPlot:
    def __init__(self,
                 plots: List[ScatterPlotDef] | List[BarPlotDef],
                 title: str | bool = None,
                 height: int = None,
                 showlegend: bool = True):

        self.plots = plots
        self.title = title
        self.height = height
        self.showlegend = showlegend

    def _return_html_plot(self,
                          plot_type: type(go.Scatter) | type(go.Bar),
                          show_fig: bool = False,
                          include_plotlyjs: bool = False,
                          use_hoversubplots: bool = False):

        if use_hoversubplots:
            return self._return_html_plot_with_hoversubplots(plot_type = plot_type,
                                                              show_fig = show_fig,
                                                              include_plotlyjs = include_plotlyjs)
        else:
            return self._return_html_plot_without_hoversubplots(plot_type=plot_type,
                                                                show_fig=show_fig,
                                                                include_plotlyjs=include_plotlyjs)

    def _return_html_plot_without_hoversubplots(self,
                                                plot_type: type(go.Scatter) | type(go.Bar),
                                                show_fig: bool = False,
                                                include_plotlyjs: bool = False):

        fig = make_subplots(rows=len(self.plots),
                            cols=1,
                            shared_xaxes=True,
                            subplot_titles=[_.title for _ in self.plots],
                            vertical_spacing = (1/len(self.plots)) * 0.25)

        for row_id, plot in enumerate(self.plots, 1):
            traces = []
            for i in range(len(plot.x_axis)):
                kwargs = {'x': plot.x_axis[i],
                          'y': plot.y_axis[i]}
                if plot.name:
                    kwargs |= ({'name': plot.name[i]})
                if plot.colors:
                    if plot_type.__name__ is go.Scatter.__name__:
                        kwargs |= ({'line': {'color': plot.colors[i]}})
                    if plot_type.__name__ is go.Bar.__name__:
                        kwargs |= ({'marker_color': plot.colors[i]})
                if hasattr(plot, 'forced_width'):
                    if plot.forced_width:
                        kwargs |= ({'width': plot.forced_width})
                # fill method for scatter plots
                if hasattr(plot, 'fill_method'):
                    if plot.fill_method:
                        kwargs |= ({'fill': plot.fill_method[i]})

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
                oldest_datapoint_refined = min([min(_) for _ in plot.x_axis])-timedelta(seconds=5)
                newest_datapoint_refined = max([max(_) for _ in plot.x_axis])+timedelta(seconds=5)

                if plot.grey_out_missing_data_until_current_datetime and not plot.force_show_until_current_datetime:
                    # mark the missing data up until the current datetime with grey
                    fig.add_vrect(x0=max([max(_) for _ in plot.x_axis]),
                                  x1=plot.now,
                                  fillcolor='grey',
                                  opacity=0.5,
                                  row=row_id,
                                  col=1)

                    # limit the plot horizontally, to see the missing data until the current time
                    fig.update_xaxes(range=[oldest_datapoint_refined, newest_datapoint_refined])

                if plot.force_show_until_current_datetime and not plot.grey_out_missing_data_until_current_datetime:
                    # force show up until the current datetime
                    fig.update_xaxes(range=[oldest_datapoint_refined, plot.now])

                if plot.force_show_until_current_datetime and plot.grey_out_missing_data_until_current_datetime:
                    # force show up until the current datetime
                    fig.update_layout(xaxis_range=[oldest_datapoint_refined, plot.now])

                    # mark the missing data up until the current datetime with grey
                    fig.add_vrect(x0=max([max(_) for _ in plot.x_axis]),
                                  x1=plot.now,
                                  fillcolor='grey',
                                  opacity=0.5,
                                  row=row_id,
                                  col=1)

        update_args = {'title_text': self.title,
                       'showlegend': self.showlegend}

        # update the height if requested
        if self.height:
            update_args |= {'height': self.height}

        # force the tick labels by default
        update_args |= {'xaxis_showticklabels': True}

        # update data on hover by default
        update_args |= {'hovermode': 'x'}

        # remove the excessive white margins
        update_args |= {'margin': dict(l=0, r=0, t=25, b=25)} if not self.title\
            else {'margin': dict(l=0, r=0, t=42, b=25)}

        # fully show the trace name by default
        update_args |= {'hoverlabel_namelength': -1}

        # force show the x axis to show on all subplots
        # xaxis{n}_showticklabels is needed for each axis in order to show the x axis, when the shared_axes is ON
        if len(self.plots) > 1:
            force_show_x_axis_args = dict([[f'xaxis{i}_showticklabels', True] for i, _ in enumerate(range(2,len(self.plots)+1),1)])
            update_args |= force_show_x_axis_args

        fig.update_layout(**update_args)

        if show_fig:
            fig.show()

        return fig.to_html(include_plotlyjs=include_plotlyjs)

    def _return_html_plot_with_hoversubplots(self,
                                             plot_type: type(go.Scatter) | type(go.Bar),
                                             show_fig: bool = False,
                                             include_plotlyjs: bool = False):
        # NOTE for future self: make_subplots() would have worked better in this case
        # BUT as of Apr25 the hoversubplots feature only works via the go.Figure() plot creation method

        # #############################################
        # ########## Initial layout configuration #####
        # #############################################
        # initial plot layout
        layout = dict(
            hoversubplots="axis", # enable parallel cursor hovering over all the subplots
            hoverlabel_namelength=-1, # fully show the trace name by default
            title=dict(text=self.title), # the title of the plot (NOT of the subplots but of the larger plot)
            hovermode="x", # update data on hover by default
            grid=dict(rows=len(self.plots), columns=1), # pre-configure the structure of the plot
            xaxis=dict( # configure the x axis
                # FAKE XAXIS ANNOTATIONS DISABLED for now as it looks bad when a large number of datapoints are plotted
                # domain=[0, 1], # add the full possible domain range
                anchor=f"y{len(self.plots)}", # Anchor to bottom y-axis
                showticklabels=True # force the tick labels by default
            ),
        )

        # update the height if requested
        if self.height:
            layout |= dict(height=self.height)

        # remove the excessive white margins
        layout |= {'margin': dict(l=0, r=0, t=25, b=25)} if not self.title \
            else {'margin': dict(l=0, r=0, t=42, b=25)}

        # FAKE XAXIS ANNOTATIONS DISABLED for now as it looks bad when a large number of datapoints are plotted
        # # NOTE currently there is no automatic way to add the x_axis under each subplot using go.Figure()
        # # so I had to come up with this mechanism that adds fake x axis values via annotations
        # # first compute the domain for each subplot
        # total_subplots_number = len(self.plots)
        # max_domain_per_subplot = 1 / total_subplots_number
        # domain_space_between_subplots = 0.05 # controls the space between subplots
        # y_domains = dict([f'yaxis{total_subplots_number - _}' if (total_subplots_number - _) > 1 else 'yaxis',
        #                   [max_domain_per_subplot * (_) + (domain_space_between_subplots if _ else 0),
        #                    max_domain_per_subplot * (_ + 1)]] for _ in range(total_subplots_number))
        # # example for total_subplots_number == 3
        # # y_domains = {
        # #     'yaxis3': [0.0, 0.33],
        # #     'yaxis2': [0.38, 0.66],
        # #     'yaxis': [0.71, 1.0]
        # # }
        # # example for total_subplots_number == 2
        # # y_domains = {
        # #     'yaxis2': [0.0, 0.5],
        # #     'yaxis': [0.55, 1.0]
        # # }
        #
        # # add the domains for each subplot
        # for row_id, _ in enumerate(self.plots, 1):
        #     relevant_y_axis_name = f'yaxis{row_id}' if row_id > 1 else 'yaxis'
        #     layout |= {relevant_y_axis_name: dict(domain=y_domains[relevant_y_axis_name])}

        # #############################################
        # ########## Pre figure creation logic ########
        # #############################################
        subplots_data = []

        # create the initial plots
        for row_id, plot in enumerate(self.plots, 1):
            for i in range(len(plot.x_axis)):
                kwargs = {
                    'x': plot.x_axis[i],
                    'y': plot.y_axis[i],
                    'xaxis': 'x',
                    'yaxis': f'y{row_id}' if row_id > 1 else 'y',
                    'showlegend': self.showlegend
                }
                if plot.name:
                    kwargs |= ({'name': plot.name[i]})

                if plot.colors:
                    if plot_type.__name__ is go.Scatter.__name__:
                        kwargs |= ({'line': {'color': plot.colors[i]}})
                    if plot_type.__name__ is go.Bar.__name__:
                        kwargs |= ({'marker_color': plot.colors[i]})
                if hasattr(plot, 'forced_width'):
                    if plot.forced_width:
                        kwargs |= ({'width': plot.forced_width})
                # fill method for scatter plots
                if hasattr(plot, 'fill_method'):
                    if plot.fill_method:
                        kwargs |= ({'fill': plot.fill_method[i]})

                subplot = plot_type(**kwargs)

                subplots_data.append(subplot)

        # #############################################
        # ########## figure creation logic ############
        # #############################################
        fig = go.Figure(data=subplots_data, layout=layout)

        # #############################################
        # ########## Post figure creation logic #######
        # #############################################
        for row_id, plot in enumerate(self.plots, 1):
            # add custom v_rects over the created figure
            if plot.v_rects:
                for _ in plot.v_rects:
                    fig.add_vrect(**_ | {'xref': 'x',
                                         'yref': f'y{row_id}'})

            # add custom h_rects over the created figure
            if plot.h_rects:
                for _ in plot.h_rects:
                    fig.add_hrect(**_ | {'xref': 'x',
                                         'yref': f'y{row_id}'})

            # if there are any forced limits specified, apply them for the relevant subplots
            if plot.forced_y_limits:
                fig.update_layout(
                    {f'yaxis{row_id}': dict(range=[plot.forced_y_limits[0], plot.forced_y_limits[1]])}
                )

            # apply any force_show_until_current_datetime and/ or grey_out_missing_data_until_current_datetime constrains
            if any([plot.force_show_until_current_datetime, plot.grey_out_missing_data_until_current_datetime]):
                    oldest_datapoint_refined = min([min(_) for _ in plot.x_axis]) - timedelta(seconds=5)
                    newest_datapoint_refined = max([max(_) for _ in plot.x_axis]) + timedelta(seconds=5)

                    if plot.grey_out_missing_data_until_current_datetime and not plot.force_show_until_current_datetime:
                        # mark the missing data up until the current datetime with grey
                        fig.add_vrect(x0=max([max(_) for _ in plot.x_axis]),
                                      x1=plot.now,
                                      fillcolor='grey',
                                      opacity=0.5,
                                      xref = 'x',
                                      yref = f'y{row_id}')

                        # limit the plot horizontally, to see the missing data until the current time
                        fig.update_xaxes(range=[oldest_datapoint_refined, newest_datapoint_refined])

                    if plot.force_show_until_current_datetime and not plot.grey_out_missing_data_until_current_datetime:
                        # force show up until the current datetime
                        fig.update_xaxes(range=[oldest_datapoint_refined, plot.now])

                    if plot.force_show_until_current_datetime and plot.grey_out_missing_data_until_current_datetime:
                        # force show up until the current datetime
                        fig.update_layout(xaxis_range=[oldest_datapoint_refined, plot.now])

                        # mark the missing data up until the current datetime with grey
                        fig.add_vrect(x0=max([max(_) for _ in plot.x_axis]),
                                      x1=plot.now,
                                      fillcolor='grey',
                                      opacity=0.5,
                                      xref = 'x',
                                      yref = f'y{row_id}')

        # FAKE XAXIS ANNOTATIONS DISABLED for now as it looks bad when a large number of datapoints are plotted
        # # create and add the fake x axis values via annotations for each subplot except the last bottom one
        # if len(self.plots) > 1:
        #     annotations = []
        #     for row_id, plot in enumerate(self.plots[:-1], 1): # skip the last subplot
        #         relevant_y_axis_name = f'yaxis{row_id}' if row_id > 1 else 'yaxis'
        #         domain = y_domains[relevant_y_axis_name]
        #         location_y = domain[0]
        #         for tick, text in zip(self.plots[0].x_axis[0],
        #                               self.plots[0].x_axis[0]):
        #             annotations.append(dict(
        #                 x=tick,
        #                 y=location_y,
        #                 text=str(text),
        #                 showarrow=False,
        #                 xanchor="center",
        #                 yanchor="top",
        #                 xref="x",
        #                 yref="paper",
        #                 font=dict(size=10, color="gray")
        #             ))
        #     fig.update_layout(
        #         annotations=annotations
        #     )

        if show_fig:
            fig.show()

        return fig.to_html(include_plotlyjs=include_plotlyjs)

    def return_html_ScatterPlot(self,
                                show_fig: bool = False,
                                include_plotlyjs: bool = False,
                                use_hoversubplots: bool = False):
        return self._return_html_plot(plot_type=go.Scatter,
                                      show_fig=show_fig,
                                      include_plotlyjs=include_plotlyjs,
                                      use_hoversubplots=use_hoversubplots)

    def return_html_BarPlot(self,
                            show_fig: bool = False,
                            include_plotlyjs: bool = False,
                            use_hoversubplots: bool = False):
        return self._return_html_plot(plot_type=go.Bar,
                                      show_fig=show_fig,
                                      include_plotlyjs=include_plotlyjs,
                                      use_hoversubplots=use_hoversubplots)