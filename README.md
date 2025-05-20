KSRTC Smart Bus Stop
A web app for real-time tracking of KSRTC buses, displaying live bus locations and bus stops on a Mapbox map. Uses a Flask backend with SQLite and ngrok for development.
Features

Shows live bus locations and bus stops with FontAwesome icons.
Includes a "Reset Map" button to recenter on Kesavadasapuram, Kerala.
Lists upcoming buses with routes and times.
Simulates bus location updates via a send_location.html page.

Setup

Install Dependencies:

Install Python and Node.js.
Install Python packages:pip install flask flask-cors


Install http-server:npm install -g http-server




Set Up ngrok:

Install ngrok from ngrok.com.
Create a www/js/config.js file with the ngrok URL:const CONFIG = {
    API_BASE_URL: 'YOUR_NGROK_URL'
};




Set Up Mapbox:

Get a Mapbox access token from mapbox.com and ensure it’s in www/js/script.js.



Usage

Run the Backend:
python app.py


Run ngrok:
ngrok http 5000


Run the Web App:

Navigate to www/:cd www


Start http-server:http-server


Open http://localhost:8080 in a browser.


Simulate Bus Locations:

Visit http://localhost:8080/send_location.html, enter a bus ID, and click "Start Sending Location."



Project Structure
ksrtc-smart-bus-stop/
├── app.py                  # Flask backend
├── bus_locations.db        # SQLite database
├── www/                    # Frontend files
│   ├── css/                # Styles (styles.css, fontawesome.css)
│   ├── js/                 # Scripts (script.js, config.js)
│   ├── webfonts/           # FontAwesome fonts
│   ├── index.html          # Main page
│   └── send_location.html  # Location simulation page
├── README.md               # This file



