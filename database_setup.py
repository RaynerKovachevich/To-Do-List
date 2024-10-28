import sqlite3

def create_database():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    
    #Create 'users' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )               
        ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
        )               
        ''')
    
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    create_database()
    
    