import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';
// Axios instance
const api = axios.create({
    baseURL: API_BASE,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getFavorites = () => axios.get(`${API_BASE}/favorites/`);
export const addFavorite = (carId) => axios.post(`${API_BASE}/favorites/add/${carId}`);
export const searchCars = (query) => axios.get(`${API_BASE}/search/`, { params: { q: query } });
export const getNotifications = () => axios.get(`${API_BASE}/notifications`);
export const getProfile = () => axios.get(`${API_BASE}/profile/`);
export const getCars = () => axios.get(`${API_BASE}/cars/`);
export const getCarDetails = (carId) => axios.get(`${API_BASE}/cars/${carId}/`);

// if needed: token-based authentication
/*api.interceptors.request.use((config) => {
    const token = localStorage.getItem('authToken'); // if token is stored in local storage
    if (token) {
        config.headers.Authorization = 'Token ${token}';
    }
    return config;
    },
    (error) => Promise.reject(error)
);*/
export default api;