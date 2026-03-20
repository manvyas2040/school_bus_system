import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import Card from "../components/ui/Card";
import Spinner from "../components/ui/Spinner";
import { login } from "../services/api";
import { saveSession } from "../services/auth";

export default function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const from = location.state?.from?.pathname;

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await login({ username, password });
      saveSession(data);

      if (from) {
        navigate(from, { replace: true });
        return;
      }

      navigate(data.role === "admin" ? "/admin" : "/driver", { replace: true });
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto grid w-full max-w-5xl gap-8 px-4 py-12 sm:px-6 md:grid-cols-2">
      <div className="animate-rise space-y-3">
        <p className="inline-block rounded-full bg-white/70 px-4 py-1 text-xs font-semibold uppercase tracking-wider text-ink/70">
          School Bus Tracking Suite
        </p>
        <h1 className="font-display text-4xl font-black leading-tight text-ink sm:text-5xl">
          Control routes. <span className="text-surge">Track live buses.</span> Keep parents informed.
        </h1>
        <p className="max-w-md text-ink/70">
          Built for admins and drivers with secure authentication, real-time location updates, and public GPS tracking.
        </p>
      </div>

      <Card title="Sign In" subtitle="Use your admin/driver account" delay={100}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-semibold text-ink/80">Username</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded-xl border border-ink/20 bg-white px-3 py-2 outline-none ring-skyrail transition focus:ring"
              required
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-semibold text-ink/80">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-xl border border-ink/20 bg-white px-3 py-2 outline-none ring-skyrail transition focus:ring"
              required
            />
          </div>

          {error && <p className="rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-ink px-4 py-2 font-semibold text-white transition hover:bg-skyrail disabled:cursor-not-allowed disabled:opacity-70"
          >
            {loading ? <Spinner label="Signing in" /> : "Sign In"}
          </button>
        </form>
      </Card>
    </div>
  );
}
