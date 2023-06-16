from typing import AnyStr, List
from os import path,\
    walk
from logging import getLogger

def extract_filenames_from_filepath(folderpath: AnyStr,
                                    filter_ends_with: List[AnyStr] = None) -> List:
    _log = getLogger()
    filepaths = []

    _log.info(f'Analysing {folderpath} ... with the following filters: {filter_ends_with}')
    if path.isdir(folderpath):
        for first_path, subdirs, files in walk(folderpath):
            for name in files:
                if (not filter_ends_with) or\
                        (filter_ends_with and any([name.endswith(_) for _ in filter_ends_with])):
                    filepaths.append(path.join(first_path, name))
        _log.info(f'Gathered {len(filepaths)} TOTAL recordings from {folderpath}')

    return filepaths

if __name__ == '__main__':
    from ag95 import configure_logger
    from pprint import pprint

    configure_logger()

    pprint((extract_filenames_from_filepath(folderpath='.')))
    print('No automatic tests implemented so far; Please check the expected behavior manually.')