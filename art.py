import sqlite3
import datetime


def create_image_dates_table():
    conn = sqlite3.connect("created-spaceships.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS image_dates
                    (id INTEGER PRIMARY KEY,
                    filepath TEXT NOT NULL,
                    date_saved DATE NOT NULL);''')
    conn.commit()
    conn.close()

create_image_dates_table()

def insert_image_date(date_saved, filepath):
    conn = sqlite3.connect('created-spaceships.db')
    conn.execute('INSERT INTO image_dates (filepath, date_saved) VALUES (?, ?)', (filepath, date_saved))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    filepath = 'example.jpg'
    date_saved = datetime.date.today()
    insert_image_date(date_saved, filepath)



