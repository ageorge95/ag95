from shutil import copy
from os import listdir,\
    path,\
    mkdir

def export_html_templates(output_path: str):
    input_path = path.dirname(__file__)

    if not path.isdir(output_path):
        mkdir(output_path)

    for filename in listdir(input_path):
        if filename.endswith('.html'):
            copy(path.join(input_path, filename),
                 path.join(output_path, filename))

if __name__ == '__main__':
    export_html_templates(output_path=path.join(path.dirname(__file__), 'export'))

    print('No automatic tests implemented so far; Please check the expected behavior manually.')