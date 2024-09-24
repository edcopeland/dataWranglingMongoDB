# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ercot_hourly_load_data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    
    for col_index in range(1, sheet.ncols - 1):
        region_dict = {}
        col_name = sheet.cell_value(0, col_index)
        region_dict['Station'] = col_name
        region_dict['Max Load'] = sheet.cell_value(1, col_index)
        exceltime = sheet.cell_value(1, 0)
        time_list = list(xlrd.xldate_as_tuple(exceltime, 0))
        time_col_names = ['Year', 'Month', 'Day', 'Hour' ]
        for i, name in enumerate(time_col_names):
            region_dict[name] = time_list[i]

        for row_index in range(1, sheet.nrows):
            cell_value = sheet.cell_value(row_index, col_index)
            if cell_value > region_dict['Max Load'] :
                region_dict['Max Load'] = cell_value
                exceltime = sheet.cell_value(row_index, 0)
                time_list = list(xlrd.xldate_as_tuple(exceltime, 0))
                time_col_names = ['Year', 'Month', 'Day', 'Hour' ]
                for i, name in enumerate(time_col_names):
                    region_dict[name] = time_list[i]
        data.append(region_dict)
    return data

def save_file(data, filename):
    fieldnames = ['Station','Year','Month','Day','Hour','Max Load']
    with open(filename, 'w') as csvfile:
        data_writer = csv.DictWriter(csvfile, fieldnames ,delimiter='|')
        data_writer.writeheader()
        for entry in data:
            data_writer.writerow(entry)

   
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()
