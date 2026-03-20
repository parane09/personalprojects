import sqlite3

def init_db():
    # Connect to (or create) the database file
    conn = sqlite3.connect('marksheets.db')
    cursor = conn.cursor()

    # Create the table using SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS marksheets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mean REAL,
            median REAL,
            std REAL,
            min REAL,
            max REAL
        )
    ''')

    # Save changes and close the connection
    conn.commit()
    conn.close()
    print("Database and 'marksheets' table have been created successfully!")

if __name__ == "__main__":
    init_db()
