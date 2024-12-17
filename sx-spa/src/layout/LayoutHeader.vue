<script setup lang="ts">
import { NLayoutHeader, NBreadcrumb, NBreadcrumbItem, NDropdown, NAvatar, NSpace} from 'naive-ui';
import { useAuthStore } from '@/stores/auth';
import { storeToRefs } from 'pinia';
import { computed } from 'vue';
import router from "@/router";
const authStore = useAuthStore();
const auth = storeToRefs(authStore);
const displayName = computed(() => {
    return auth.userInfo.value?.display_name || auth.userInfo.value?.username;
});
const options = [
    { label: 'Signout', key: 'logout' },
];
const handleOptionSelect = async (key: string) => {
  if (key === "logout") {
    await authStore.logout();
    await router.push("/login");
  }
};
</script>

<template>
    <n-layout-header bordered>
        <n-breadcrumb class="my-1">
            <n-breadcrumb-item> Dashboard</n-breadcrumb-item>
            <n-breadcrumb-item> Home </n-breadcrumb-item>
        </n-breadcrumb>
        <n-space class="navs my-1" :size="20" align="center">
            <span>Hello {{ displayName }}</span>
            <n-dropdown :options="options" placement="bottom-end" @select="handleOptionSelect">
                <n-avatar size="small" round>
                    <img src="~@/assets/logo.jpg" alt="" />
                </n-avatar>
            </n-dropdown>
        </n-space>
    </n-layout-header>
</template>


<style scoped>
.n-layout-header {
  display: flex;
  font-size: 1.1em;
  padding: 8px 18px;
}
.navs {
  margin-left: auto;
  line-height: 1px;
}

</style>