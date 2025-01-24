import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';
// Axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getFavorites = async () => await api.get('/favorites/');
export const addToFavorites = async (carId) => await api.post(`/favorites/add/${carId}`);
export const searchCars = async (query) => await api.get('/search/', { params: { q: query } });
export const getNotifications = async () => await api.get('/notifications');
export const getUserProfile = async () => await api.get('/profile/');

// if needed: token-based authentication
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('authToken'); // if token is stored in local storage
    if (token) {
        config.headers.Authorization = 'Token ${token}';
    }
    return config;
    },
    (error) => Promise.reject(error)
);
export default api;