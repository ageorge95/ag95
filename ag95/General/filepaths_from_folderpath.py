from typing import AnyStr, List
from os import path,\
    walk
from logging import getLogger
from warnings import warn

def extract_filenames_from_filepath(folderpath: AnyStr,
                                    filter_ends_with: List[AnyStr] = None) -> List:
    warn(
        "extract_filenames_from_filepath is deprecated and is"
        " replaced by extract_filenames_from_folderpath.",
        DeprecationWarning,
        stacklevel=2
    )
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

def extract_filenames_from_folderpath(folderpath: AnyStr,
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
    from pprint import pprint

    pprint((extract_filenames_from_folderpath(folderpath='.')))
    print('No automatic tests implemented so far; Please check the expected behavior manually.')