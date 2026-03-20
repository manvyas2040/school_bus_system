import { useEffect, useState } from "react";

import BusMap from "../components/map/BusMap";
import Card from "../components/ui/Card";
import Spinner from "../components/ui/Spinner";
import { getGps, getMe, getTimetable, updateGps } from "../services/api";

export default function DriverDashboard() {
  const [profile, setProfile] = useState(null);
  const [gps, setGps] = useState(null);
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState("");
  const [timetable, setTimetable] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError("");
    try {
      const me = await getMe();
      setProfile(me);

      if (me.bus_id) {
        const gpsData = await getGps(me.bus_id);
        setGps(gpsData);
        setLatitude(String(gpsData.latitude));
        setLongitude(String(gpsData.longitude));

        if (me.route_id) {
          const timetableData = await getTimetable(me.route_id);
          setTimetable(timetableData);
        }
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to load driver data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const submitGps = async (event) => {
    event.preventDefault();
    if (!profile?.bus_id) return;

    setUpdating(true);
    setError("");
    try {
      const data = await updateGps(profile.bus_id, {
        latitude: Number(latitude),
        longitude: Number(longitude),
      });
      setGps(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to update GPS");
    } finally {
      setUpdating(false);
    }
  };

  const autoLocate = () => {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported on this browser");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLatitude(position.coords.latitude.toFixed(6));
        setLongitude(position.coords.longitude.toFixed(6));
      },
      () => {
        setError("Unable to fetch your current location");
      },
      { enableHighAccuracy: true, timeout: 9000 },
    );
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <Spinner label="Loading driver dashboard" />
      </div>
    );
  }

  return (
    <div className="mx-auto grid w-full max-w-6xl gap-5 px-4 py-8 sm:px-6 lg:grid-cols-2">
      <Card title="Driver Dashboard" subtitle="Update your assigned bus location" className="lg:col-span-2" delay={50}>
        <div className="flex flex-wrap gap-3 text-sm">
          <span className="rounded-full bg-ink/10 px-3 py-1">User: {profile?.username}</span>
          <span className="rounded-full bg-skyrail/10 px-3 py-1 text-skyrail">Bus ID: {profile?.bus_id ?? "Unassigned"}</span>
          <span className="rounded-full bg-mintline/10 px-3 py-1 text-mintline">Role: {profile?.role}</span>
        </div>
      </Card>

      <Card title="Update GPS" delay={120}>
        {profile?.bus_id ? (
          <form className="space-y-3" onSubmit={submitGps}>
            <input value={latitude} onChange={(e) => setLatitude(e.target.value)} placeholder="Latitude" className="w-full rounded-xl border border-ink/20 px-3 py-2" required />
            <input value={longitude} onChange={(e) => setLongitude(e.target.value)} placeholder="Longitude" className="w-full rounded-xl border border-ink/20 px-3 py-2" required />
            <div className="flex gap-2">
              <button type="button" onClick={autoLocate} className="rounded-xl border border-ink/20 px-4 py-2">
                Use Current Location
              </button>
              <button className="rounded-xl bg-ink px-4 py-2 text-white">{updating ? "Saving..." : "Push GPS"}</button>
            </div>
          </form>
        ) : (
          <p className="text-sm text-ink/70">No bus assigned. Ask admin to assign your bus first.</p>
        )}
        {error && <p className="mt-3 rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
      </Card>

      <Card title="Live Position" delay={180}>
        {gps ? (
          <div className="space-y-3">
            <p className="text-sm text-ink/70">
              Last update: <strong>{new Date(gps.updated_at).toLocaleString()}</strong>
            </p>
            <BusMap latitude={gps.latitude} longitude={gps.longitude} />
          </div>
        ) : (
          <p className="text-sm text-ink/70">No GPS data available yet.</p>
        )}
      </Card>

      <Card title="Route Timetable" className="lg:col-span-2" delay={240}>
        {timetable?.entries?.length ? (
          <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
            {timetable.entries.map((entry, index) => (
              <div key={`${entry.bus_number}-${index}`} className="rounded-2xl border border-ink/10 bg-white px-3 py-2 text-sm">
                <p className="font-semibold text-ink">Bus {entry.bus_number}</p>
                <p className="text-ink/60">Checkpoint: {entry.checkpoint}</p>
                <p className="text-ink/60">ETA: {entry.eta_minutes} min</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-ink/70">Timetable appears once route data is linked to your bus.</p>
        )}
      </Card>
    </div>
  );
}
