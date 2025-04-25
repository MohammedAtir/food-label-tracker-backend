import sqlite3

def init_db():
    conn = sqlite3.connect('foods.db')
    cursor = conn.cursor()

    # Create table for food items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            sugar REAL,
            carbs REAL,
            protein REAL
        )
    ''')

    conn.commit()
    conn.close()

# Call the function to initialize the database
init_db()
