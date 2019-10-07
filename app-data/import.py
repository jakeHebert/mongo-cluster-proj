from pymongo import MongoClient
import sys
import csv

"""
    This script allows a user to import a .csv file into a mongo DB.
    It takes a cli parameter for which file to use. e.q -> python test.py "test.csv"
    It uses the first row as a header row, to populate the keys.
    It skips the second row(this project's csv file has an empty row).
"""
FILEPATH = sys.argv[1]     # FILEPATH is cli param
server_ip = "localhost"    # Mongo server ip address
DB_NAME = "default"
COL_NAME = "coll"

# DB connectivity
client = MongoClient(server_ip, 27019)        # 27019 points to mongos1
db = client[DB_NAME]
myCol = db[COL_NAME]

# Enable sharding on the database and the collection.
client.admin.command('enableSharding', DB_NAME)
client.admin.command('shardCollection', DB_NAME + "." + COL_NAME, key={"_id": 'hashed'})

# Arrays used to hold the header and each row of key-value pairs(cell)
header = []
rows = []

with open(FILEPATH, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter="\t")
    index = 0   # index is used to keep track of which line reader is on. Needed to skip line 1 and to grab columns.
    for line in reader:
        line = str(line).split(",")
        if index == 0:  # If index is 0, create the header, or the array of columns in the .csv file.
            header = line
            index += 1
            continue
        elif index == 1:    # If line 1, skip. Bunch of copyright stuff...
            index += 1
            continue

        # For each column, add all key-values to the row, then add the row the array of rows.
        row = {}    # Dict to hold key-value pairs for the row.
        for i in range(len(header)):
            row[header[i]] = line[i]
        rows.append(row)
        index += 1

# For each row, insert it into the database collection.
for i in rows:
    myCol.insert_one(i)

print(myCol.count_documents({}))
print("Import data complete.")
