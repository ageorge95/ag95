from django.conf import settings
from django import setup
from django import template

settings.configure(TEMPLATES=[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': False, # we have no apps
    },
])
setup()

if __name__ == '__main__':

    with open('DataTableFull_template.html', 'r') as html_template:
        t = template.Template(html_template.read())

    c = template.Context({
        'report_title':'My WebPage Title',
        'tables':[{'table_id': 'ID_0',
                   'table_title': 'My Table 0',
                   'headers': ['header_1', 'header_2', 'header_3'],
                   'restrict_width_columns': str([0,1]),
                   'order': {'columnID': 1,
                             'direction': 'asc'},
                   'pageLength': 1,
                   'rows': [[{'text_color': 'black', 'text': 'text_1'},
                             {'text_color': 'red', 'text': 'text_2'},
                             {'text_color': 'orange', 'text': 'text_3'}],
                            [{'text_color': 'black', 'text': 'text_4'},
                             {'text_color': 'red', 'text': 'text_5'},
                             {'text_color': 'orange', 'text': 'text_6'}],
                            [{'text_color': 'black', 'text': 'text_7'},
                             {'text_color': 'red', 'text': 'text_8'},
                             {'text_color': 'orange', 'text': 'text_9'}]]},
                  {'table_id': 'ID_1',
                   'table_title': 'My Table 1',
                   'headers': ['header_1', 'header_2', 'header_3'],
                   'restrict_width_columns': str([0]),
                   'order': {'columnID': 2,
                             'direction': 'desc'},
                   'pageLength': 10,
                   'rows': [[{'text_color': 'black', 'text': 'text_10'},
                             {'text_color': 'red', 'text': 'text_11'},
                             {'text_color': 'orange', 'text': 'text_12'}],
                            [{'text_color': 'black', 'text': 'text_13'},
                             {'text_color': 'red', 'text': 'text_14'},
                             {'text_color': 'orange', 'text': 'text_15'}],
                            [{'text_color': 'black', 'text': 'text_16'},
                             {'text_color': 'red', 'text': 'text_17'},
                             {'text_color': 'orange', 'text': 'text_18'}]]},
                  {'table_id': 'ID_2',
                   'table_title': 'My Table 2',
                   'headers': ['header_1', 'header_2', 'header_3'],
                   'restrict_width_columns': str([]),
                   'order': {'columnID': 2,
                             'direction': 'desc'},
                   'pageLength': 10,
                   'rows': [[{'text_color': 'black', 'text': 'text_19'},
                             {'text_color': 'red', 'text': 'text_20'},
                             {'text_color': 'orange', 'text': 'text_21'}],
                            [{'text_color': 'black', 'text': 'text_22'},
                             {'text_color': 'red', 'text': 'text_23'},
                             {'text_color': 'orange', 'text': 'text_24'}],
                            [{'text_color': 'black', 'text': 'text_25'},
                             {'text_color': 'red', 'text': 'text_26'},
                             {'text_color': 'orange', 'text': 'text_27'}]]}
                  ]})

    with open('DataTableFull.html', 'w') as html_out:
        html_out.write(t.render(c))

    print('No automatic tests implemented so far; Please check the expected behavior manually.')

