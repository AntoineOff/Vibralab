# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'database.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        ''')

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        with sqlite3.connect(DATABASE) as conn:
            try:
                conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Email already registered.', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect(DATABASE) as conn:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

            if user and check_password_hash(user[3], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
