from sys import argv, exit
import csv
from cs50 import SQL

# access SQL database
db = SQL("sqlite:///winexp.db")

# check command-line usage for correct len(argv)
if len(argv) != 2:
    print(f"Usage: python {argv[0]} <file>.cvs")
    exit(1)
    
# open .csv file for reading
with open(argv[1], "r") as characters:
    
    # create a reader
    reader = csv.DictReader(characters)
    
    for row in reader:   
        
        # insert each row in the database
        db.execute("INSERT INTO vintages(country, region, vintage, wsscore, rpscore, wescore, score, status) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", 
                    row["country"], row["region"], row["vintage"], row["wsscore"], row["rpscore"], row["wescore"], row["score"], row["status"])
    