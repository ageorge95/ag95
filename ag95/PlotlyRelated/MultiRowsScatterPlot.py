from datetime import (datetime,
                      timedelta)
from ag95 import (ScatterPlotDef,
                  MultiRowPlot)

def suite_of_tests(use_hoversubplots):

    # TEST MultiRowsScatterPlot
    # [single_line]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1,2,3,4,5]],
                                       y_axis=[[2,2,2,3,4]])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line,
    # single_line]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1,2,3,4,5]],
                                       y_axis=[[2,2,2,3,4]]),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line,'
          f'\n single_line];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line & fill,
    # single_line & fill]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       fill_method=['tonexty']),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       fill_method=['tozeroy'])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line & fill,'
          f'\n single_line & fill];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line,
    # single_line]
    # + a plot title
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]]),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]])],
                 title='My Really Loooooooooooooooooooooooooooooooooooooooooooooooooooooooong Plot Title').return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line,'
          f'\n single_line]'
          f'\n + a plot title;'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line & title,
    # single_line & title]
    # + a plot title
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       title='My Really Loooooooooooooooooooooooooooooooooooooooooooooooooooooooong SubPlot Title'),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       title='My Really Loooooooooooooooooooooooooooooooooooooooooooooooooooooooong SubPlot Title')],
                 title='My Really Loooooooooooooooooooooooooooooooooooooooooooooooooooooooong Plot Title').return_html_ScatterPlot(
        show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line & title,'
          f'\n single_line & title]'
          f'\n + a plot title;'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line,
    # single_line,
    # single_line]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]]),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]]),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line,'
          f'\n single_line,'
          f'\n single_line];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line,
    # double_line,
    # triple_line]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]]),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]]),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line,'
          f'\n double_line,'
          f'\n triple_line];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line & names,
    # double_line & names,
    # triple_line & names]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line']),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line']),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line & names,'
          f'\n double_line & names,'
          f'\n triple_line & names];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line & names & hrects,
    # double_line & names,
    # triple_line & names & hrects]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
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
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line']),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
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
                                                 'opacity': 0.8}])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line & names & hrects,'
          f'\n double_line & names,'
          f'\n triple_line & names & hrects];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line & names & vrects,
    # double_line & names,
    # triple_line & names & vrects]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
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
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line']),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
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
                                                 'opacity': 0.8}])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line & names & vrects,'
          f'\n double_line & names,'
          f'\n triple_line & names & vrects];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line & names,
    # double_line & names & forced_y_limits,
    # triple_line & names & forced_y_limits]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line']),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line'],
                                       forced_y_limits=[-1,10]),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'],
                                       forced_y_limits=[-1,10])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line & names,'
          f'\n double_line & names & forced_y_limits,'
          f'\n triple_line & names & forced_y_limits];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line & names,
    # double_line & names,
    # triple_line & names]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line']),
                        ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
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
                        ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
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
                                             'my_third_plot_third_line'])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line & names,'
          f'\n double_line & names,'
          f'\n triple_line & names];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line & names & force_show_until_current_datetime,
    # double_line & names & force_show_until_current_datetime,
    # triple_line & names]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line'],
                                       force_show_until_current_datetime=True),
                        ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
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
                        ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
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
                                             'my_third_plot_third_line'])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line & names & force_show_until_current_datetime,'
          f'\n double_line & names & force_show_until_current_datetime,'
          f'\n triple_line & names];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line & names & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime,
    # double_line & names & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime,
    # triple_line & names]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
                                                datetime.now()-timedelta(minutes=9),
                                                datetime.now()-timedelta(minutes=8),
                                                datetime.now()-timedelta(minutes=7)]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line'],
                                       force_show_until_current_datetime=True,
                                       grey_out_missing_data_until_current_datetime=True),
                        ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
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
                        ScatterPlotDef(x_axis=[[datetime.now()-timedelta(minutes=10),
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
                                             'my_third_plot_third_line'])]).return_html_ScatterPlot(show_fig=True,
                                                                                       use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line & names & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime,'
          f'\n double_line & names & force_show_until_current_datetime & grey_out_missing_data_until_current_datetime,'
          f'\n triple_line & names];'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')

    # TEST MultiRowsScatterPlot
    # [single_line & names & x_annotations,
    # double_line & names,
    # triple_line & names & x_annotations]
    MultiRowPlot(plots=[ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4]],
                                       name=['my_first_plot_first_line'],
                                       x_annotations=[[3.5, "Limit A"]]),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5]],
                                       name=['my_second_plot_first_line',
                                             'my_second_plot_second_line']),
                        ScatterPlotDef(x_axis=[[1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5],
                                               [1, 2, 3, 4, 5]],
                                       y_axis=[[2, 2, 2, 3, 4],
                                               [3, 3, 3, 4, 5],
                                               [4, 4, 4, 5, 6]],
                                       name=['my_third_plot_first_line',
                                             'my_third_plot_second_line',
                                             'my_third_plot_third_line'],
                                       x_annotations=[[4.5, "Limit B"]])]).return_html_ScatterPlot(show_fig=True,
                                                                                                   use_hoversubplots=use_hoversubplots)
    input(f'You should see MultiRowsScatterPlot'
          f'\n [single_line & names & x_annotations,'
          f'\n double_line & names,'
          f'\n triple_line & names & x_annotations];'
          f'\n NOTE: Text should be at the TOP of the subplot.'
          f'\n press any key to continue, if the manual test is passed (with use_hoversubplots set to {use_hoversubplots}).')


if __name__ == '__main__':
    print('No automatic tests implemented so far; Please check the expected behavior manually.')

    suite_of_tests(use_hoversubplots=False)
    suite_of_tests(use_hoversubplots=True)

    print('All tests are PASSED !')