from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_connection():
    return sqlite3.connect("assets.db")

def create_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   type TEXT NOT NULL,
                   serial_number INTEGER NOT NULL,
                   operating_system TEXT NOT NULL
        )''')
    conn.commit()
    conn.close()

