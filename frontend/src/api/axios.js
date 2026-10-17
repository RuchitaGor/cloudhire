import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('cloudhire_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth endpoints
export const authAPI = {
  register: (data) => api.post('/auth/register/', data),
  login: (data) => api.post('/auth/login/', data),
  me: () => api.get('/auth/me/'),
};

// Job endpoints
export const jobsAPI = {
  listPublished: (search = '') => api.get(`/jobs/?search=${search}`),
  getPublished: (id) => api.get(`/jobs/${id}/`),
  // Recruiter
  listMy: () => api.get('/jobs/manage/'),
  create: (data) => api.post('/jobs/manage/', data),
  update: (id, data) => api.patch(`/jobs/manage/${id}/`, data),
  remove: (id) => api.delete(`/jobs/manage/${id}/`),
};

// Resume endpoints
export const resumeAPI = {
  upload: (formData) =>
    api.post('/resumes/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getMy: () => api.get('/resumes/my/'),
};

// Application endpoints
export const applicationsAPI = {
  apply: (jobId) => api.post(`/applications/apply/${jobId}/`),
  listMy: () => api.get('/applications/my/'),
  // Recruiter
  listByJob: (jobId) => api.get(`/applications/job/${jobId}/`),
  updateStatus: (appId, status) => api.patch(`/applications/${appId}/status/`, { status }),
};

// Admin endpoints
export const adminAPI = {
  listUsers: () => api.get('/auth/admin/users/'),
  deleteUser: (id) => api.delete(`/auth/admin/users/${id}/`),
  getReport: () => api.get('/applications/report/'),
};

export default api;
