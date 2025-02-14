from setuptools import setup, find_packages

VERSION = '0.3.55'
DESCRIPTION = 'ag95 scripts collection'
LONG_DESCRIPTION = 'Various scripts that can be used in all kinds of python projects.'

setup(
    name="ag95",
    version=VERSION,
    author="ageorge95",
    author_email="arteni.george.daniel@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    extras_require={
        "DecimalScripts": [],
        "LoggingScripts": [
            'concurrent_log_handler',
        ],
        "Threading": [],
        "General": [],
        "TimeRelated": [],
        "SqliteDatabase": [
            'concurrent_log_handler'
        ],
        "GenericDatabase": [
            'concurrent_log_handler'
        ],
        "DuckDbDatabase": [
            'concurrent_log_handler',
            'duckdb'
        ],
        "PlotlyRelated": [
            'plotly'
        ],
        "TemplatesHtml": [],
        "DataManipulation": [],
        "TradingRelated": [],
        "WindowsCredentials": [
            'keyring'
        ],
        "IoT": [
            'requests'
        ],
        "IO": []
    },
    keywords=['python', 'ag95']
)