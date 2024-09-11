# Run this file to (re)initialise the SQLite DB

import os 
import sys 
import sqlite3

scriptDir = os.path.dirname(os.path.abspath(sys.argv[0])) 
sqlitePath = os.path.join(scriptDir, "data.db")
schemaPath = os.path.join(scriptDir, "schema.sql")

connection = sqlite3.connect(sqlitePath)

with open(schemaPath) as f:
    connection.executescript(f.read())

