import { apiClient } from './apiClient';

export const warehouseService = {
  getAll: (skip = 0, limit = 100) => apiClient.get(`/warehouses?skip=${skip}&limit=${limit}`),
  getById: (id) => apiClient.get(`/warehouses/${id}`),
  create: (warehouseData) => apiClient.post('/warehouses', warehouseData),
  update: (id, warehouseData) => apiClient.put(`/warehouses/${id}`, warehouseData),
  delete: (id) => apiClient.delete(`/warehouses/${id}`),
};
