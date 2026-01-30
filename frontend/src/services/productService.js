import { apiClient } from './apiClient';

export const productService = {
  getAll: (skip = 0, limit = 100) => apiClient.get(`/products?skip=${skip}&limit=${limit}`),
  getById: (id) => apiClient.get(`/products/${id}`),
  create: (productData) => apiClient.post('/products', productData),
  update: (id, productData) => apiClient.put(`/products/${id}`, productData),
  delete: (id) => apiClient.delete(`/products/${id}`),
};
