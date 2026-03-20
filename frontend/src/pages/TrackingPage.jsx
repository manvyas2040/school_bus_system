import { useState } from "react";

import BusMap from "../components/map/BusMap";
import Card from "../components/ui/Card";
import Spinner from "../components/ui/Spinner";
import { getGps } from "../services/api";

export default function TrackingPage() {
  const [busId, setBusId] = useState("");
  const [gps, setGps] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchGps = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await getGps(Number(busId));
      setGps(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "GPS data not found");
      setGps(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto grid w-full max-w-5xl gap-5 px-4 py-8 sm:px-6">
      <Card title="Public GPS Tracking" subtitle="Parents can track live bus positions by Bus ID" delay={80}>
        <form onSubmit={fetchGps} className="flex flex-col gap-3 sm:flex-row">
          <input
            value={busId}
            onChange={(e) => setBusId(e.target.value)}
            placeholder="Enter Bus ID"
            className="w-full rounded-xl border border-ink/20 px-3 py-2 sm:max-w-xs"
            required
          />
          <button className="rounded-xl bg-ink px-4 py-2 font-semibold text-white">{loading ? "Searching..." : "Track"}</button>
        </form>
        {loading && <div className="mt-3"><Spinner label="Fetching latest GPS" /></div>}
        {error && <p className="mt-3 rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
      </Card>

      {gps && (
        <Card title={`Bus ${gps.bus_id} Live Location`} delay={140}>
          <div className="mb-3 text-sm text-ink/70">
            Coordinates: {gps.latitude}, {gps.longitude}
          </div>
          <BusMap latitude={gps.latitude} longitude={gps.longitude} />
          <p className="mt-3 text-sm text-ink/60">Updated: {new Date(gps.updated_at).toLocaleString()}</p>
        </Card>
      )}
    </div>
  );
}
