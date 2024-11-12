#!/usr/bin/env python
"""
Your task is to write a query that will return all cities
that are founded in 19st century.

convert founding date from string to date
use range query to find cities founded in 19th century

"""

from datetime import datetime
from pymongo import MongoClient

def convert_founding_date_to_date():
    for city in db.cities.find({"foundingDate": {"$type": "string", "$ne" : "NULL"}}):
        date_str = city['foundingDate']
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            db.cities.update_one(
                {"_id": city["_id"]},
                {"$set": {"foundingDate": date_obj}}
            )
        except ValueError:
            print(f"Invalid date format: {date_str}")

    
def range_query():
    # Modify the below line with your query.
    # You can use datetime(year, month, day) to specify date in the query
    # founding date in 19C
    query = {"foundingDate" : { "$gte" : datetime(1800, 1, 1), "$lt" : datetime(1900, 1, 1) }}  
    return query

# Do not edit code below this line in the online code editor.
# Code here is for local use on your own computer.
def get_db():
    client = MongoClient('localhost:27017')
    db = client.testDB
    return db

if __name__ == "__main__":
    # For local use
    db = get_db()
    convert_founding_date_to_date()
    query = range_query()
    cities = db.cities.find(query)
    for city in cities:
        print(city['name'], city['foundingDate'])
    

    