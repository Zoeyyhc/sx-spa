import {defineStore} from 'pinia';
import axios from "@/utils/http"

export const useAuthStore = defineStore('auth', {
    state: () => ({
        userInfo: null,
    }),
    getters: {
        getUserInfo: (state) => state.userInfo,
        isLoggedin: (state) => state.userInfo !== null,
    },
    actions:{
        async login(username: string, password: string) {
            const response = await axios.post('/auth/login', {
                username, 
                password
            });

            console.log(response)

        },
    },
});