import Vue from 'vue'
import VueRouter from 'vue-router'

import store from '@/store';

import Home from '@/views/Home.vue'
import Register from '@/views/Register.vue'
import Login from '@/views/Login.vue'

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: "Home",
    component: Home,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isAuthenticated) {
      next();
      return;
    }
    next('/login');
  } else {
    next();
  }
});

export default router;