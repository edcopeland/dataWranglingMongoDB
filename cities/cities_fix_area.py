import codecs
import csv
import json
import pprint

CITIES = 'cities/cities.csv'


def fix_area(area):
    # Check if area is None or an empty string
    if not area:
        return None

    # Remove curly braces if present
    if area.startswith("{") and area.endswith("}"):
        area = area[1:-1]

    # Split by '|' to get multiple values if present
    values = area.split("|")

    # Convert to floats and find the most precise value
    precise_value = None
    max_precision = 0

    for value in values:
        try:
            # Try converting each value to float
            float_value = float(value)

            # Determine decimal precision by counting digits after the decimal
            precision = len(value.split(".")[1]) if "." in value else 0

            # Choose the value with the highest precision
            if precision > max_precision:
                precise_value = float_value
                max_precision = precision

        except ValueError:
            # If conversion fails, skip this value
            continue

    return precise_value


def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        # Skipping the extra metadata
        for i in range(3):
            next(reader)

        # Processing file
        for line in reader:
            # Calling the function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print("Printing three example results:")
    for n in range(5, 8):
        pprint.pprint(data[n]["areaLand"])

    print('3 = ',data[3]["areaLand"])  
    assert data[3]["areaLand"] is None      
    print('8 = ',data[8]["areaLand"])  
    assert data[8]["areaLand"] == 55166700.0
    print('20 = ',data[20]["areaLand"])  
    assert data[20]["areaLand"] == 14581600.0
    print('33 = ',data[33]["areaLand"])  
    assert data[33]["areaLand"] == 20564500.0    


if __name__ == "__main__":
    test()