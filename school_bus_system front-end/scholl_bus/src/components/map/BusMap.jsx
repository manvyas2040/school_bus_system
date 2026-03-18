import { CircleMarker, MapContainer, TileLayer } from "react-leaflet";

export default function BusMap({ latitude, longitude }) {
  const position = [latitude, longitude];

  return (
    <div className="h-72 overflow-hidden rounded-2xl border border-white/60">
      <MapContainer center={position} zoom={14} className="h-full w-full">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <CircleMarker
          center={position}
          radius={10}
          pathOptions={{ color: "#ef4444", fillColor: "#ef4444", fillOpacity: 0.95 }}
        />
      </MapContainer>
    </div>
  );
}
