// http.ts
import axios from 'axios';
import store from '@/store';

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL + '/api/v1/',
});

console.log('Base URL:', import.meta.env.VITE_API_BASE_URL + '/api/v1/');


http.interceptors.request.use(config => {
  const token = store.state.auth.token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  console.log('Base URL:', import.meta.env.VITE_API_BASE_URL + '/api/v1/');

  return config;
});

export default http;