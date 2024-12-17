<script setup lang="ts">
import { NLayout } from 'naive-ui';
import LayoutContent from '@/layout/layoutContent.vue';
import LayoutSidebar from '@/layout/LayoutSidebar.vue';
import LayoutHeader from '@/layout/LayoutHeader.vue';
</script>


<template>
    <n-layout position="absolute" has-sider>
        <layout-sidebar> </layout-sidebar>
        <n-layout>
            <layout-header></layout-header>
            <layout-content></layout-content>
        </n-layout>
    </n-layout>
</template>
