import sqlite3

def get_classroom_titles():
    query = 'SELECT title FROM classrooms'
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        db_rows = cursor.fetchall()
    return [row[0] for row in db_rows]
