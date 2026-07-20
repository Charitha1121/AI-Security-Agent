import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export const authApi = {

  login: (email, password) =>
    api.post("/auth/login", {
      username: email,
      password,
    }),

  me: () =>
    api.get("/auth/me"),
};


export const fileApi = {

  upload: (file) => {

    const formData = new FormData();

    formData.append("file", file);

    return api.post(
      "/files/upload",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
  },

  getAll: () =>
    api.get("/files/"),
};


export const scanApi = {

  scan: (fileId) =>
    api.post(`/scan/${fileId}`),

  get: (fileId) =>
    api.get(`/scan/${fileId}`),

  rescan: (fileId) =>
    api.put(`/scan/${fileId}/rescan`),
};


export const dashboardApi = {

  stats: () =>
    api.get("/dashboard/stats"),
};
export const getScanHistory = async () => {
  const response = await api.get(
    "/scan/history"
  );

  return response.data;
};
export default api;