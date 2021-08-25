window.onload = function () {

  // Defines userMarker
  const redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  // Initialized userMarker
  let userMarker;

  // Initialize Leaflet map
  const myMap = L.map('mapid').setView([43.0731, -89.4012], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(myMap);


  // Sets click on map function to add to latitude and longitude inputs
  myMap.on('click', (e) => {

    userMarker = L.marker(e.latlng, { icon: redIcon }).addTo(myMap);

    const { lat, lng } = e.latlng;

    document.getElementById('latitude').value = lat;
    document.getElementById('longitude').value = lng;
  });

};

