import { createRouter, createWebHistory } from 'vue-router'
import layout from '@/layout/index.vue';
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'layout',
      redirect: '/home',
      component: layout,
      children: [
        {
          name: 'home',
          path: '/home',
          component: () => import('../views/HomeView.vue'),
          meta: {
            requiresAuth: true,
            title: "Home",
          },
        },
        {
          name: "browse",
          path: "/browse",
          component: () => import("../views/BrowseView.vue"),
          meta: {
            title: "All Courses",
            requiresAuth: true,
          },
        },
        {
          name: "courses",
          path: "/courses",
          component: () => import("../views/CoursesView.vue"),
          meta: {
            requiresAuth: true,
            title: "Course",
          },
        },
        {
          name: "course",
          path: "/courses/:id",
          component: () => import("../views/CourseView.vue"),
          meta: {
            requiresAuth: true,
            title: "Course Page",
          },
        },
      ]
      
    },
    {
      path: '/login',
      name: 'login', 
      component: () => import('../views/LoginView.vue'),
      meta:{
        requiresAuth: false,
        title: "Login",
      }
    },
  ],
})
router.afterEach((to) => {
  document.title = to.meta.title || to.name?.toString() || "ShangxueOnline";
});

router.beforeEach((to) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isLoggedin) {
    return {
      name: "login",
      query: { redirect: to.fullPath },
    };
  }
});

export default router
