const TOKEN_KEY = "sbs_access_token";
const REFRESH_KEY = "sbs_refresh_token";
const USER_KEY = "sbs_user";

export function saveSession(payload) {
  localStorage.setItem(TOKEN_KEY, payload.access_token);
  localStorage.setItem(REFRESH_KEY, payload.refresh_token);
  localStorage.setItem(
    USER_KEY,
    JSON.stringify({ role: payload.role, username: payload.username, bus_id: payload.bus_id ?? null }),
  );
}

export function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem(USER_KEY);
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_KEY);
}

export function getUser() {
  const value = localStorage.getItem(USER_KEY);
  if (!value) return null;
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}
