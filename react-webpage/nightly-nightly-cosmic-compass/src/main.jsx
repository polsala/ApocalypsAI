import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Mock icons for Leaflet to prevent errors in testing environments
// Mock rationale: Leaflet's default icons require image files which are not bundled
// in this self-contained utility. These mocks ensure the component renders without errors.
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeTo('iconUrl', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=');
L.Icon.Default.mergeTo('shadowUrl', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=');

// Mock data for celestial bodies and alien civilizations
// Mock rationale: These are static, fictional data points for demonstration and testing purposes.
const mockCelestialBodies = [
  { id: 1, name: 'Nebula of Whispers', lat: 40.7128, lng: -74.0060, description: 'A swirling cloud of cosmic dust, said to carry ancient secrets.' },
  { id: 2, name: 'Xylos Prime', lat: 34.0522, lng: -118.2437, description: 'A gas giant with rings of pure energy.' },
  { id: 3, name: 'Asteroid Belt of Giggles', lat: 48.8566, lng: 2.3522, description: 'A chaotic cluster of rocks that occasionally emit faint, joyful sounds.' },
];

const mockAlienCivilizations = [
  { id: 101, name: 'Zorpian Outpost', lat: 51.5074, lng: -0.1278, description: 'A small, friendly outpost of the Zorpian Federation.' },
  { id: 102, name: 'Gleep Glorp Colony', lat: 41.9028, lng: 12.4964, description: 'Known for their peculiar love of pasta and existential dread.' },
  { id: 103, name: 'The Lumina Collective', lat: 35.6895, lng: 139.6917, description: 'Beings of pure light, communicating through interpretive dance.' },
];

function CosmicCompass() {
  const [position, setPosition] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setPosition({
            lat: pos.coords.latitude,
            lng: pos.coords.longitude,
          });
        },
        (err) => {
          setError(err.message);
          // Fallback to a default location if geolocation fails
          setPosition({ lat: 38.8951, lng: -77.0364 }); // Washington D.C.
        }
      );
    } else {
      setError('Geolocation is not supported by your browser.');
      // Fallback to a default location
      setPosition({ lat: 38.8951, lng: -77.0364 }); // Washington D.C.
    }
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-black to-purple-900 text-white font-sans p-4">
      <h1 className="text-4xl font-bold text-center mb-8 cosmic-shadow">Cosmic Compass</h1>
      <p className="text-center text-lg mb-8">Your whimsical guide to the universe, starting from your current location.</p>

      {error && <p className="text-center text-red-500 mb-4">Error: {error}</p>}

      <div className="w-full h-[60vh] rounded-lg shadow-xl overflow-hidden border-2 border-purple-700">
        {position ? (
          <MapContainer
            center={[position.lat, position.lng]}
            zoom={3}
            style={{ height: '100%', width: '100%' }}
            className="bg-black"
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors &copy; ApocalypsAI"
              // Custom dark tile layer for a more cosmic feel
              // Mock rationale: Using a placeholder URL as a real dark tile layer might require external API keys or specific setup.
              // In a real app, you'd use something like: 'https://tiles.stadiamaps.com/tiles/stamen_toner_lite/{z}/{x}/{y}.png'
              // For this example, we'll stick to a basic one and style it with CSS.
              subdomains={['a', 'b', 'c']}
            />
            <Marker position={[position.lat, position.lng]}>
              <Popup>Your current location! <br /> Somewhere in the cosmos.</Popup>
            </Marker>

            {/* Celestial Bodies */}
            {mockCelestialBodies.map(body => (
              <Marker key={body.id} position={[body.lat, body.lng]}>
                <Popup>
                  <strong>{body.name}</strong><br />{body.description}
                </Popup>
              </Marker>
            ))}

            {/* Alien Civilizations */}
            {mockAlienCivilizations.map(civ => (
              <Marker key={civ.id} position={[civ.lat, civ.lng]}>
                <Popup>
                  <strong>{civ.name}</strong><br />{civ.description}
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        ) : (
          <div className="flex items-center justify-center h-full bg-gray-800">
            <p>Loading cosmic coordinates...</p>
          </div>
        )}
      </div>
      <div className="mt-8 text-center">
        <p className="text-sm text-gray-400">"The universe is not only stranger than we imagine, it is stranger than we *can* imagine." - Arthur Eddington (and maybe Zorp)</p>
      </div>
    </div>
  );
}

export default CosmicCompass;
