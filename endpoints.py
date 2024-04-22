from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Helper function to return database connection
def get_connection():
    return sqlite3.connect("assets.db")

# Helper function to create DB if not already created
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

# GET request that returns all assets from the table
@app.route('/assets', methods=['GET'])
def get_all_assets():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assets")
    assets = cursor.fetchall()
    conn.close()
    return jsonify(assets)

if __name__ == "__main__":
    create_db()
    app.run()