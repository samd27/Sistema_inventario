import axios from 'axios';

// Usar variable de entorno o fallback a localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8080';
const ALERTAS_API_BASE_URL = import.meta.env.VITE_ALERTAS_API_URL || 'http://127.0.0.1:8081';
const REPORTES_API_BASE_URL = import.meta.env.VITE_REPORTES_API_URL || 'http://127.0.0.1:8082';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

const alertasApi = axios.create({
  baseURL: `${ALERTAS_API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

const reportesApi = axios.create({
  baseURL: `${REPORTES_API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejar errores globalmente
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// ========== PRODUCTOS ==========
export const productosAPI = {
  getAll: () => api.get('/productos/'),
  getById: (id) => api.get(`/productos/${id}`),
  getBajoStock: () => api.get('/productos/bajo-stock'),
  create: (data) => api.post('/productos/', data),
  update: (id, data) => api.put(`/productos/${id}`, data),
  delete: (id) => api.delete(`/productos/${id}`),
};

// ========== CATEGORÍAS ==========
export const categoriasAPI = {
  getAll: () => api.get('/categorias/'),
  getById: (id) => api.get(`/categorias/${id}`),
  create: (data) => api.post('/categorias/', data),
  update: (id, data) => api.put(`/categorias/${id}`, data),
  delete: (id) => api.delete(`/categorias/${id}`),
};

// ========== PROVEEDORES ==========
export const proveedoresAPI = {
  getAll: () => api.get('/proveedores/'),
  getById: (id) => api.get(`/proveedores/${id}`),
  create: (data) => api.post('/proveedores/', data),
  update: (id, data) => api.put(`/proveedores/${id}`, data),
  delete: (id) => api.delete(`/proveedores/${id}`),
};

// ========== ALERTAS (MICROSERVICIO) ==========
export const alertasAPI = {
  getAll: (estado) => alertasApi.get(`/alertas/${estado ? `?estado=${estado}` : ''}`),
  triggerCheckNow: () => alertasApi.post('/alertas/check-now'),
  getNotifications: () => alertasApi.get('/alertas/notificaciones'),
};

// ========== REPORTES (MICROSERVICIO) ==========
export const reportesAPI = {
  getResumen: () => reportesApi.get('/reportes/resumen'),
  generarSnapshotBajoStock: () => reportesApi.post('/reportes/bajo-stock-snapshot'),
  getTendenciaBajoStock: () => reportesApi.get('/reportes/tendencia-bajo-stock'),
  getEjecuciones: () => reportesApi.get('/reportes/ejecuciones'),
};

export default api;
