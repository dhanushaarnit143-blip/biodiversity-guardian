/// <reference types="vite/client" />
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: ((import.meta as any).env?.VITE_API_URL as string | undefined) ?? 'http://localhost:8000',
  timeout: 30_000,
  headers: { 'Content-Type': 'application/json' },
});

export default apiClient;
