import sqlite3

def init_db():
    # Connect to (or create) the database file
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Create the tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'active'
        )
    ''')

    # Create the notes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()
    print("Database initialized successfully with 'tasks' and 'notes' tables.")

if __name__ == "__main__":
    init_db()
