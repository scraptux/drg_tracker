import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    { path: '/', component: () => import('./views/Index.vue') },
    { path: '/:drg/', component: () => import('./views/DRG.vue') },
    { path: '/:drg/version/:year', component: () => import('./views/Version.vue') },
    { path: '/:drg/version/:year/kapitel/:kapitel', component: () => import('./views/Kapitel.vue') },
    { path: '/:drg/version/:year/gruppe/:gruppe', component: () => import('./views/Gruppe.vue') },
    { path: '/ops/version/:year/dreisteller/:dcode', component: () => import('./views/Dreisteller.vue') },
    { path: '/:drg/version/:year/code/:code', component: () => import('./views/Code.vue') },
    { path: '/:drg/version/:year/track/:code', component: () => import('./views/Track.vue') },
    { path: '/search/:s', component: () => import('./views/Search.vue') },
    { path: '/track/', component: () => import('./views/MultiTrack.vue') },
    { path: '/track/:sharecode', component: () => import('./views/MultiTrack.vue') },
    { path: '/impressum', component: () => import('./views/Impressum.vue') }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes,
})

export default router