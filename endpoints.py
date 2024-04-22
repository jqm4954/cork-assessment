from flask import Flask, jsonify, request
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
    if assets:
        return jsonify(assets)
    else:
        return {'message': 'No assets found.'}, 404

# GET request that returns single asset given ID
@app.route('/assets/<id>', methods=['GET'])
def get_one_asset(id):
    conn = get_connection()
    cursor = conn.cursor()
    data = ({"id":id})
    cursor.execute("SELECT * FROM assets WHERE id = :id", data)
    asset = cursor.fetchone()
    conn.close()
    if asset:
        return jsonify(asset)
    else:
        return {'message': 'Asset not found.'}, 404

# DELETE request that removes a single asset given ID
@app.route('/assets/<id>', methods=['DELETE'])
def delete_one_asset(id):
    conn = get_connection()
    cursor = conn.cursor()
    data = ({"id":id})
    cursor.execute("SELECT * FROM assets WHERE id=:id", data)
    asset = cursor.fetchone()
    if not asset:
        conn.close()
        return {'message': 'Asset not found'}, 404
    else:
        cursor.execute("DELETE FROM assets WHERE id=:id", data)
        conn.commit()
        conn.close()
        return {'message':'Asset successfully deleted'}, 202

# POST request to add single asset to db
@app.route('/assets', methods=['POST'])
def post_one_asset():
    incoming_data = request.get_json()
    db_data = ({"name": incoming_data.get('name'),
                "type": incoming_data.get('type'),
                "serial_number": incoming_data.get('serial_number'),
                "operating_system": incoming_data.get('operating_system')
                })
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO assets 
                   (name, type, serial_number, operating_system) VALUES
                   (:name, :type, :serial_number, :operating_system)
                   ''', db_data)
    except sqlite3.IntegrityError:
        return {'message': 'Incorrect information supplied. Please provide name, type, serial number, and operating system'}, 422
    conn.commit()
    conn.close()
    return {'message': 'Asset successfully inserted'}, 201

# POST request to update single asset
@app.route('/assets/<id>', methods=['POST'])
def update_asset(id):
    incoming_data = request.get_json()
    db_data = ({"name": incoming_data.get('name'),
                "type": incoming_data.get('type'),
                "serial_number": incoming_data.get('serial_number'),
                "operating_system": incoming_data.get('operating_system'),
                "id":id
                })
    conn = get_connection()
    cursor = conn.cursor()
    # Try updating
    try:
        cursor.execute('''UPDATE assets SET name=:name, 
                       type=:type,
                       serial_number=:serial_number
                       operating_system=:operating_system
                       WHERE id=:id''', db_data)
        conn.commit()
        return {'message':'Update successful'}, 201
    except sqlite3.IntegrityError:
        return {'message':'Update not successful. Please provide updated name, type, serial number, and operating system'}, 422


if __name__ == "__main__":
    create_db()
    app.run()