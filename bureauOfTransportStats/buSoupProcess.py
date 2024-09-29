#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Let's assume that you combined the code from the previous 2 exercises with code
from the lesson on how to build requests, and downloaded all the data locally.
The files are in a directory "data", named after the carrier and airport:
"{}-{}.html".format(carrier, airport), for example "FL-ATL.html".

The table with flight info has a table class="dataTDRight". Your task is to
use 'process_file()' to extract the flight data from that table as a list of
dictionaries, each dictionary containing relevant data from the file and table
row. This is an example of the data structure you should return:

data = [{"courier": "FL",
         "airport": "ATL",
         "year": 2012,
         "month": 12,
         "flights": {"domestic": 100,
                     "international": 100}
        },
         {"courier": "..."}
]

Note - year, month, and the flight data should be integers.
You should skip the rows that contain the TOTAL data for a year.


The 'data/FL-ATL.html' file is only a part of the full data,
covering data through 2003. The test() code will be run on the full table, but
the given file should provide an example of what you will get.
"""
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os
html = "FL-ATL.html"

datadir = "bureauOfTransportStats/data"
html_file = "bureauOfTransportStats/data/FL-ATL.html"


# def open_zip(datadir):
#     with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
#         myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files



def process_file(file):
    """
    This function extracts data from the file given as the function argument in
    a list of dictionaries. This is example of the data structure you should
    return:

    data = [{"courier": "FL",
             "airport": "ATL",
             "year": 2012,
             "month": 12,
             "flights": {"domestic": 100,
                         "international": 100}
            },
            {"courier": "..."}
    ]


    Note - year, month, and the flight data should be integers.
    You should skip the rows that contain the TOTAL data for a year.
    """
    data = []
    info = {}
    info["courier"], info["airport"] = file[:6].split("-")
    
    # Note: create a new dictionary for each entry in the output data list.
    # If you use the info dictionary defined here each element in the list 
    # will be a reference to the same info dictionary.
    
    with open("{}/{}".format(datadir, file), "r") as html:
        soup = BeautifulSoup(html,"html.parser")
        table_data = soup.find_all("tr", {"class": "dataTDRight"})

        for row in table_data:  
            td = row.find_all('td')
            total_column = False

            for i, data_point in enumerate(td):
                if data_point.text == 'TOTAL':
                    total_column = True
                    break        
                if i == 0:
                    year = int(data_point.text)
                elif i == 1:
                    month = int(data_point.text)
                elif i == 2:
                     domestic = int(data_point.text.replace(',',''))
                                         
                elif i == 3:
                    international = int(data_point.text.replace(',', ''))
                    
                    
            if not total_column:
                dct = {
                    "courier": info["courier"],
                    "airport": info["airport"],
                    "year": year,
                    "month": month,
                    "flights": {
                        "domestic": domestic,
                        "international": international
                    }
                }
                # print(dct)
                data.append(dct)
               
              
    print(data)
    return data


def test():
    print("Running a simple test...")
    # open_zip(datadir)
    files = process_all(datadir)
    data = []
    # Test will loop over three data files.
    # for f in files:
    data += process_file('FL-ATL.html')
        
    assert len(data) == 15  # Total number of rows
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    assert data[0]["courier"] == 'FL'
    assert data[0]["month"] == 10
    assert data[-1]["airport"] == "ATL"
    assert data[-1]["flights"] == {'international': 97094, 'domestic': 798879}
    
    print("... success!")

if __name__ == "__main__":
    test()