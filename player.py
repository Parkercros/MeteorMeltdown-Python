import sqlite3

# create a connection to the database
conn = sqlite3.connect('my_database.db')

# create a cursor object to execute SQL queries
cursor = conn.cursor()

# create the Player table
cursor.execute('''
    CREATE TABLE Player (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        score INTEGER,
        level INTEGER
    )
''')
# commit the changes and close the connection
conn.commit()
conn.close()
