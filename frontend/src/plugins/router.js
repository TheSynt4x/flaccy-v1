import {createRouter, createWebHistory} from 'vue-router';

import Libraries from '@/views/Libraries.vue'
import Songs from '@/views/Songs.vue';

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
    },
    {
        path: '/artists/:name',
        component: () => import('@/views/Artist.vue'),
        meta: {
            inNavbar: false,
        }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
