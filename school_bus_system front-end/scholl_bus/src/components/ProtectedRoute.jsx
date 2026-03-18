import { Navigate, useLocation } from "react-router-dom";
import { getUser } from "../services/auth";

export default function ProtectedRoute({ allowedRoles, children }) {
  const location = useLocation();
  const user = getUser();

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}
