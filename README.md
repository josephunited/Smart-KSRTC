KSRTC Smart Bus Stop
The KSRTC Smart Bus Stop is a web application designed to provide real-time bus tracking for Kerala State Road Transport Corporation (KSRTC) buses. The app displays live bus locations and bus stop information on an interactive Mapbox map, with a Flask backend managing data in a SQLite database. The backend is exposed via ngrok for development and testing. This project was developed as a mini-project for real-time transit tracking.
Features

Real-Time Bus Tracking: Displays live KSRTC bus locations on a Mapbox map, updated every second.
Bus Stop Information: Shows bus stops and depots with custom FontAwesome icons (blue for main stops, orange for depots, grey for regular stops) and popups with stop names.
Reset Map View: Includes a "Reset Map" button to recenter the map on Kesavadasapuram, Kerala, showing nearby buses and stops.
Bus Schedule: Lists upcoming buses with routes and estimated arrival times.
Location Simulation: Provides a send_location.html page to simulate bus location updates for testing.
Local FontAwesome Icons: Uses offline FontAwesome icons for bus (fa-bus) and stop (fa-house, fa-circle) markers.

Tech Stack

Frontend: HTML, CSS, JavaScript, Mapbox GL JS, FontAwesome
Backend: Flask (Python), SQLite
Development Tools: ngrok (for tunneling), http-server (for web testing)
Dependencies: Flask-CORS, Mapbox API

Prerequisites
Before setting up the project, ensure you have the following installed:

Python (3.8 or higher)
Node.js (16.x or higher)
ngrok (free account for tunneling)
Git (for cloning and version control)
A Mapbox Access Token (sign up at mapbox.com)

Installation

Clone the Repository:
git clone https://github.com/your-username/ksrtc-smart-bus-stop.git
cd ksrtc-smart-bus-stop


Set Up the Backend:

Install Python dependencies:pip install flask flask-cors


Initialize the SQLite database:
Run python app.py to create bus_locations.db and populate it with bus stop data (defined in app.py).




Set Up the Frontend:

Navigate to the www/ folder:cd www


Install http-server globally (for web testing):npm install -g http-server




Configure ngrok:

Download and install ngrok from ngrok.com.
Start ngrok to tunnel your Flask server (run in a separate terminal):ngrok http 5000


Update the ngrok URL in www/js/config.js:const CONFIG = {
    API_BASE_URL: 'https://your-ngrok-url.ngrok.io'
};




Set Up Mapbox:

Replace the Mapbox access token in www/js/script.js with your own:mapboxgl.accessToken = 'your-mapbox-token';





Usage

Run the Backend:

Start the Flask server:python app.py


Ensure it’s running on http://127.0.0.1:5000.


Run ngrok:

Start ngrok to expose the Flask server (in a separate terminal):ngrok http 5000


Update www/js/config.js with the new ngrok URL.


Run the Web App:

Navigate to www/:cd www


Start http-server:http-server


Open http://192.168.56.1:8080 or http://localhost:8080 in a browser.
Verify:
The Mapbox map loads, centered on Kesavadasapuram.
Bus stop icons (fa-house, fa-circle) and bus icons (fa-bus) appear.
The "Reset Map" button recenters the map.
The bus schedule lists upcoming buses.
Check DevTools (F12) for errors.




Simulate Bus Locations:

Open http://192.168.56.1:8080/send_location.html in a browser.
Enter a bus ID (e.g., Bus101), click "Start Sending Location" to simulate updates, and check the map for the bus marker.
Note: Geolocation simulation may require browser permissions or mock coordinates for testing.



Project Structure
ksrtc-smart-bus-stop/
├── app.py                  # Flask backend with SQLite database setup
├── bus_locations.db        # SQLite database for bus locations and stops
├── www/                    # Frontend assets
│   ├── css/                # Styles (fontawesome.css, styles.css)
│   ├── js/                 # Scripts (config.js, script.js)
│   ├── webfonts/           # FontAwesome fonts
│   ├── index.html          # Main web app page
│   └── send_location.html  # Location simulation page
├── README.md               # Project documentation

Troubleshooting

CORS Errors:
Ensure Flask-CORS is installed and CORS(app) is added to app.py.
Check DevTools Network tab for Access-Control-Allow-Origin headers.


Map Not Loading:
Verify Mapbox token in script.js.
Ensure <div id="map"> exists in index.html.
Check for Uncaught Error: Container 'map' not found in DevTools Console.


Icons Missing:
Confirm css/fontawesome.css and webfonts/ are in www/.
Test FontAwesome with a simple HTML page (e.g., <i class="fas fa-bus"></i>).


ngrok URL Issues:
Update www/js/config.js with the current ngrok URL after each ngrok restart.
Ensure script.js and send_location.html use CONFIG.API_BASE_URL for API calls.


Script Errors:
Check for Uncaught SyntaxError: Identifier 'shouldFitBounds' has already been declared in DevTools Console.
Verify script.js has only one let shouldFitBounds declaration and is not included multiple times in index.html.
Ensure script.js file size is ~3-4 KB (not ~6 KB, which may indicate duplicates).



Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or feedback, contact your-email@example.com or open an issue on GitHub.
