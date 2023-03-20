<script setup>
import Table from '@/components/Table.vue';
import { ref, onMounted } from 'vue'

let headers = ref([
    { title: 'Artist', key: 'artist' },
    { title: 'Title', key: 'title' },
    { title: 'Album', key: 'album' },
    { title: 'Year', key: 'year' },
]);

let songs = ref([]);
let itemsPerPage = ref(10);

let search = ref('');

onMounted(() => {
    fetch('http://localhost:8000/api/songs')
        .then(response => response.json())
        .then(data => {
            songs.value = data.songs;
        });
});
</script>

<template>
    <div>
        <h1>Songs</h1>

        lol
        <Table v-model:search="search" :items-per-page="itemsPerPage" :headers="headers" :items="songs"></Table>
    </div>
</template>