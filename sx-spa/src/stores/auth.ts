import {defineStore} from 'pinia';
import axios from "@/utils/http"
import { getCurrentUser } from '@/api/user';

const PREFIX = import.meta.env.VITE_STORAGE_PREFIX;
const USER_INFO_PREFIX = PREFIX + 'userInfo';
export const useAuthStore = defineStore('auth', {
    state: () => ({
        userInfo: JSON.parse(localStorage.getItem(USER_INFO_PREFIX) ?? 'null'),
    }),
    getters: {
        getUserInfo: (state) => state.userInfo,
        isLoggedin: (state) => state.userInfo !== null,
    },
    actions:{
        async login(username: string, password: string) {
            try {
                const response = await axios.post('auth/login', {
                    username, 
                    password
                });
                const user = await getCurrentUser();
                localStorage.setItem(USER_INFO_PREFIX, JSON.stringify(user));
            } catch (error) {
                console.error('Login error:', error);
            }
        },
        },
    });
