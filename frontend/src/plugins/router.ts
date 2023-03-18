import {createRouter, createWebHistory} from 'vue-router';

import Libraries from '@/views/Libraries.vue'
import Songs from '@/views/Songs.vue';

export interface RouteMeta {
    title: string;
    icon: string;
    inNavbar: boolean;
}

export interface Route {
    path: string;
    meta: RouteMeta;
}

export const routes = [
    { 
        path: '/', 
        component: Libraries,
        meta: {
            title: 'Libraries',
            icon: 'mdi-music-box-multiple',
            inNavbar: true,
        }
    },
    {
        path: '/songs',
        component: Songs,
        meta: {
            title: 'Songs',
            icon: 'mdi-music',
            inNavbar: true,
        }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
