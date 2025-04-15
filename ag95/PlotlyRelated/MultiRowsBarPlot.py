from datetime import (datetime,
                      timedelta)
from ag95 import (BarPlotDef,
                  MultiRowPlot)

def suite_of_tests(use_hoversubplots):

    # TEST MultiRowsBarPlot
    # [single_line]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1,2,3,4,5]],
                                   y_axis=[[2,2,2,3,4]])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsBarPlot'
          f'\n [single_line];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsBarPlot
    # [single_line,
    # single_line]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1,2,3,4,5]],
                                   y_axis=[[2,2,2,3,4]]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4]])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsBarPlot'
          f'\n [single_line,'
          f'\n single_line];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsBarPlot
    # [single_line,
    # single_line,
    # single_line]
    MultiRowPlot(plots=[BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4]]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4]]),
                        BarPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                   y_axis=[[2, 2, 2, 3, 4]])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsBarPlot'
          f'\n [single_line,'
          f'\n single_line,'
          f'\n single_line];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsBarPlot
    # [single_line,
    # double_line,
    # triple_line]
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
                                               [4, 4, 4, 5, 6]])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsBarPlot'
          f'\n [single_line,'
          f'\n double_line,'
          f'\n triple_line];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsBarPlot
    # [single_line & names,
    # double_line & names,
    # triple_line & names]
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
                                             'my_third_plot_third_line'])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsBarPlot'
          f'\n [single_line & names,'
          f'\n double_line & names,'
          f'\n triple_line & names];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsBarPlot
    # [single_line & names & hrects,
    # double_line & names,
    # triple_line & names & hrects]
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
                                                 'opacity': 0.8}])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsBarPlot'
          f'\n [single_line & names & hrects,'
          f'\n double_line & names,'
          f'\n triple_line & names & hrects];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsBarPlot
    # [single_line & names & vrects,
    # double_line & names,
    # triple_line & names & vrects]
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
                                                 'opacity': 0.8}])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsBarPlot'
          f'\n [single_line & names & vrects,'
          f'\n double_line & names,'
          f'\n triple_line & names & vrects];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsBarPlot
    # [single_line & names,
    # double_line & names & forced_y_limits,
    # triple_line & names & forced_y_limits]
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
                                       forced_y_limits=[-1,10])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should seeMultiRowsBarPlot'
          f'\n [single_line & names,'
          f'\n double_line & names & forced_y_limits,'
          f'\n triple_line & names & forced_y_limits];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsBarPlot
    # [single_line & names,
    # double_line & names,
    # triple_line & names]
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
                                             'my_third_plot_third_line'])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsBarPlot'
          f'\n [single_line & names,'
          f'\n double_line & names,'
          f'\n triple_line & names];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

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
                                             'my_third_plot_third_line'])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsBarPlot'
          f'\n [single_line & names & force_show_until_current_datetime,'
          f'\n double_line & names & force_show_until_current_datetime,'
          f'\n triple_line & names];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

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
                                             'my_third_plot_third_line'])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsBarPlot [single_line & names & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime,'
          f'\n double_line & names & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime,'
          f'\n triple_line & names];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsBarPlot
    # [single_line & names & forced_width,
    # double_line & names & forced_width,
    # triple_line & names]
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
                                             'my_third_plot_third_line'])]).return_html_BarPlot(show_fig=True,
                                                                               use_hoversubplots=use_hoversubplots)
    input(f'You should see'
          f'\n [single_line & names & forced_width,'
          f'\n double_line & names & forced_width,'
          f'\n triple_line & names];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

if __name__ == '__main__':
    print('No automatic tests implemented so far; Please check the expected behavior manually.')

    suite_of_tests(use_hoversubplots=False)
    suite_of_tests(use_hoversubplots=True)

    print('All tests are PASSED !')