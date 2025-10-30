import axios from "axios"

const API_BASE = "http://localhost:8000"

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authAPI = {
  login: (username, password) => api.post("/auth/login", { username, password }),
}

export const inventoryAPI = {
  importInventory: (file) => {
    const formData = new FormData()
    formData.append("file", file)
    return api.post("/inventory/import", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },

  transferInventory: (file) => {
    const formData = new FormData()
    formData.append("file", file)
    return api.post("/inventory/transfer", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },

  recordSales: (file) => {
    const formData = new FormData()
    formData.append("file", file)
    return api.post("/inventory/sales", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },

  getStockStatus: () => api.get("/inventory/stock-status"),

  getAnalytics: (params) => api.get("/inventory/analytics", { params }),
}

export default api
