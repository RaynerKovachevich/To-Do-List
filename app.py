from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

#home ROUTE
@app.route('/')
def index():
    if 'username' not in session:
        return redirect('/login')
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE user_id = ?', (session['user_id'],)).fetchall()
    
    conn.close () 
    return render_template('index.html', tasks=tasks)

#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            session['user_id'] = user['id']
            return redirect('/')
        
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

#Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists. Please choosr another." 
        
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

   

#Route to add a task 
@app.route('/add', methods=['POST'])
def add_task():
    if 'username' not in session:
        return redirect('/login')
    
    task = request.form['task']
    conn = get_db_connection()
    conn.commit()
    conn.close()
    return redirect('/')

#Route to mark task as complete
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET status = ? WHERE id = /', ('complete', task_id) )
    conn.commit()
    conn.close()
    return redirect('/')

#route to log out
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
               