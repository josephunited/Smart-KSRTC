import sqlite3
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Initialize SQLite database and create tables
def init_db():
    conn = sqlite3.connect('bus_locations.db')
    c = conn.cursor()
    # Table for live bus locations
    c.execute('''CREATE TABLE IF NOT EXISTS locations
                 (bus_id TEXT PRIMARY KEY, latitude REAL, longitude REAL, timestamp DATETIME)''')
    # Table for bus stops and depots
    c.execute('''CREATE TABLE IF NOT EXISTS bus_stops
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, latitude REAL, longitude REAL, type TEXT)''')
    conn.commit()
    conn.close()

# Populate bus stops and depots data
def populate_bus_stops():
    conn = sqlite3.connect('bus_locations.db')
    c = conn.cursor()
    # Check if bus stops already exist to avoid duplicates
    c.execute('SELECT COUNT(*) FROM bus_stops')
    if c.fetchone()[0] == 0:  # If table is empty, populate it
        stops = [
            ("Kesavadasapuram (Chaithanya Eye Hospital)", 8.529806571358003, 76.93761052468263, "main"),
            ("Bus Stop 1", 8.53028348043197, 76.93863342676488, "stop"),
            ("Bus Stop 2", 8.543319960083254, 76.94176651102204, "stop"),
            ("Bus Stop 3", 8.53554991633029, 76.94898044011757, "stop"),
            ("Bus Stop 4", 8.535337873416472, 76.9491077608212, "stop"),
            ("Bus Stop 5", 8.536043906368786, 76.94491761981257, "stop"),
            ("Bus Stop 6", 8.536001059505974, 76.9443607516276, "stop"),
            ("Bus Stop 7", 8.533694126180992, 76.95348891321636, "stop"),
            ("Bus Stop 8", 8.535539142081957, 76.94278694554244, "stop"),
            ("Bus Stop 9", 8.532712122470947, 76.94015621993819, "stop"),
            ("Bus Stop 10", 8.527083842817488, 76.93907930856085, "stop"),
            ("Bus Stop 11", 8.529663472824545, 76.93489357566608, "stop"),
            ("Bus Stop 12", 8.520345566970477, 76.941615967821, "stop"),
            ("Bus Stop 13", 8.518717475314117, 76.94154828388822, "stop"),
            ("Bus Stop 14", 8.523764984109514, 76.94077725682061, "stop"),
            ("Bus Stop 15", 8.514272392818622, 76.94584498069437, "stop"),
            ("Bus Stop 16", 8.509258933129695, 76.94944837225368, "stop"),
            ("Depot 1", 8.489530601659354, 76.95104781919244, "depot"),
            ("Depot 2", 8.606545035897623, 77.00371841642817, "depot")
        ]
        c.executemany('INSERT INTO bus_stops (name, latitude, longitude, type) VALUES (?, ?, ?, ?)', stops)
        conn.commit()
    conn.close()

# Serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Serve the location sender page
@app.route('/send_location')
def send_location():
    return render_template('send_location.html')

# API to receive new location from a bus
@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.get_json()
    bus_id = data['bus_id']
    latitude = data['latitude']
    longitude = data['longitude']

    # Store in SQLite
    conn = sqlite3.connect('bus_locations.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO locations (bus_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)',
              (bus_id, latitude, longitude, datetime.now()))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

# API to send all current bus locations to frontend
@app.route('/get_locations', methods=['GET'])
def get_locations():
    conn = sqlite3.connect('bus_locations.db')
    c = conn.cursor()
    c.execute('SELECT bus_id, latitude, longitude FROM locations')
    locations = {row[0]: {'latitude': row[1], 'longitude': row[2]} for row in c.fetchall()}
    conn.close()
    return jsonify(locations)

# API to get bus stops and depots
@app.route('/get_bus_stops', methods=['GET'])
def get_bus_stops():
    conn = sqlite3.connect('bus_locations.db')
    c = conn.cursor()
    c.execute('SELECT name, latitude, longitude, type FROM bus_stops')
    stops = [{"name": row[0], "latitude": row[1], "longitude": row[2], "type": row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(stops)

# API to get upcoming buses
bus_schedule = [
    {"id": "Bus101", "name": "Bus 101", "route": "Kesavadasapuram to East Fort", "arrival": (datetime.now() + timedelta(minutes=5)).strftime("%I:%M %p")},
    {"id": "Bus205", "name": "Bus 205", "route": "Technopark to Statue", "arrival": (datetime.now() + timedelta(minutes=10)).strftime("%I:%M %p")},
    {"id": "Bus307", "name": "Bus 307", "route": "Palayam to Vellayambalam", "arrival": (datetime.now() + timedelta(minutes=15)).strftime("%I:%M %p")}
]

@app.route('/get_bus_schedule', methods=['GET'])
def get_bus_schedule():
    for bus in bus_schedule:
        bus["arrival"] = (datetime.now() + timedelta(minutes=(bus_schedule.index(bus) + 1) * 5)).strftime("%I:%M %p")
    return jsonify(bus_schedule)

if __name__ == '__main__':
    init_db()  # Initialize the database
    populate_bus_stops()  # Populate bus stops
    app.run(host='0.0.0.0', port=5000, debug=True)