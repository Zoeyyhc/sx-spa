import axios from 'axios';

const axiosInstance = axios.create({
    timeout: 10000,
    baseURL: import.meta.env.VITE_API_BASE,
});


axios.defaults.withCredentials = true;

axiosInstance.interceptors.request.use((config) => {
    console.log(config.withCredentials=true);
    return config;
});

export default axiosInstance;
