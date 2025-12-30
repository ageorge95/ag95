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
                 fill_method: List[Literal["tonexty", "tozeroy"]] | bool = None,
                 use_full_number_format: bool = False,
                 x_annotations: List[List] = None):

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
        self.use_full_number_format = use_full_number_format
        self.x_annotations = x_annotations

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
                 forced_width: float = 0,
                 use_full_number_format: bool = False,
                 x_annotations: List[List] = None):

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
        self.use_full_number_format = use_full_number_format
        self.x_annotations = x_annotations

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
                 forced_width: float = 0,
                 use_full_number_format: bool = False,
                 x_annotations: List[List] = None):

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
        self.use_full_number_format = use_full_number_format
        self.x_annotations = x_annotations

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

        # fully show the trace name by default
        update_args |= {'hoverlabel_namelength': -1}

        # Check if full number format is requested
        if hasattr(self.plot, 'use_full_number_format') and self.plot.use_full_number_format:
            # Use a smarter format that handles both large numbers and decimal places
            update_args |= {'yaxis': {
                'tickformat': ',.6~f',  # Fixed point format with up to 6 decimal places, remove trailing zeros
                'exponentformat': 'none',  # Disable scientific notation
                'hoverformat': ',.6~f'  # Same format for hover labels
            }}

            # Set number formatting for x-axis only if it's numeric (not datetime)
            # Check if x_axis contains datetime objects
            if len(self.plot.x_axis) > 0 and len(self.plot.x_axis[0]) > 0:
                first_value = self.plot.x_axis[0][0]
                if isinstance(first_value, (int, float)) and not isinstance(first_value, bool):
                    update_args |= {'xaxis': {
                        'tickformat': ',.6~f',
                        'exponentformat': 'none',
                        'hoverformat': ',.6~f'
                    }}

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

        if hasattr(self.plot, 'x_annotations') and self.plot.x_annotations:
                for prediction in self.plot.x_annotations:
                    # add dashed lines
                    fig.add_shape(
                        type="line",
                        x0=prediction[0],
                        x1=prediction[0],
                        y0=0,
                        y1=1,
                        xref="x",
                        yref="paper",
                        layer="above",
                        line=dict(
                            color="Red",
                            width=2,
                            dash="dash",
                        )
                    )

                    # add text annotation
                    fig.add_annotation(
                        x=prediction[0],
                        y=1,    # Place exactly on top of the plot area
                        xref="x",
                        yref="paper",
                        text=f"{prediction[1]}",
                        showarrow=False,
                        yanchor="bottom", # Sit on top of the y position
                        font=dict(
                            color="Red",
                            size=12
                        )
                    )

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

            if hasattr(plot, 'x_annotations') and plot.x_annotations:
                for prediction in plot.x_annotations:
                    # add dashed lines
                    fig.add_shape(
                        type="line",
                        x0=prediction[0], 
                        x1=prediction[0],
                        y0=0,
                        y1=1,
                        xref=f"x{row_id}" if row_id > 1 else "x",
                        yref=f"y{row_id} domain" if row_id > 1 else "y domain",
                        layer="above",
                        line=dict(
                            color="Red",
                            width=2,
                            dash="dash",
                        ),
                        row=row_id,
                        col=1
                    )
                    # add text annotation
                    fig.add_annotation(
                        x=prediction[0],
                        y=1,   # Place exactly on top of the subplot domain
                        xref=f"x{row_id}" if row_id > 1 else "x",
                        yref=f"y{row_id} domain" if row_id > 1 else "y domain",
                        text=f"{prediction[1]}",
                        showarrow=False,
                        yanchor="bottom",
                        font=dict(
                            color="Red",
                            size=12
                        ),
                        # Note: we explicitely avoid passing row=row_id, col=1 here because we are using domain refs
                        # passing row/col would override yref to be data-based
                    )

            if plot.forced_y_limits:
                fig.update_yaxes(range=[plot.forced_y_limits[0], plot.forced_y_limits[1]],
                                 row=row_id,
                                 col=1)

            if hasattr(plot, 'use_full_number_format') and plot.use_full_number_format:
                # Update y-axis formatting for this subplot
                fig.update_yaxes(
                    tickformat=',.6~f',  # Fixed point format with up to 6 decimal places, remove trailing zeros
                    exponentformat='none',
                    hoverformat=',.6~f',  # Format for hover labels
                    row=row_id,
                    col=1
                )

                # Update x-axis formatting only if it's numeric (not datetime)
                if len(plot.x_axis) > 0 and len(plot.x_axis[0]) > 0:
                    first_value = plot.x_axis[0][0]
                    if isinstance(first_value, (int, float)) and not isinstance(first_value, bool):
                        fig.update_xaxes(
                            tickformat=',.6~f',
                            exponentformat='none',
                            hoverformat=',.6~f',
                            row=row_id,
                            col=1
                        )

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
        total_plots = len(self.plots)

        # Use the same vertical spacing calculation as in make_subplots
        vertical_spacing = (1 / total_plots) * 0.25
        plot_height = (1 - (total_plots - 1) * vertical_spacing) / total_plots

        # Build domains from bottom to top
        domains = []
        for i in range(total_plots):
            bottom = i * (plot_height + vertical_spacing)
            top = bottom + plot_height
            domains.append([bottom, top])

        # Reverse so first subplot is at the top
        domains = domains[::-1]

        # initial plot layout
        layout = dict(
            hoversubplots="axis", # enable parallel cursor hovering over all the subplots
            hoverlabel_namelength=-1, # fully show the trace name by default
            title=dict(text=self.title), # the title of the plot (NOT of the subplots but of the larger plot)
            hovermode="x", # update data on hover by default
        )

        # Set domains for each y-axis
        for row_id in range(1, total_plots + 1):
            yaxis_name = f'yaxis{row_id}' if row_id > 1 else 'yaxis'
            layout[yaxis_name] = dict(
                domain=domains[row_id - 1],
                showticklabels=True
            )
            
            # Shared Data Axis Logic:
            # The Main Axis 'xaxis' is used for ALL data traces to ensure perfect hover synchronization.
            # We anchor it to the BOTTOM-MOST plot (row_id = total_plots) so it behaves normally for that plot.
            # For all other UPPER plots, we create "Phantom Axes" just for visual ticks.
            
            # Bottom Plot (Row N) -> Uses the Main Axis 'xaxis'
            if row_id == total_plots:
                 layout['xaxis'] = dict(
                    anchor=yaxis_name.replace('axis', ''), # anchor to yN
                    showticklabels=True,
                    side='bottom'
                 )
            else:
                 # Upper Plots -> Use Phantom Axes (xaxis2, xaxis3...) just for visuals
                 # We use sequential IDs based on row (row 1 -> xaxis2, row 2 -> xaxis3... to avoid collision with main 'xaxis')
                 # ACTUALLY, simpler naming:
                 # Main is xaxis. 
                 # Let's use xaxis_name = xaxis2, xaxis3...
                 phantom_xaxis_name = f'xaxis{row_id + 1}'
                 
                 layout[phantom_xaxis_name] = dict(
                    anchor=yaxis_name.replace('axis', ''), # anchor to y, y2...
                    showticklabels=True,
                    matches='x', # link range/zoom to main axis
                    side='bottom',
                    overlaying='x' # CRITICAL: Overlay on main axis to allow visibility without claiming domain
                 )

        # update the height if requested
        if self.height:
            layout |= dict(height=self.height)

        # Use the same margin calculation as in _return_html_plot_without_hoversubplots
        if not self.title:
            layout |= {'margin': dict(l=0, r=0, t=25, b=25)}
        else:
            layout |= {'margin': dict(l=0, r=0, t=42, b=25)}

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
                    'xaxis': 'x', # ALL traces go to the main axis for sync
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

        # Ghost Trace Injection for Upper Subplots
        # We need to add invisible traces to the phantom axes (xaxis2, xaxis3...) 
        # to force Plotly to render them, otherwise they stay hidden.
        for row_id in range(1, total_plots): # Skip the last subplot (which uses the real axis)
             phantom_xaxis_name = f'xaxis{row_id + 1}' # matches the creation logic above
             
             # Use the first data point from the plot to ensure the axis range isn't distorted
             # Default to 0 if no data exists (edge case)
             try:
                 ghost_x = plot.x_axis[0][0]
                 ghost_y = plot.y_axis[0][0]
             except (IndexError, TypeError):
                 ghost_x = 0
                 ghost_y = 0

             ghost_trace = go.Scatter(
                 x=[ghost_x], y=[ghost_y], 
                 xaxis=phantom_xaxis_name.replace('axis', ''), # x2, x3...
                 yaxis=f'y{row_id}' if row_id > 1 else 'y',
                 opacity=0,
                 showlegend=False,
                 hoverinfo='skip'
             )
             subplots_data.append(ghost_trace)

        # #############################################
        # ########## figure creation logic ############
        # #############################################
        fig = go.Figure(data=subplots_data, layout=layout)

        # #############################################
        # ########## Post figure creation logic #######
        # #############################################

        # Add subplot titles as annotations - place them just above each subplot
        for row_id, plot in enumerate(self.plots, 1):
            if plot.title:
                # Get the domain for this subplot
                domain = domains[row_id - 1]

                # Position the title at the top of the domain with a small offset
                y_position = domain[1] + 0  # Slightly above the top of the plot, no offset needed to avoid overlapping

                # Add annotation as title for this subplot
                fig.add_annotation(
                    xref="paper",
                    yref="paper",
                    x=0.5,  # Center horizontally
                    y=y_position,
                    text=plot.title,
                    showarrow=False,
                    font=dict(size=16, color="black"),
                    yanchor="bottom",
                    xanchor="center"
                )

        for row_id, plot in enumerate(self.plots, 1):
            # add custom v_rects over the created figure
            if plot.v_rects:
                for _ in plot.v_rects:
                    fig.add_vrect(**_ | {'xref': 'x',
                                         'yref': f'y{row_id}'})

            if hasattr(plot, 'x_annotations') and plot.x_annotations:
                for prediction in plot.x_annotations:
                    # add dashed lines
                    fig.add_shape(
                        type="line",
                        x0=prediction[0],
                        x1=prediction[0],
                        y0=0,
                        y1=1,
                        xref=f"x{row_id}" if row_id > 1 else "x",
                        yref=f"y{row_id} domain" if row_id > 1 else "y domain",
                        layer="above",
                        line=dict(
                            color="Red",
                            width=2,
                            dash="dash",
                        )
                    )

                    # add text annotation
                    fig.add_annotation(
                        x=prediction[0],
                        y=1, # Place exactly on top of the subplot (calculated domain)
                        xref="x", # Correctly target shared axis
                        yref=f"y{row_id} domain" if row_id > 1 else "y domain",
                        text=f"{prediction[1]}",
                        showarrow=False,
                        yanchor="bottom",
                        font=dict(
                            color="Red",
                            size=12
                        )
                    )

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

            if hasattr(plot, 'use_full_number_format') and plot.use_full_number_format:
                # Update layout for specific y-axis
                yaxis_key = f'yaxis{row_id}' if row_id > 1 else 'yaxis'
                fig.update_layout(
                    {yaxis_key: dict(
                        tickformat=',.6~f',  # Fixed point format with up to 6 decimal places, remove trailing zeros
                        exponentformat='none',
                        hoverformat=',.6~f'  # Format for hover labels
                    )}
                )

                # Update x-axis only if it's numeric (not datetime)
                if len(plot.x_axis) > 0 and len(plot.x_axis[0]) > 0:
                    first_value = plot.x_axis[0][0]
                    if isinstance(first_value, (int, float)) and not isinstance(first_value, bool):
                        fig.update_layout(
                            xaxis=dict(
                                tickformat=',.6~f',
                                exponentformat='none',
                                hoverformat=',.6~f'
                            )
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