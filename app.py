from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for the index page
@app.route('/')
def index():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

# Route to add a new todo
@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form['todo']
    conn = get_db_connection()
    conn.execute('INSERT INTO todos (task) VALUES (?)', (new_todo,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route to delete a todo
@app.route('/delete/<int:id>')
def delete_todo(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    # Create the database and the todos table if it doesn't exist
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL)')
    conn.close()
    app.run(debug=True)
