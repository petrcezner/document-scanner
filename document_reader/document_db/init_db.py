import sqlite3
import sys

sys.path.insert(0, "/app/document_db")

connection = sqlite3.connect('database.db')

with open(r"document_reader/document_db/schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO warehouse (id)"
            "VALUES (?)",
            (0,))

cur.execute("INSERT INTO box (id, warehouse_id)"
            "VALUES (?, ?)",
            (0, 0))

connection.commit()
connection.close()
