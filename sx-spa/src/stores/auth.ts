import {defineStore} from 'pinia';
import axios from "@/utils/http"
import { getCurrentUser } from '@/api/user';

const PREFIX = import.meta.env.VITE_STORAGE_PREFIX || "sx_spa_";
const USER_INFO_PREFIX = (PREFIX ?? "") + "user_info";
export const useAuthStore = defineStore(
    'auth', {
    state: () => ({
        userInfo: JSON.parse(localStorage.getItem(USER_INFO_PREFIX) ?? "null")
    }),
    getters: {
        getUserInfo: (state) => state.userInfo,
        isLoggedin: (state) => state.userInfo !== null,
    },
    actions:{
        async login(username: string, password: string) {
            
            await axios.post('auth/login', {
                username,
                password});
            
           
            const user = await getCurrentUser();
         
            localStorage.setItem(USER_INFO_PREFIX,JSON.stringify(user));
            this.userInfo = user;
      
        },
        async reload(){
            const user = await getCurrentUser();
            localStorage.setItem(USER_INFO_PREFIX,JSON.stringify(user));
            this.userInfo = user;
        },
        async logout(){
            localStorage.removeItem(USER_INFO_PREFIX);
            this.userInfo = null;
        }
    },

});