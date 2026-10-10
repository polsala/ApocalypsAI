import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import { calculateImpactRadius } from '../utils/temporalCalculations';

function EchoMap({ echoes, onEchoSelect }) {
  const defaultPosition = [0, 0]; // Center of the known world, or perhaps a safe zone
  const defaultZoom = 2;

  return (
    <MapContainer center={defaultPosition} zoom={defaultZoom} scrollWheelZoom={true} style={{ height: '100%', width: '100%' }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {echoes.map((echo) => (
        <React.Fragment key={echo.id}>
          <Marker position={[echo.location.lat, echo.location.lng]} eventHandlers={{
            click: () => onEchoSelect(echo),
          }}>
            <Popup>
              <b>Echo ID:</b> {echo.id}<br/>
              <b>Intensity:</b> {echo.intensity}<br/>
              <b>Description:</b> {echo.description}
            </Popup>
          </Marker>
          <Circle
            center={[echo.location.lat, echo.location.lng]}
            radius={calculateImpactRadius(echo.intensity) * 1000} // Radius in meters
            pathOptions={{ color: 'purple', fillColor: 'magenta', fillOpacity: 0.3, weight: 1 }}
            eventHandlers={{
              click: () => onEchoSelect(echo),
            }}
          />
        </React.Fragment>
      ))}
    </MapContainer>
  );
}

export default EchoMap;
