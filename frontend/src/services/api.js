import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8080/api';

const api = axios.create({
  baseURL: API_BASE_URL,
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

export default api;
