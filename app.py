from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Schedule an appointment
@app.route('/schedule', methods=['POST'])
def schedule():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    time = request.form['time']
    
    # Insert the appointment into the database
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('INSERT INTO appointments (name, email, phone, date, time) VALUES (?, ?, ?, ?, ?)',
              (name, email, phone, date, time))
    conn.commit()
    conn.close()

    return redirect(url_for('appointments'))

# View all scheduled appointments
@app.route('/appointments')
def appointments():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('SELECT * FROM appointments ORDER BY date, time')
    appointments = c.fetchall()
    conn.close()
    return render_template('appointments.html', appointments=appointments)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
