import axios from "axios";
import { clearSession, getRefreshToken, getToken } from "./auth";

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 12000,
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let isRefreshing = false;
let queue = [];

function resolveQueue(error, token = null) {
  queue.forEach((promise) => {
    if (error) {
      promise.reject(error);
    } else {
      promise.resolve(token);
    }
  });
  queue = [];
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status !== 401 || originalRequest?._retry) {
      return Promise.reject(error);
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        queue.push({ resolve, reject });
      }).then((token) => {
        originalRequest.headers.Authorization = `Bearer ${token}`;
        return api(originalRequest);
      });
    }

    originalRequest._retry = true;
    isRefreshing = true;

    try {
      const refreshToken = getRefreshToken();
      if (!refreshToken) {
        clearSession();
        return Promise.reject(error);
      }

      const refreshResponse = await axios.post(`${API_BASE_URL}/auth/refresh`, {
        refresh_token: refreshToken,
      });

      const newAccess = refreshResponse.data.access_token;
      const newRefresh = refreshResponse.data.refresh_token;

      localStorage.setItem("sbs_access_token", newAccess);
      localStorage.setItem("sbs_refresh_token", newRefresh);

      resolveQueue(null, newAccess);
      originalRequest.headers.Authorization = `Bearer ${newAccess}`;
      return api(originalRequest);
    } catch (refreshError) {
      resolveQueue(refreshError, null);
      clearSession();
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  },
);

function extractError(error) {
  return error?.response?.data?.detail || "Something went wrong";
}

export async function login(formData) {
  const params = new URLSearchParams(formData);
  const response = await api.post("/auth/login", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return response.data;
}

export async function signup(payload) {
  const response = await api.post("/auth/signup", payload);
  return response.data;
}

export async function getMe() {
  const response = await api.get("/auth/me");
  return response.data;
}

export async function createRoute(payload) {
  try {
    const response = await api.post("/routes", payload);
    return response.data;
  } catch (error) {
    throw new Error(extractError(error));
  }
}

export async function getRoutes() {
  const response = await api.get("/routes");
  return response.data;
}

export async function createBus(payload) {
  try {
    const response = await api.post("/buses", payload);
    return response.data;
  } catch (error) {
    throw new Error(extractError(error));
  }
}

export async function getBuses(search = "") {
  const response = await api.get("/buses", { params: { search } });
  return response.data;
}

export async function getDrivers() {
  const response = await api.get("/drivers");
  return response.data;
}

export async function assignDriver(busId, driverId) {
  const response = await api.put(`/buses/${busId}/assign-driver/${driverId}`);
  return response.data;
}

export async function createStudent(payload) {
  try {
    const response = await api.post("/students", payload);
    return response.data;
  } catch (error) {
    throw new Error(extractError(error));
  }
}

export async function getStudents(page = 1, pageSize = 8) {
  const response = await api.get("/students", { params: { page, page_size: pageSize } });
  return response.data;
}

export async function assignStudent(studentId, busId) {
  const response = await api.put(`/students/${studentId}/assign/${busId}`);
  return response.data;
}

export async function updateGps(busId, payload) {
  const response = await api.post(`/gps/${busId}`, payload);
  return response.data;
}

export async function getGps(busId) {
  const response = await api.get(`/gps/${busId}`);
  return response.data;
}

export async function getTimetable(routeId) {
  const response = await api.get(`/timetable/${routeId}`);
  return response.data;
}
