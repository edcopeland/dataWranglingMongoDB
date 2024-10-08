"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in the range as described above,
  write that line to the output_good file
- if the value of the field is not a valid year as described above, 
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the 
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv


INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'
# regex for year
YEAR_REGEX = r'^\d{4}$' # needs to be a string!!!

def write_file(output_file, output_list,header):
    with open(output_file, "w") as f:
        writer = csv.DictWriter(f, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in output_list:
            writer.writerow(row)
    

def process_file(input_file, output_good, output_bad):
    good_list = []
    bad_list = []
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        # store reader in dictionary
        unsorted_data = list(reader)
        
   
    for line in unsorted_data:
        
       if len(line.get('URI').split('/')) > 1 and line.get('URI').split('/')[2] == 'dbpedia.org':
            production_start_year = line.get('productionStartYear', '').strip()
            production_start_year = production_start_year.split('-')[0]
            if production_start_year.isdigit():
                production_start_year = int(production_start_year)
                if production_start_year >= 1886 and production_start_year <= 2014:
                    line['productionStartYear'] = production_start_year
                    good_list.append(line)
                else:
                    bad_list.append(line)
            else:
                bad_list.append(line)
         
    write_file(OUTPUT_GOOD,good_list,header)
    write_file(OUTPUT_BAD,bad_list,header)
                 

def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()