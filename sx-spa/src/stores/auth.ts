import {defineStore} from 'pinia';
import axios from "@/utils/http"
import { getCurrentUser } from '@/api/user';
import { useLocalStorage, StorageSerializers } from '@vueuse/core';
import type { User } from "@/interfaces/user.interface";

const PREFIX = import.meta.env.VITE_STORAGE_PREFIX || "sx_spa_";
const USER_INFO_PREFIX = (PREFIX ?? "") + "user_info";
export const useAuthStore = defineStore(
    'auth', {
    state: () => ({
        userInfo: useLocalStorage<User | null>(USER_INFO_PREFIX, null, {
            serializer: StorageSerializers.object,
          }),      
    }),
    getters: {
        getUserInfo: (state) => state.userInfo,
        isAdmin: (state) => state.userInfo?.user_type === "admin",
        isLoggedin: (state) => state.userInfo !== null,
    },
    actions:{
        async login(username: string, password: string) {
            
            await axios.post('auth/login', {
                username,
                password});
            
           
            const user = await getCurrentUser();
            this.userInfo = user;
      
        },
        async reload(){
            const user = await getCurrentUser();
            this.userInfo = user;
        },
        async logout(){
            this.userInfo = null;
        }
    },

});