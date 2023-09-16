from flask import Flask, jsonify, request, render_template
import sqlite3
import requests

app = Flask(__name__)
app.config['DEBUG'] = True

# API URLs
api1_url = "http://127.0.0.1/rfid-data"  #rfid_data api
api2_url = "http://127.0.0.1/weighbridge-data"  #weighbridge_data api

# SQLite database setup
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   api1_data TEXT,
                   api2_data TEXT)''')
conn.commit()

# Function to fetch data from APIs
def fetch_data():
    api1_response = requests.get(api1_url)
    api2_response = requests.get(api2_url)
    api1_data = api1_response.json()
    api2_data = api2_response.json()
    return api1_data, api2_data

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# API endpoint to fetch live data
@app.route('/api/live-data', methods=['GET'])
def live_data():
    api1_data, api2_data = fetch_data()
    print(api1_data, api2_data)
    return jsonify(api1_data=api1_data, api2_data=api2_data)

# API endpoint to save data
@app.route('/api/save-data', methods=['POST'])
def save_data():
    api1_data, api2_data = fetch_data()
    cursor.execute("INSERT INTO data (api1_data, api2_data) VALUES (?, ?)", (str(api1_data), str(api2_data)))
    conn.commit()
    return jsonify(message="Data saved successfully")

# API endpoint to retrieve logged data
@app.route('/api/logged-data', methods=['GET'])
def logged_data():
    cursor.execute("SELECT * FROM data")
    result = cursor.fetchall()
    data = []
    for row in result:
        data.append({
            'id': row[0],
            'api1_data': row[1],
            'api2_data': row[2]
        })
    return jsonify(data)

if __name__ == '__main__':
    app.run() # Run on port 5000
