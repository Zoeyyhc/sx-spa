<script setup lang="ts">
import { NCard, NSpace, NH2, NText, NGrid, NGridItem, NButton } from "naive-ui";
import { defineProps } from "vue";
import type { User } from "@/interfaces/user.interface";
const props = defineProps<{
  userInfo: User;
}>();
</script>
<template>
  <n-card
    :segmented="{
      content: true,
      footer: 'soft',
    }"
  >
    <n-grid :cols="2" x-gap="12">
      <n-grid-item>
        <n-space vertical>
          <n-h2>Enrolled Courses</n-h2>
          <n-h2 type="info" prefix="bar">
            <n-text type="info">{{
              props.userInfo.enrolled_courses
                ? props.userInfo.enrolled_courses.length
                : 0
            }}</n-text>
          </n-h2>
        </n-space>
      </n-grid-item>
      <n-grid-item>
        <n-space vertical>
          <n-h2>Campus</n-h2>
          <n-h2 type="info" prefix="bar">
            <n-text type="info">{{ props.userInfo.campus.name }}</n-text>
          </n-h2>
        </n-space>
      </n-grid-item>
    </n-grid>
    <template #footer>
      <n-space justify="end">
        <n-button tertiary type="warning" tag="a" href="/browse">
          Enroll New Courses ->
        </n-button>
      </n-space>
    </template>
  </n-card>
</template>