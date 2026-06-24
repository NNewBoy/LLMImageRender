import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory('/llmimagerender/'),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/pages/HomePage.vue'),
    },
    {
      path: '/render/single',
      name: 'single-render',
      component: () => import('@/pages/SingleRenderPage.vue'),
    },
    {
      path: '/render/scene',
      name: 'scene-render',
      component: () => import('@/pages/SceneRenderPage.vue'),
    },
    {
      path: '/render/:taskId',
      name: 'render-detail',
      component: () => import('@/pages/RenderDetailPage.vue'),
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/pages/HistoryPage.vue'),
    },
    {
      path: '/gallery',
      name: 'gallery',
      component: () => import('@/pages/GalleryPage.vue'),
    },
  ],
})

export default router