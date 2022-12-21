'''
Author: Sam Tracey
Module: Data Representation.
Description: This module contains the configuration for the MySQL database connection and FRED API.

'''

# MySQL database connection details

db = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'datarepresentation'
}

# Fred API connection details

fred = {
    'url': 'https://api.stlouisfed.org/fred/series/observations?series_id=',
    'url_end': '&api_key=735b868f6c19b3ea684013624f617bdc&file_type=json',
    'unemployment': 'SCUR',
    'MFGEMP': 'SCMFG',
    'Quits': 'JTS00SOQUL',
    'Openings': 'JTS00SOJOL'
}

