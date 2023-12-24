import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Main from '../views/Main.vue'
import test from '../views/test.vue'
import Analysis from '../views/Analysis.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path:'/main',
    name:'Main',
    component:Main
  },
  {
    path:'/test',
    name:'test',
    component:test
  },
  {
    path:'/analysis',
    name:'Analysis',
    component:Analysis
  }
]

const router = new VueRouter({
  routes
})

export default router
