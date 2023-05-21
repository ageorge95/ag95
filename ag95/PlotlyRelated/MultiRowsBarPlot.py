from datetime import datetime,\
    timedelta
from ag95 import BarPlotDef,\
    MultiRowPlot

if __name__ == '__main__':
    print('No automatic tests implemented so far; Please check the expected behavior manually.')

    # TEST MultiRowsBarPlot [single_line]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1,2,3,4,5]],
                                   y_axis=[[2,2,2,3,4]])]).return_html_BarPlot(show_fig=True)
    input(f'You should see MultiRowsBarPlot [single_line];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot [single_line, single_line]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1,2,3,4,5]],
                                   y_axis=[[2,2,2,3,4]]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4]])]).return_html_BarPlot(show_fig=True)
    input(f'You should see MultiRowsBarPlot [single_line, single_line];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot [single_line, single_line, single_line]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4]]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4]]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4]])]).return_html_BarPlot(show_fig=True)
    input(f'You should see MultiRowsBarPlot [single_line, single_line, single_line];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot [single_line, double_line, triple_line]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]])]).return_html_BarPlot(show_fig=True)
    input(f'You should see MultiRowsBarPlot [single_line, double_line, triple_line];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot [single_line & names, double_line & names, triple_line & names]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line']),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line']),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'])]).return_html_BarPlot(show_fig=True)
    input(f'You should see MultiRowsBarPlot [single_line & names, double_line & names, triple_line & names];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot [single_line & names & hrects, double_line & names, triple_line & names & hrects]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line'],
                                       h_rects=[{'y0': 3,
                                                 'y1': 4,
                                                 'fillcolor': 'green',
                                                 'opacity': 0.2},
                                                {'y0': 4,
                                                 'y1': 5,
                                                 'fillcolor': 'red',
                                                 'opacity': 0.8}]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line']),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'],
                                       h_rects=[{'y0': 3,
                                                 'y1': 4,
                                                 'fillcolor': 'green',
                                                 'opacity': 0.2},
                                                {'y0': 4,
                                                 'y1': 5,
                                                 'fillcolor': 'red',
                                                 'opacity': 0.8}])]).return_html_BarPlot(show_fig=True)
    input(f'You should see MultiRowsBarPlot [single_line & names & hrects, double_line & names, triple_line & names & hrects];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot [single_line & names & vrects, double_line & names, triple_line & names & vrects]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line'],
                                       v_rects=[{'x0': 3,
                                                 'x1': 4,
                                                 'fillcolor': 'green',
                                                 'opacity': 0.2},
                                                {'x0': 4,
                                                 'x1': 5,
                                                 'fillcolor': 'red',
                                                 'opacity': 0.8}]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line']),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'],
                                       v_rects=[{'x0': 3,
                                                 'x1': 4,
                                                 'fillcolor': 'green',
                                                 'opacity': 0.2},
                                                {'x0': 4,
                                                 'x1': 5,
                                                 'fillcolor': 'red',
                                                 'opacity': 0.8}])]).return_html_BarPlot(show_fig=True)
    input(f'You should see MultiRowsBarPlot [single_line & names & vrects, double_line & names, triple_line & names & vrects];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot [single_line & names, double_line & names & forced_y_limits, triple_line & names & forced_y_limits]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line']),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line'],
                                       forced_y_limits=[-1,10]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'],
                                       forced_y_limits=[-1,10])]).return_html_BarPlot(show_fig=True)
    input(f'You should seeMultiRowsBarPlot [single_line & names, double_line & names & forced_y_limits, triple_line & names & forced_y_limits];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot [single_line & names, double_line & names, triple_line & names]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line']),
                        BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line']),
                        BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'])]).return_html_BarPlot(show_fig=True)
    input(f'You should see MultiRowsBarPlot [single_line & names, double_line & names, triple_line & names];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot
    # [single_line & names & force_show_until_current_datetime,
    # double_line & names & force_show_until_current_datetime,
    # triple_line & names]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line'],
                                       force_show_until_current_datetime=True),
                        BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line'],
                                       force_show_until_current_datetime=True),
                        BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'])]).return_html_BarPlot(show_fig=True)
    input(f'You should see MultiRowsBarPlot'
          f' [single_line & names & force_show_until_current_datetime,'
          f' double_line & names & force_show_until_current_datetime,'
          f' triple_line & names];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot
    # [single_line & names & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime,
    # double_line & names & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime,
    # triple_line & names]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line'],
                                       force_show_until_current_datetime=True,
                                       grey_out_missing_data_until_current_datetime=True),
                        BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line'],
                                       force_show_until_current_datetime=True,
                                       grey_out_missing_data_until_current_datetime=True),
                        BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'])]).return_html_BarPlot(show_fig=True)
    input(f'You should see MultiRowsBarPlot [single_line & names & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime,'
          f' double_line & names & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime,'
          f' triple_line & names];'
          f' press any key to continue, if the manual test is passed.')

    # TEST MultiRowsBarPlot [single_line & names & forced_width, double_line & names & forced_width, triple_line & names]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line'],
                                       forced_width=500),
                        BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line'],
                                       forced_width=500),
                        BarPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)],
                                               [datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'])]).return_html_BarPlot(show_fig=True)
    input(f'You should see [single_line & names & forced_width, double_line & names & forced_width, triple_line & names];'
          f' press any key to continue, if the manual test is passed.')

    print('All tests are PASSED !')