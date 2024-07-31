import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/home.vue'),
    meta: { pageName: 'Home' }
  },
  {
    path: '/notes',
    name: 'Notes',
    component: () => import('../views/notes.vue'),
  },
  {
    path: '/images',
    name: 'Images',
    component: () => import('../views/images.vue'),
  },
  {
    path: '/library',
    name: 'Library',
    component: () => import('../views/library.vue'),
  },
  {
    path: '/logs',
    name: 'Logs',
    component: () => import('../views/logs.vue'),
  },
  {
    path: '/doc/:name',
    name: 'note',
    component: () => import('../views/note.vue'),
    props: true,
  },
  {
  path: '/:pathMatch(.*)*',
  name: 'NotFound',
  component: () => import('../views/404.vue'),
}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

