const alertBanner = document.getElementById("alertBanner");
const map = L.map('map').setView([28.6145, 77.2095], 14);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let ambulanceMarker = null;
let vehicleMarkers = {};

// 🚑 Emoji Icons using DivIcon

const ambulanceIcon = L.divIcon({
    html: "🚑",
    className: "emoji-icon",
    iconSize: [40, 40],
    iconAnchor: [20, 20]
});

const normalVehicleIcon = L.divIcon({
    html: "🚗",
    className: "emoji-icon",
    iconSize: [35, 35],
    iconAnchor: [17, 17]
});

const alertVehicleIcon = L.divIcon({
    html: "🚨",
    className: "emoji-icon",
    iconSize: [35, 35],
    iconAnchor: [17, 17]
});
async function fetchAmbulances() {
    const response = await fetch("http://127.0.0.1:8000/ambulance/");
    return await response.json();
}

async function fetchVehicles() {
    const response = await fetch("http://127.0.0.1:8000/vehicle/");
    return await response.json();
}

async function updateMap() {

    const ambulances = await fetchAmbulances();
    const vehicles = await fetchVehicles();

    if (ambulances.length === 0) return;

    const amb = ambulances[0];

    // Update ambulance
    if (!ambulanceMarker) {
        ambulanceMarker = L.marker(
            [amb.latitude, amb.longitude],
            { icon: ambulanceIcon }
        ).addTo(map)
         .bindPopup("Ambulance: " + amb.vehicle_number);
    } else {
        ambulanceMarker.setLatLng([amb.latitude, amb.longitude]);
        // map.setView([amb.latitude, amb.longitude], 14);
    }

    // Trigger alert engine
    const alertResponse = await fetch("http://127.0.0.1:8000/ambulance/update-location", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            vehicle_number: amb.vehicle_number,
            latitude: amb.latitude,
            longitude: amb.longitude,
            speed: amb.speed
        })
    });

    const alertData = await alertResponse.json();
    const alertedVehicles = alertData.vehicles_alerted.map(v => v.vehicle_number);

    let alertActive = false;

    vehicles.forEach(vehicle => {

        let marker = vehicleMarkers[vehicle.vehicle_number];
        const isAlerted = alertedVehicles.includes(vehicle.vehicle_number);

        if (!marker) {
            marker = L.marker(
                [vehicle.latitude, vehicle.longitude],
                { icon: normalVehicleIcon }
            ).addTo(map);

            vehicleMarkers[vehicle.vehicle_number] = marker;
        } else {
            marker.setLatLng([vehicle.latitude, vehicle.longitude]);
        }

        if (isAlerted) {
            alertActive = true;
            marker.setIcon(alertVehicleIcon);
            marker.bindPopup("🚨 EMERGENCY VEHICLE APPROACHING!").openPopup();
        } else {
            marker.setIcon(normalVehicleIcon);
            marker.bindPopup("Vehicle: " + vehicle.vehicle_number);
        }
    });
    if (alertActive) {
        alertBanner.classList.remove("hidden");
    } else {
        alertBanner.classList.add("hidden");
    }
}

// Auto refresh
setInterval(updateMap, 3000);
updateMap();