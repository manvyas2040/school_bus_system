import { Bus, LocateFixed, LogOut, ShieldCheck } from "lucide-react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { clearSession, getUser } from "../../services/auth";

function navClass({ isActive }) {
  return `rounded-full px-4 py-2 text-sm font-semibold transition ${
    isActive ? "bg-ink text-white" : "text-ink/80 hover:bg-white/60"
  }`;
}

export default function Navbar() {
  const user = getUser();
  const navigate = useNavigate();

  const logout = () => {
    clearSession();
    navigate("/login");
  };

  return (
    <header className="sticky top-0 z-20 border-b border-white/40 bg-white/70 backdrop-blur-lg">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-3 sm:px-6">
        <Link to="/" className="flex items-center gap-2 text-ink">
          <Bus className="h-5 w-5 text-surge" />
          <span className="font-display text-lg font-bold tracking-tight">TransitDesk</span>
        </Link>

        <nav className="flex items-center gap-2">
          <NavLink to="/track" className={navClass}>
            Track Bus
          </NavLink>
          {user?.role === "admin" && (
            <NavLink to="/admin" className={navClass}>
              <ShieldCheck className="mr-2 inline h-4 w-4" />
              Admin
            </NavLink>
          )}
          {user?.role === "driver" && (
            <NavLink to="/driver" className={navClass}>
              <LocateFixed className="mr-2 inline h-4 w-4" />
              Driver
            </NavLink>
          )}
          {user && (
            <button
              onClick={logout}
              className="rounded-full bg-surge px-4 py-2 text-sm font-semibold text-white transition hover:bg-red-700"
            >
              <LogOut className="mr-2 inline h-4 w-4" />
              Logout
            </button>
          )}
          {!user && (
            <NavLink to="/login" className={navClass}>
              Login
            </NavLink>
          )}
        </nav>
      </div>
    </header>
  );
}
