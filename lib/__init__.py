

import sqlite3

# Generate sqlite3.Connection object and sqlite3.Cursor object
CONN = sqlite3.connect(":memory:")
CURSOR = CONN.cursor()
