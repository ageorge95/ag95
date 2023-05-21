from datetime import datetime,\
    timedelta
from ag95 import ScatterPlotDef,\
    SinglePlot

if __name__ == '__main__':
    print('No automatic tests implemented so far; Please check the expected behavior manually.')

    # TEST ScatterPlot single line
    SinglePlot(plot=ScatterPlotDef(x_axis=[[1,2,3,4,5]],
                                   y_axis=[[2,2,2,3,4]])).return_html_ScatterPlot(show_fig=True)
    input(f'You should see a simple plot on screen;'
          f' press any key to continue, if the manual test is passed.')

    # TEST ScatterPlot single line with legend
    SinglePlot(plot=ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4]],
                                   name=['my_plot_line_1'])).return_html_ScatterPlot(show_fig=True)
    input(f'You should see a simple plot on screen with NO legend on the right side;'
          f' press any key to continue, if the manual test is passed.')

    # TEST ScatterPlot double line with legend
    SinglePlot(plot=ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                           [1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4],
                                           [3, 3, 3, 4, 5]],
                                   name=['my_plot_line_1',
                                         'my_plot_line_2'])).return_html_ScatterPlot(show_fig=True)
    input(f'You should see a simple plot on screen with a legend on the right side;'
          f' press any key to continue, if the manual test is passed.')

    # TEST ScatterPlot double line with legend, with forced_y_limits
    SinglePlot(plot=ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                           [1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4],
                                           [3, 3, 3, 4, 5]],
                                   name=['my_plot_line_1',
                                         'my_plot_line_2'],
                                   forced_y_limits=[-10,20])).return_html_ScatterPlot(show_fig=True)
    input(f'You should see a simple plot on screen with a legend on the right side and forced y limits to -10 and 20;'
          f' press any key to continue, if the manual test is passed.')

    # TEST ScatterPlot double line with legend, with v_rects
    SinglePlot(plot=ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                           [1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4],
                                           [3, 3, 3, 4, 5]],
                                   name=['my_plot_line_1',
                                         'my_plot_line_2'],
                                   v_rects=[{'x0': 3,
                                             'x1': 4,
                                             'fillcolor': 'green',
                                             'opacity': 0.2},
                                            {'x0': 4,
                                             'x1': 5,
                                             'fillcolor': 'red',
                                             'opacity': 0.8}])).return_html_ScatterPlot(show_fig=True)
    input(f'You should see a simple plot on screen with a legend on the right side and some vertical rectangles;'
          f' press any key to continue, if the manual test is passed.')

    # TEST ScatterPlot double line with legend, with h_rects
    SinglePlot(plot=ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                           [1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4],
                                           [3, 3, 3, 4, 5]],
                                   name=['my_plot_line_1',
                                         'my_plot_line_2'],
                                   h_rects=[{'y0': 3,
                                             'y1': 4,
                                             'fillcolor': 'green',
                                             'opacity': 0.2},
                                            {'y0': 4,
                                             'y1': 5,
                                             'fillcolor': 'red',
                                             'opacity': 0.8}])).return_html_ScatterPlot(show_fig=True)
    input(f'You should see a simple plot on screen with a legend on the right side and some horizontal rectangles;'
          f' press any key to continue, if the manual test is passed.')

    # TEST ScatterPlot double line with legend
    SinglePlot(plot=ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                            datetime.now()-timedelta(minutes=9),
                                            datetime.now()-timedelta(minutes=8),
                                            datetime.now()-timedelta(minutes=7)],
                                           [datetime.now() - timedelta(minutes=10),
                                            datetime.now() - timedelta(minutes=9),
                                            datetime.now() - timedelta(minutes=8),
                                            datetime.now() - timedelta(minutes=7)]],
                                   y_axis=[[2, 2, 2, 3, 4],
                                           [3, 3, 3, 4, 5]],
                                   name=['my_plot_line_1',
                                         'my_plot_line_2'])).return_html_ScatterPlot(show_fig=True)
    input(f'You should see a simple plot on screen with a legend on the right side;'
          f' press any key to continue, if the manual test is passed.')

    # TEST ScatterPlot double line with legend and forced shown until the current datetime
    SinglePlot(plot=ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                            datetime.now()-timedelta(minutes=9),
                                            datetime.now()-timedelta(minutes=8),
                                            datetime.now()-timedelta(minutes=7)],
                                           [datetime.now() - timedelta(minutes=10),
                                            datetime.now() - timedelta(minutes=9),
                                            datetime.now() - timedelta(minutes=8),
                                            datetime.now() - timedelta(minutes=7)]],
                                   y_axis=[[2, 2, 2, 3, 4],
                                           [3, 3, 3, 4, 5]],
                                   name=['my_plot_line_1',
                                         'my_plot_line_2'],
                                   force_show_until_current_datetime=True)).return_html_ScatterPlot(show_fig=True)
    input(f'You should see a simple plot on screen with a legend on the right side and force shown until the current datetime;'
          f' press any key to continue, if the manual test is passed.')

    # TEST ScatterPlot double line with legend and forced shown until the current datetime with a greyed-out portion
    SinglePlot(plot=ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                            datetime.now()-timedelta(minutes=9),
                                            datetime.now()-timedelta(minutes=8),
                                            datetime.now()-timedelta(minutes=7)],
                                           [datetime.now() - timedelta(minutes=10),
                                            datetime.now() - timedelta(minutes=9),
                                            datetime.now() - timedelta(minutes=8),
                                            datetime.now() - timedelta(minutes=7)]],
                                   y_axis=[[2, 2, 2, 3, 4],
                                           [3, 3, 3, 4, 5]],
                                   name=['my_plot_line_1',
                                         'my_plot_line_2'],
                                   force_show_until_current_datetime=True,
                                   grey_out_missing_data_until_current_datetime=True)).return_html_ScatterPlot(show_fig=True)
    input(f'You should see a simple plot on screen with a legend on the right side and force shown until the current datetime with a greyed-out portion;'
          f' press any key to continue, if the manual test is passed.')

    print('All tests are PASSED !')