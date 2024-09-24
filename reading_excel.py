#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format

"""

import xlrd
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    coast_values = sheet.col_values(1, 1, sheet.nrows)
    times = sheet.col_values(0, 1, sheet.nrows)

    min_index = max_index = 0
    total_coast = 0

    for i, value in enumerate(coast_values[1:], 1):
        total_coast += value
        if value < coast_values[min_index]:
            min_index = i
        elif value > coast_values[max_index]:
            max_index = i

    data = {
        'maxtime': xlrd.xldate_as_tuple(times[max_index], 0),
        'maxvalue': coast_values[max_index],
        'mintime': xlrd.xldate_as_tuple(times[min_index], 0),
        'minvalue': coast_values[min_index],
        'avgcoast': total_coast / len(coast_values)
    }

    return data


def test():
    open_zip(datafile)
    data = parse_file(datafile)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)


test()