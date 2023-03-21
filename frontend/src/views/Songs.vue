<script setup>
import Table from '@/components/Table.vue';
import { ref, onMounted } from 'vue'

import { useSongStore } from '@/store/songs';

const songStore = useSongStore();

let headers = ref([
    { title: 'Artist', key: 'artist' },
    { title: 'Title', key: 'title' },
    { title: 'Album', key: 'album' },
    { title: 'Year', key: 'year' },
]);

let itemsPerPage = ref(10);

let search = ref('');

onMounted(async () => {
    await songStore.fetchSongs();
});
</script>

<template>
    <div>
        <h1>Songs</h1>

        <Table v-model:search="search" :items-per-page="itemsPerPage" :headers="headers" :items="songStore.allSongs"></Table>
    </div>
</template>