import sqlite3
import datetime
from PIL import Image


def create_image_dates_table():
    conn = sqlite3.connect("created-spaceships.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS image_dates
                    (filepath TEXT PRIMARY KEY NOT NULL,
                    date_saved DATE NOT NULL,
                    width INTEGER NOT NULL,
                    height INTEGER NOT NULL);''')
    conn.commit()
    conn.close()

create_image_dates_table()

def insert_image_date(date_saved, filepath, width, height):
    conn = sqlite3.connect('created-spaceships.db')
    conn.execute('INSERT INTO image_dates (filepath, date_saved, width, height) VALUES (?, ?, ?, ?)',
                (filepath, date_saved, width, height))
    conn.commit()
    conn.close()

def get_image_size(filepath):
    with Image.open(filepath) as img:
        width, height = img.size
    return width, height

if __name__ == "__main__":
    setup_database()
    filepath = 'example.jpg'
    date_saved = datetime.date.today()
    width, height = get_image_size(filepath)
    insert_image_date(date_saved, filepath, width, height)
