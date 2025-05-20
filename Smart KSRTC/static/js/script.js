// Initialize Mapbox
mapboxgl.accessToken = "pk.eyJ1IjoianV3ZWxqbyIsImEiOiJjbTl5MGFmZ3AxNW12MmxyMHF3bnM2NWd5In0.1RXRSwz18tX5m9EKGy3rVQ"; // Replace with your Mapbox token

var map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/streets-v11",
    center: [76.93761052468263, 8.529806571358003], // Center on Kesavadasapuram
    zoom: 16 // Increased zoom level for closer view
});

// Store all live bus markers
var liveMarkers = {};

// Store bus stop markers
var busStopMarkers = [];

// Flag to control whether to fit bounds
let shouldFitBounds = true;

// Fetch latest bus locations and update map
function updateBusLocations() {
    fetch('/get_locations')
        .then(response => response.json())
        .then(data => {
            Object.keys(data).forEach(busId => {
                const { latitude, longitude } = data[busId];
                if (!liveMarkers[busId]) {
                    let markerElement = document.createElement("div");
                    markerElement.className = "bus-marker";
                    markerElement.innerHTML = `
                        <i class="fas fa-bus" style="font-size:24px; color:#ff6f00;"></i>
                        <br>
                        <span style="font-size:12px; color:white; background:#333; padding:2px 5px; border-radius:3px;">${busId}</span>
                    `;
                    liveMarkers[busId] = new mapboxgl.Marker({ element: markerElement })
                        .setLngLat([longitude, latitude])
                        .addTo(map);
                } else {
                    liveMarkers[busId].setLngLat([longitude, latitude]);
                }
            });

            // Only adjust bounds if shouldFitBounds is true
            if (shouldFitBounds) {
                const bounds = new mapboxgl.LngLatBounds();
                const kesavadasapuramCoords = [76.93761052468263, 8.529806571358003];
                bounds.extend(kesavadasapuramCoords);

                // Include live bus locations if they are close to Kesavadasapuram
                Object.values(data).forEach(loc => {
                    const distance = getDistance(
                        kesavadasapuramCoords[1], kesavadasapuramCoords[0],
                        loc.latitude, loc.longitude
                    );
                    if (distance < 1) { // Only include buses within 1 km of Kesavadasapuram
                        bounds.extend([loc.longitude, loc.latitude]);
                    }
                });

                // Include bus stops within a smaller radius (e.g., 1 km)
                busStopMarkers.forEach(marker => {
                    const coords = marker.getLngLat();
                    const distance = getDistance(
                        kesavadasapuramCoords[1], kesavadasapuramCoords[0],
                        coords.lat, coords.lng
                    );
                    if (distance < 1) { // Only include stops within 1 km
                        bounds.extend([coords.lng, coords.lat]);
                    }
                });

                if (!bounds.isEmpty()) {
                    map.fitBounds(bounds, { padding: 50, maxZoom: 16 });
                    shouldFitBounds = false; // Disable auto-fitting after initial setup
                }
            }
        })
        .catch(error => console.error("Error fetching bus locations:", error));
}

// Helper function to calculate distance in km (Haversine formula)
function getDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the earth in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in km
}

// Function to reset map view to default bounds
function resetMapView() {
    shouldFitBounds = true;
    updateBusLocations();
}

setInterval(updateBusLocations, 1000);

// Fetch and add bus stops and depots from the server
fetch('/get_bus_stops')
    .then(response => response.json())
    .then(data => {
        data.forEach(stop => {
            const el = document.createElement("div");
            if (stop.type === "main") {
                el.className = "safehouse-marker pulse";
                el.innerHTML = `<div style="position: relative;"><i class="fas fa-circle" style="font-size: 10px; color: #00bcd4; position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%);"></i><i class="fas fa-house" style="font-size:34px; color:#00bcd4;"></i></div>`;
            } else if (stop.type === "depot") {
                el.className = "orange-safehouse-marker";
                el.innerHTML = `<i class="fas fa-house" style="font-size:26px; color:#ff6f00;"></i>`;
            } else {
                el.className = "grey-safehouse-marker";
                el.innerHTML = `<i class="fas fa-house" style="font-size:26px; color:#757575;"></i>`;
            }
            const marker = new mapboxgl.Marker(el)
                .setLngLat([stop.longitude, stop.latitude])
                .setPopup(new mapboxgl.Popup({ offset: 25, className: 'popup' }).setHTML(`<b style="background: rgba(0,0,0,0.7); padding: 5px;">${stop.name}</b>`))
                .addTo(map);
            busStopMarkers.push(marker);
        });
        // Trigger initial map view setup after bus stops are loaded
        updateBusLocations();
    })
    .catch(error => console.error("Error fetching bus stops:", error));