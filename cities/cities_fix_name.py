#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up.

In the previous quiz you recognized that the "name" value can be an array (or
list in Python terms). It would make it easier to process and query the data
later if all values for the name are in a Python list, instead of being
just a string separated with special characters, like now.

Finish the function fix_name(). It will recieve a string as an input, and it
will return a list of all the names. If there is only one name, the list will
have only one item in it; if the name is "NULL", the list should be empty.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import pprint

CITIES = 'cities/cities.csv'


def fix_name(name):
    names = []
    if not name:
        return None
    
    if name.startswith('{') and name.endswith('}'):
        name = name[1:-1]
        names = name.split('|')
        return names
        
    if name == 'NULL':
        return names
        
    else :
        names.append(name)
        return names


def process_file(filename):
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        #skipping the extra metadata
        for i in range(3):
            next(reader)
        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "name" in line:
                line["name"] = fix_name(line["name"])
            data.append(line)
    return data


def test():
    data = process_file(CITIES)

    print("Printing 20 results:")
    for n in range(20):
        pass
        # print(n)
        # pprint.pprint(data[n]["name"])

    assert data[14]["name"] == ['Negtemiut', 'Nightmute']
    print("['Negtemiut', 'Nightmute']:",data[14]["name"])
    assert data[9]["name"] == ['Pell City Alabama']
    print("['Pell City Alabama']:",data[9]["name"])
    assert data[3]["name"] == ['Kumhari']
    print("['Kumhari']:",data[3]["name"])

if __name__ == "__main__":
    test()