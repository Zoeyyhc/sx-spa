<script setup lang="ts">
import type { CourseBasicInfo } from "@/api/course";
import type { User } from "@/interfaces/user.interface";
import { NGrid, NGridItem, NCard, NA, NP, NSpace, NButton, NSpin } from "naive-ui";
import { useRouter } from "vue-router";
import { ref } from 'vue';

// Add loading state
const loading = ref(false);

// Make props optional with defaults
const props = withDefaults(defineProps<{
  userInfo?: User;
  courses?: CourseBasicInfo[];
}>(), {
  courses: () => [],
  userInfo: undefined
});

const router = useRouter();

const isEnrolledCourse = (course_id: string) => {
  if (!props.userInfo) return false;
  if (props.userInfo.user_type === "User.Admin") return true;
  console.log(props.userInfo.enrolled_courses);
  return props.userInfo.enrolled_courses?.some(course => course.id === course_id) ?? false;
};

const handleCourseClick = (course_id: string) => {
  if (isEnrolledCourse(course_id)) {
    router.replace(`/courses/${course_id}`);
  }
};


</script>

<template>
  <n-spin :show="loading">
    <n-grid :cols="3" :x-gap="12" :y-gap="8" v-if="courses && courses.length">
      <n-grid-item v-for="course in courses" :key="course.id">
        <n-card :title="course.name">
          <template #cover>
            <n-a @click="handleCourseClick(course.id)">
              <img :src="course.cover_image" alt="" style="height: 100%" />
            </n-a>
          </template>
          <template #footer>
            <n-space
              justify="space-between"
              align="center"
              class="h-8"
              v-if="!isEnrolledCourse(course.id)"
            >
              <span class="text-orange-400 py-2">
                ${{ course.original_price }}
              </span>
              <n-button size="small" type="success">Purchase now</n-button>
            </n-space>
            <n-space class="h-8" align="center" v-else>
              <span class="text-green-500">Enrolled</span>
            </n-space>
          </template>
          <n-p class="mt-1">
            Teacher: {{ course.teacher?.display_name || 'Not assigned' }}
            Course ID: {{ course.id }}
          </n-p>
          <n-p>Description: {{ course.description || 'No description available' }}</n-p>
        </n-card>
      </n-grid-item>
    </n-grid>
    <n-space v-else justify="center">
      <n-p>No courses available</n-p>
    </n-space>
  </n-spin>
</template>
