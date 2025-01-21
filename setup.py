from setuptools import setup, find_packages

VERSION = '0.3.53'
DESCRIPTION = 'ag95 scripts collection'
LONG_DESCRIPTION = 'Various scripts that can be used in all kinds of python projects.'

setup(
    name="ag95",
    version=VERSION,
    author="ageorge95",
    # author_email="some_email@provider.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'concurrent_log_handler',
        'django',
        'plotly',
        'duckdb',
        'keyring',
        'requests'
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=['python', 'ag95']
)