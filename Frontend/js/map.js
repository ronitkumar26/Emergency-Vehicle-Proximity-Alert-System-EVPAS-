const sirenSound = document.getElementById("sirenSound");
let sirenPlaying = false;
const alertBanner = document.getElementById("alertBanner");
const map = L.map('map').setView([28.6145, 77.2095], 14);

let audioUnlocked = false;

document.addEventListener("click", () => {
    if (!audioUnlocked) {
        sirenSound.play().then(() => {
            sirenSound.pause();
            sirenSound.currentTime = 0;
            audioUnlocked = true;
            console.log("Audio unlocked");
        }).catch(err => {
            console.log("Audio still blocked:", err);
        });
    }
});

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
    const alertedVehicles = alertData.vehicles_alerted;

    let alertActive = false;
    let nearestDistance = null;

    vehicles.forEach(vehicle => {
        
        let marker = vehicleMarkers[vehicle.vehicle_number];

        const alertVehicle = alertedVehicles.find(
            v => v.vehicle_number === vehicle.vehicle_number
        );

        const isAlerted = !!alertVehicle;

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

            marker.bindPopup(
                "🚨 EMERGENCY APPROACHING<br>Distance: " +
                alertVehicle.distance_km + " km"
            ).openPopup();

            nearestDistance = alertVehicle.distance_km;

        } else {
            marker.setIcon(normalVehicleIcon);
            marker.bindPopup("Vehicle: " + vehicle.vehicle_number);
        }

    });
    if (alertActive) {

        alertBanner.classList.remove("hidden");
        alertBanner.innerHTML = `
            🚑 Emergency Vehicle Approaching <br>
            Distance: ${nearestDistance} km
        `;
    
        if (sirenSound.paused) {
            sirenSound.play().catch(err => console.log(err));
        }
    
    } else {
    
        alertBanner.innerHTML = "✅ Emergency Cleared";
        
        setTimeout(() => {
            alertBanner.classList.add("hidden");
        }, 2000);
    
        if (!sirenSound.paused) {
            sirenSound.pause();
            sirenSound.currentTime = 0;
        }
    }
}

// Auto refresh
setInterval(updateMap, 3000);
updateMap();