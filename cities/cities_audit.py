import codecs
import csv
import json
import pprint
from pymongo import MongoClient



"""
audit the data in cities.csv file and remove the fields that have all null values

take the cities.csv file and create cities_audited.json file 

populate the mongodb database with the data from cities_audited.json file

methods :
    audit_file(filename) - remove the fields that have all null values
    create_json_file(data) - save the filtered data to a json file
    empty_mongo_db() - empty the mongodb database to avoid duplicates when running the script multiple times
    populate_mongo_db(data) - populate the mongodb database with the data from cities_audited.json file
    display_mongo_db_content() - display the content of the mongodb database to verify the data was populated correctly
 

"""

CITIES = 'cities/cities.csv'  
json_file_path = 'cities/cities.json'

client = MongoClient("mongodb://localhost:27017")
db = client.testDB



    
def audit_file(filename):
    
    """
    audit the data in cities.csv file and remove the fields that have all null values
    Args:
        filename (str): The name of the file to audit.

    Returns:
        dict: A dictionary containing the filtered data.

    """

    data = {"cities":[]}
    audit_field = "areaCode"
    unique_keys = set()
    null_key_counts = {}
    null_filtered_fields = set()
    columns = 0

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        # Skipping the extra metadata
        for _ in range(3):
            next(reader)

        # Processing file
        for line in reader:
            columns += 1
            data['cities'].append(line)
            
            unique_keys.update(line.keys())
           
            for key, value in line.items():
                if key not in null_key_counts:
                    # Initialize counts for this key
                    null_key_counts[key] = {"null": 0, "non-null": 0}

                # Count null and non-null values
                if value == 'NULL' or value is None or value == '':
                    null_key_counts[key]["null"] += 1
                else:
                    null_key_counts[key]["non-null"] += 1
                    
        
        for field in null_key_counts:
            if null_key_counts[field]["null"] == 39:
                null_filtered_fields.add(field)
            
       
        
        # print('Number of fields in first column : ') 
        # print(len(data['cities'][0].keys()))
        # print('Number of unique fields : ')
        # print(len(unique_keys))
        # print('Number of Columns : ')
        # print(columns)
        # print('What are the field names in the csv file, and how many of the cities hold null values for those fields? : ')
        # pprint.pprint(null_key_counts)
        # print('What fields have all null values? : ')
        # pprint.pprint(len(null_filtered_fields))
        
        # removing null fields from the data
        for line in data['cities']:
                for field in null_filtered_fields:
                    if field in line:
                        del line[field]
            
        # print('number of fields after removing null fields : ')
        # print(len(data['cities'][0].keys()))
   

    return data



def create_json_file(data):
    """
    save the filtered data to a json file
    Args:
        data (dict): The filtered data to be saved.

    Returns:
        None
    
    
    
    """
     # save the filtered data to a json file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data['cities'], json_file, indent=4, ensure_ascii=False)
            
            
          
        
def populate_mongo_db(data):
    """
    populate the mongodb database with the data from cities_audited.json file
    Args:
        data (dict): The filtered data to be inserted into the database.

    Returns:
        None
    
    Prints the number of fields in the collection and the inserted document's ID
    
    
    
    """
    cities_collection = db['cities']
 
    result = cities_collection.insert_many(data['cities'])
    
    # print the number of fields in the collection
    num_fields = len(cities_collection.find_one().keys())
    print(f'number of fields inserted into cities collection :{num_fields}')
    # # Print the inserted document's ID
    # print(f"Inserted document ID: {result.inserted_ids}")



def empty_mongo_db():
    """
    empty the mongodb database to avoid duplicates when running the script multiple times
    Args:
        None
    
    """
    # Get a list of all collections
    collections = db.list_collection_names()

    # Drop each collection
    for collection in collections:
        db[collection].drop()
        
    print('database has been cleared')
        
        
        
        
def display_mongo_db_content(number):
    """
    display the content of the mongodb database to verify the data was populated correctly
    Args:
        number (int): The number of documents to display.

    Returns:
        None
    
    Prints the collection name, the number of documents in the collection, 
    and the documents.
    
    """
    collections = db.list_collection_names()
    for collection_name in collections:
        print(f"\nCollection: {collection_name}")
        print("-" * 50)
        
        # Get the collection
        if len(collections) > 0:
            collection = db[collection_name]
        
        
            # find all documents in the collection
            documents = collection.find()
            
            # print each document
            # for x,doc in enumerate(documents):
            #     if x < number:
            #         print(f"\nDocument {x + 1}:")
            #         print("-" * 50)
            #         pprint.pprint(doc)
                    
            print(len(list(documents)))




if __name__ == "__main__":
    """
    remove the comments to run the methods as required
    
    """
    # audit the city data - removing consistently empty fields
    # data = audit_file(CITIES)
    
    # create_json_file(data)
    
    # empty_mongo_db()
    
    # populate_mongo_db(data)
    
    display_mongo_db_content(1)
    
    
    
    
    
   


