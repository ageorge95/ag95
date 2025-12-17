from datetime import datetime,\
    timedelta
from ag95 import HistogramPlotDef,\
    SinglePlot

if __name__ == '__main__':
    print('No automatic tests implemented so far; Please check the expected behavior manually.')

    # TEST SingleHistogramPlot [single_line]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[1,2,3,4,5]],
                                     y_axis=[[2,2,2,3,4]])).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [single_line];'
          f' press any key to continue, if the manual test is passed.')

    # TEST SingleHistogramPlot [single_line & no name]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                     y_axis=[[2, 2, 2, 3, 4]],
                                     name=['my_plot_line_1'])).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [single_line & no name];'
          f' press any key to continue, if the manual test is passed.')

    # TEST SingleHistogramPlot [double_line & name]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                             [1, 2, 3, 4, 5]],
                                     y_axis=[[2, 2, 2, 3, 4],
                                             [3, 3, 3, 4, 5]],
                                     name=['my_plot_line_1',
                                           'my_plot_line_2'])).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [double_line & name];'
          f' press any key to continue, if the manual test is passed.')

    # TEST SingleHistogramPlot [double_line & name & forced red color]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                             [1, 2, 3, 4, 5]],
                                     y_axis=[[2, 2, 2, 3, 4],
                                             [3, 3, 3, 4, 5]],
                                     colors=['red', 'red'],
                                     name=['my_plot_line_1',
                                           'my_plot_line_2'])).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [double_line & name & forced red color];'
          f' press any key to continue, if the manual test is passed.')

    # TEST SingleHistogramPlot [double_line & name & forced_y_limits]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                             [1, 2, 3, 4, 5]],
                                     y_axis=[[2, 2, 2, 3, 4],
                                             [3, 3, 3, 4, 5]],
                                     name=['my_plot_line_1',
                                           'my_plot_line_2'],
                                     forced_y_limits=[-10,20])).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [double_line & name & forced_y_limits];'
          f' press any key to continue, if the manual test is passed.')

    # TEST SingleHistogramPlot [double_line & name & vrects]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[1, 2, 3, 4, 5],
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
                                               'opacity': 0.8}])).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [double_line & name & vrects];'
          f' press any key to continue, if the manual test is passed.')

    # TEST SingleHistogramPlot [double_line & name & hrects]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[1, 2, 3, 4, 5],
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
                                               'opacity': 0.8}])).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [double_line & name & hrects];'
          f' press any key to continue, if the manual test is passed.')

    # TEST SingleHistogramPlot [double_line & name]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
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
                                           'my_plot_line_2'])).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [double_line & name];'
          f' press any key to continue, if the manual test is passed.')

    # TEST SingleHistogramPlot [double_line & name & force_show_until_current_datetime]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
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
                                     force_show_until_current_datetime=True)).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [double_line & name & force_show_until_current_datetime];'
          f' press any key to continue, if the manual test is passed.')

    # TEST SingleHistogramPlot [double_line & name & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
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
                                     grey_out_missing_data_until_current_datetime=True)).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [double_line & name & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime];'
          f' press any key to continue, if the manual test is passed.')

    # TEST SingleHistogramPlot [double_line & name & x_annotations]
    SinglePlot(plot=HistogramPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                             [1, 2, 3, 4, 5]],
                                     y_axis=[[2, 2, 2, 3, 4],
                                             [3, 3, 3, 4, 5]],
                                     name=['my_plot_line_1',
                                           'my_plot_line_2'],
                                     x_annotations=[[3.5, "Threshold X"],
                                                    [4.5, "Threshold Y"]])).return_html_HistogramPlot(show_fig=True)
    input(f'You should see SingleHistogramPlot [double_line & name & x_annotations];'
          f' NOTE: Text should be at the TOP of the plot.'
          f' press any key to continue, if the manual test is passed.')

    print('All tests are PASSED !')