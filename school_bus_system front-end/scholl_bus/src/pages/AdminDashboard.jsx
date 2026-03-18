import { useCallback, useEffect, useMemo, useState } from "react";

import Card from "../components/ui/Card";
import Spinner from "../components/ui/Spinner";
import {
  assignDriver,
  assignStudent,
  createBus,
  createRoute,
  createStudent,
  getBuses,
  getDrivers,
  getRoutes,
  getStudents,
} from "../services/api";

export default function AdminDashboard() {
  const [routes, setRoutes] = useState([]);
  const [buses, setBuses] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [students, setStudents] = useState([]);
  const [totalStudents, setTotalStudents] = useState(0);
  const [page, setPage] = useState(1);
  const [busSearch, setBusSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [routeName, setRouteName] = useState("");
  const [busForm, setBusForm] = useState({ number: "", route_id: "" });
  const [studentForm, setStudentForm] = useState({ name: "", roll: "", bus_id: "" });
  const [assignDriverForm, setAssignDriverForm] = useState({ bus_id: "", driver_id: "" });
  const [assignStudentForm, setAssignStudentForm] = useState({ student_id: "", bus_id: "" });

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [routeData, busData, driverData, studentData] = await Promise.all([
        getRoutes(),
        getBuses(busSearch),
        getDrivers(),
        getStudents(page, 8),
      ]);
      setRoutes(routeData);
      setBuses(busData.items || []);
      setDrivers(driverData.items || []);
      setStudents(studentData.items || []);
      setTotalStudents(studentData.total || 0);
    } catch (err) {
      setError(err?.response?.data?.detail || err.message || "Failed to load admin data");
    } finally {
      setLoading(false);
    }
  }, [busSearch, page]);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  const totalPages = useMemo(() => Math.max(1, Math.ceil(totalStudents / 8)), [totalStudents]);

  const handleCreateRoute = async (e) => {
    e.preventDefault();
    await createRoute({ name: routeName });
    setRouteName("");
    loadDashboard();
  };

  const handleCreateBus = async (e) => {
    e.preventDefault();
    await createBus({ number: busForm.number, route_id: Number(busForm.route_id) });
    setBusForm({ number: "", route_id: "" });
    loadDashboard();
  };

  const handleCreateStudent = async (e) => {
    e.preventDefault();
    await createStudent({
      name: studentForm.name,
      roll: studentForm.roll,
      bus_id: studentForm.bus_id ? Number(studentForm.bus_id) : null,
    });
    setStudentForm({ name: "", roll: "", bus_id: "" });
    loadDashboard();
  };

  const handleAssignDriver = async (e) => {
    e.preventDefault();
    await assignDriver(Number(assignDriverForm.bus_id), Number(assignDriverForm.driver_id));
    setAssignDriverForm({ bus_id: "", driver_id: "" });
    loadDashboard();
  };

  const handleAssignStudent = async (e) => {
    e.preventDefault();
    await assignStudent(Number(assignStudentForm.student_id), Number(assignStudentForm.bus_id));
    setAssignStudentForm({ student_id: "", bus_id: "" });
    loadDashboard();
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <Spinner label="Loading admin dashboard" />
      </div>
    );
  }

  return (
    <div className="mx-auto grid w-full max-w-6xl gap-5 px-4 py-8 sm:px-6 lg:grid-cols-2">
      <Card title="Admin Command Center" subtitle="Manage routes, buses, drivers, and students" className="lg:col-span-2" delay={50}>
        {error && <p className="rounded-xl bg-red-50 px-4 py-2 text-sm text-red-700">{error}</p>}
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <input
            value={busSearch}
            onChange={(e) => setBusSearch(e.target.value)}
            placeholder="Search buses by number"
            className="rounded-xl border border-ink/20 px-3 py-2 text-sm"
          />
          <span className="rounded-full bg-mintline/10 px-3 py-1 text-xs font-semibold text-mintline">Routes: {routes.length}</span>
          <span className="rounded-full bg-skyrail/10 px-3 py-1 text-xs font-semibold text-skyrail">Buses: {buses.length}</span>
          <span className="rounded-full bg-amberline/10 px-3 py-1 text-xs font-semibold text-amberline">Students: {totalStudents}</span>
        </div>
      </Card>

      <Card title="Create Route" delay={100}>
        <form className="space-y-3" onSubmit={handleCreateRoute}>
          <input value={routeName} onChange={(e) => setRouteName(e.target.value)} placeholder="Route name" className="w-full rounded-xl border border-ink/20 px-3 py-2" required />
          <button className="rounded-xl bg-ink px-4 py-2 text-white">Create Route</button>
        </form>
      </Card>

      <Card title="Create Bus" delay={150}>
        <form className="space-y-3" onSubmit={handleCreateBus}>
          <input value={busForm.number} onChange={(e) => setBusForm((prev) => ({ ...prev, number: e.target.value }))} placeholder="Bus number" className="w-full rounded-xl border border-ink/20 px-3 py-2" required />
          <select value={busForm.route_id} onChange={(e) => setBusForm((prev) => ({ ...prev, route_id: e.target.value }))} className="w-full rounded-xl border border-ink/20 px-3 py-2" required>
            <option value="">Select route</option>
            {routes.map((route) => (
              <option key={route.id} value={route.id}>
                {route.name}
              </option>
            ))}
          </select>
          <button className="rounded-xl bg-ink px-4 py-2 text-white">Create Bus</button>
        </form>
      </Card>

      <Card title="Add Student" delay={200}>
        <form className="space-y-3" onSubmit={handleCreateStudent}>
          <input value={studentForm.name} onChange={(e) => setStudentForm((prev) => ({ ...prev, name: e.target.value }))} placeholder="Student name" className="w-full rounded-xl border border-ink/20 px-3 py-2" required />
          <input value={studentForm.roll} onChange={(e) => setStudentForm((prev) => ({ ...prev, roll: e.target.value }))} placeholder="Roll number" className="w-full rounded-xl border border-ink/20 px-3 py-2" required />
          <select value={studentForm.bus_id} onChange={(e) => setStudentForm((prev) => ({ ...prev, bus_id: e.target.value }))} className="w-full rounded-xl border border-ink/20 px-3 py-2">
            <option value="">Optional bus assignment</option>
            {buses.map((bus) => (
              <option key={bus.id} value={bus.id}>
                {bus.number}
              </option>
            ))}
          </select>
          <button className="rounded-xl bg-ink px-4 py-2 text-white">Add Student</button>
        </form>
      </Card>

      <Card title="Assign Driver" delay={250}>
        <form className="space-y-3" onSubmit={handleAssignDriver}>
          <select value={assignDriverForm.driver_id} onChange={(e) => setAssignDriverForm((prev) => ({ ...prev, driver_id: e.target.value }))} className="w-full rounded-xl border border-ink/20 px-3 py-2" required>
            <option value="">Select driver</option>
            {drivers.map((driver) => (
              <option key={driver.id} value={driver.id}>
                {driver.username}
              </option>
            ))}
          </select>
          <select value={assignDriverForm.bus_id} onChange={(e) => setAssignDriverForm((prev) => ({ ...prev, bus_id: e.target.value }))} className="w-full rounded-xl border border-ink/20 px-3 py-2" required>
            <option value="">Select bus</option>
            {buses.map((bus) => (
              <option key={bus.id} value={bus.id}>
                {bus.number}
              </option>
            ))}
          </select>
          <button className="rounded-xl bg-ink px-4 py-2 text-white">Assign Driver</button>
        </form>
      </Card>

      <Card title="Assign Student" delay={300}>
        <form className="space-y-3" onSubmit={handleAssignStudent}>
          <select value={assignStudentForm.student_id} onChange={(e) => setAssignStudentForm((prev) => ({ ...prev, student_id: e.target.value }))} className="w-full rounded-xl border border-ink/20 px-3 py-2" required>
            <option value="">Select student</option>
            {students.map((student) => (
              <option key={student.id} value={student.id}>
                {student.name} ({student.roll})
              </option>
            ))}
          </select>
          <select value={assignStudentForm.bus_id} onChange={(e) => setAssignStudentForm((prev) => ({ ...prev, bus_id: e.target.value }))} className="w-full rounded-xl border border-ink/20 px-3 py-2" required>
            <option value="">Select bus</option>
            {buses.map((bus) => (
              <option key={bus.id} value={bus.id}>
                {bus.number}
              </option>
            ))}
          </select>
          <button className="rounded-xl bg-ink px-4 py-2 text-white">Assign Student</button>
        </form>
      </Card>

      <Card title="Buses" className="lg:col-span-2" delay={350}>
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {buses.map((bus) => (
            <div key={bus.id} className="rounded-2xl border border-ink/10 bg-white px-3 py-2 text-sm">
              <p className="font-semibold text-ink">{bus.number}</p>
              <p className="text-ink/60">Route ID: {bus.route_id}</p>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Students" className="lg:col-span-2" delay={400}>
        <div className="space-y-2">
          {students.map((student) => (
            <div key={student.id} className="flex items-center justify-between rounded-2xl border border-ink/10 bg-white px-3 py-2 text-sm">
              <span className="text-ink">
                {student.name} ({student.roll})
              </span>
              <span className="text-ink/60">Bus: {student.bus_id ?? "Not assigned"}</span>
            </div>
          ))}
          <div className="mt-4 flex items-center justify-between text-sm">
            <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)} className="rounded-lg border border-ink/15 px-3 py-1 disabled:opacity-40">
              Previous
            </button>
            <span>
              Page {page} / {totalPages}
            </span>
            <button disabled={page >= totalPages} onClick={() => setPage((p) => p + 1)} className="rounded-lg border border-ink/15 px-3 py-1 disabled:opacity-40">
              Next
            </button>
          </div>
        </div>
      </Card>
    </div>
  );
}
