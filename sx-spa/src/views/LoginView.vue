<script  setup lang = "ts" >
import { NSpace, NH1, NH5, NButton,NForm,NFormItem,NInput,NA} from 'naive-ui';
import {ref,computed} from 'vue';
import {useAuthStore} from '@/stores/auth';
import {useRouter} from "vue-router";


interface LoginForm {
    username: string;
    password: string;
}   
const router = useRouter();
const formRef = ref<LoginForm | null>(null);
const formValue = ref<LoginForm>({username: 'admin', password: 'admin'});

const authStore = useAuthStore();
const loading = ref(false);
const disabled = computed(
    () => formValue.value.username === ""|| formValue.value.password === ""
);
const handleLogin = async() => {
    try {
    loading.value = true;
    await authStore.login(formValue.value.username, formValue.value.password);
    router.replace("/");
  } finally {
    loading.value = false;
  }
};

</script>

<template>
    <div class="login">
        <n-space vertical class="login-card">
            <n-h1>Welcome to SHANGXUE Online</n-h1>
            <n-h5 class="">Please Login to Continue</n-h5>     
            <n-form ref="formRef" :model="formValue">
                <n-form-item path="username" label="Username:">
                    <n-input type="text" placeholder="Please input username: " v-model:value="formValue.username"></n-input>
                </n-form-item>
                <n-form-item path="password" label="Password:">
                    <n-input type="password" placeholder="Please input password: " v-model:value="formValue.password"></n-input>
                </n-form-item>
            </n-form>
            <n-space align="center" justify="space-between">
                <n-a href = "/forget">
                    Forget your password ?
                </n-a>
                <n-space>
                    <n-button tag="a" size="large" href="/register">
                        Register
                    </n-button>
                    <n-button type="primary" tag="a" size="large"
                    :loading = "loading"
                    :disabled = "disabled"
                    @click="handleLogin">
                    Login
                    </n-button>
                </n-space>
            </n-space>
        </n-space>
    </div>
</template>

<style lang="less">
.login {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    height: 100vh;
    width: 100%;
}
.login-card{
    margin-right :15vw;
}
</style>